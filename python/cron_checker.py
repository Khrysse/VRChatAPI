#!/usr/bin/env python3
"""
Cron-like task checker for VRChat Bridge
Runs periodic tasks without relying on system cron
"""

import time
import requests
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_auth_status():
    """Check VRChat authentication status"""
    try:
        apache_port = os.getenv('APACHE_PORT', '8080')
        url = f"http://localhost:{apache_port}/api/cron/checkAuth.php"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logger.info("Auth check completed successfully")
        else:
            logger.warning(f"Auth check failed with status {response.status_code}")
            
    except Exception as e:
        logger.error(f"Auth check error: {e}")

def main():
    """Main loop for periodic tasks"""
    logger.info("Starting cron checker service")
    
    # Check interval in seconds (24 hours = 86400 seconds)
    check_interval = int(os.getenv('CRON_CHECK_INTERVAL', '86400'))
    
    while True:
        try:
            logger.info(f"Running scheduled tasks at {datetime.now()}")
            check_auth_status()
            
            # Sleep until next check
            logger.info(f"Next check in {check_interval} seconds")
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            logger.info("Cron checker stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error in cron checker: {e}")
            time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    main() 