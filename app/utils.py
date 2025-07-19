"""
Common utilities for security, validation, and error handling
"""
import re
import logging
from typing import Optional
from fastapi import HTTPException
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# VRChat ID patterns for validation
VRCHAT_USER_ID_PATTERN = re.compile(r'^usr_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
VRCHAT_GROUP_ID_PATTERN = re.compile(r'^grp_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
VRCHAT_WORLD_ID_PATTERN = re.compile(r'^wrld_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
VRCHAT_INSTANCE_ID_PATTERN = re.compile(r'^[0-9a-zA-Z~:_-]+$')

def validate_vrchat_user_id(user_id: str) -> str:
    """Validate VRChat user ID format"""
    if not user_id or not VRCHAT_USER_ID_PATTERN.match(user_id):
        logger.warning(f"Invalid user ID format attempted: {user_id[:10]}...")
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    return user_id

def validate_vrchat_group_id(group_id: str) -> str:
    """Validate VRChat group ID format"""
    if not group_id or not VRCHAT_GROUP_ID_PATTERN.match(group_id):
        logger.warning(f"Invalid group ID format attempted: {group_id[:10]}...")
        raise HTTPException(status_code=400, detail="Invalid group ID format")
    return group_id

def validate_vrchat_world_id(world_id: str) -> str:
    """Validate VRChat world ID format"""
    if not world_id or not VRCHAT_WORLD_ID_PATTERN.match(world_id):
        logger.warning(f"Invalid world ID format attempted: {world_id[:10]}...")
        raise HTTPException(status_code=400, detail="Invalid world ID format")
    return world_id

def validate_vrchat_instance_id(instance_id: str) -> str:
    """Validate VRChat instance ID format"""
    if not instance_id or not VRCHAT_INSTANCE_ID_PATTERN.match(instance_id) or len(instance_id) > 100:
        logger.warning(f"Invalid instance ID format attempted: {instance_id[:10]}...")
        raise HTTPException(status_code=400, detail="Invalid instance ID format")
    return instance_id

def validate_pagination_params(offset: Optional[int] = None, n: Optional[int] = None) -> tuple[Optional[int], Optional[int]]:
    """Validate and limit pagination parameters"""
    if offset is not None:
        if offset < 0:
            raise HTTPException(status_code=400, detail="Offset must be non-negative")
        if offset > 10000:  # Reasonable limit
            raise HTTPException(status_code=400, detail="Offset too large")
    
    if n is not None:
        if n < 1:
            raise HTTPException(status_code=400, detail="Count must be positive")
        if n > 100:  # Reasonable limit to prevent abuse
            n = 100
            logger.info(f"Pagination count limited to {n}")
    
    return offset, n

def sanitize_error_message(error: str, status_code: int) -> str:
    """Sanitize error messages to prevent information disclosure"""
    # Map common error patterns to generic messages
    if status_code == 401:
        return "Authentication required"
    elif status_code == 403:
        return "Access denied"
    elif status_code == 404:
        return "Resource not found"
    elif status_code == 429:
        return "Rate limit exceeded"
    elif status_code >= 500:
        # Never expose internal error details
        logger.error(f"Internal error: {error}")
        return "Internal server error"
    else:
        # For client errors, provide generic message
        return "Request could not be processed"

async def make_vrchat_request(url: str, headers: dict, cookies: dict) -> httpx.Response:
    """Make a secure request to VRChat API with proper error handling"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers, cookies=cookies)
            return response
    except httpx.TimeoutException:
        logger.warning(f"VRChat API timeout for URL: {url}")
        raise HTTPException(status_code=504, detail="VRChat API timeout")
    except httpx.RequestError as e:
        logger.error(f"VRChat API request error: {str(e)}")
        raise HTTPException(status_code=502, detail="VRChat API unavailable")

def handle_vrchat_response(response: httpx.Response, operation: str) -> dict:
    """Handle VRChat API responses with proper error sanitization"""
    if response.status_code == 200:
        try:
            return response.json()
        except Exception:
            logger.error(f"Invalid JSON response from VRChat API for {operation}")
            raise HTTPException(status_code=502, detail="Invalid response from VRChat API")
    
    # Sanitize error message
    sanitized_message = sanitize_error_message(response.text, response.status_code)
    logger.warning(f"VRChat API error for {operation}: {response.status_code} - {response.text[:100]}...")
    raise HTTPException(status_code=response.status_code, detail=sanitized_message)