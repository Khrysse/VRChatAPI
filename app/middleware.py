"""
Rate limiting and security middleware
"""
import time
from collections import defaultdict, deque
from typing import Dict, Deque
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using sliding window algorithm
    """
    def __init__(self, app, calls_per_minute: int = 60, calls_per_hour: int = 1000):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.calls_per_hour = calls_per_hour
        
        # Store requests by IP: {ip: deque of timestamps}
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)
        
    def get_client_ip(self, request: Request) -> str:
        """Get client IP with support for proxies"""
        # Check for forwarded headers (common in reverse proxy setups)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP in the chain
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
            
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"
    
    def cleanup_old_requests(self, ip: str, current_time: float):
        """Remove requests older than 1 hour"""
        requests = self.requests[ip]
        cutoff_time = current_time - 3600  # 1 hour ago
        
        while requests and requests[0] < cutoff_time:
            requests.popleft()
    
    def is_rate_limited(self, ip: str, current_time: float) -> tuple[bool, str]:
        """Check if IP is rate limited"""
        self.cleanup_old_requests(ip, current_time)
        requests = self.requests[ip]
        
        # Check minute limit
        minute_cutoff = current_time - 60
        minute_requests = sum(1 for req_time in requests if req_time > minute_cutoff)
        
        if minute_requests >= self.calls_per_minute:
            return True, f"Rate limit exceeded: {minute_requests}/{self.calls_per_minute} requests per minute"
        
        # Check hour limit
        if len(requests) >= self.calls_per_hour:
            return True, f"Rate limit exceeded: {len(requests)}/{self.calls_per_hour} requests per hour"
        
        return False, ""
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks and docs
        if request.url.path in ["/api/health", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        # Check if rate limited
        is_limited, message = self.is_rate_limited(client_ip, current_time)
        
        if is_limited:
            logger.warning(f"Rate limit exceeded for IP {client_ip}: {message}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later.",
                headers={"Retry-After": "60"}
            )
        
        # Record this request
        self.requests[client_ip].append(current_time)
        
        # Add rate limit headers to response
        response = await call_next(request)
        
        # Calculate remaining requests
        requests = self.requests[client_ip]
        minute_cutoff = current_time - 60
        minute_requests = sum(1 for req_time in requests if req_time > minute_cutoff)
        
        response.headers["X-RateLimit-Limit-Minute"] = str(self.calls_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(max(0, self.calls_per_minute - minute_requests))
        response.headers["X-RateLimit-Limit-Hour"] = str(self.calls_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(max(0, self.calls_per_hour - len(requests)))
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
        
        # Only add HSTS for HTTPS requests
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response