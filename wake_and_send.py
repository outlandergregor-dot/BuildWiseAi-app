#!/usr/bin/env python3
"""
Wake up the BuildWiseAI sandbox and send onboarding emails.

This script attempts to wake up the sandbox by making repeated requests
until it responds, then calls the onboarding email API.
"""

import time
import sys
import logging
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ubuntu/BuildWiseAi-app/onboarding_emails.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

BASE_URL = "https://3000-i15h83mk6ch6w41lvgs8n-f6f9bf8a.us2.manus.computer"
MAX_WAKE_ATTEMPTS = 10
WAKE_DELAY = 10  # seconds between wake attempts


def wake_up_sandbox():
    """
    Attempt to wake up the sandbox by making repeated requests.
    
    Returns:
        bool: True if sandbox is awake, False otherwise
    """
    logger.info(f"Attempting to wake up sandbox at {BASE_URL}")
    
    for attempt in range(1, MAX_WAKE_ATTEMPTS + 1):
        try:
            logger.info(f"Wake attempt {attempt}/{MAX_WAKE_ATTEMPTS}")
            response = requests.get(BASE_URL, timeout=15)
            
            if response.status_code == 200:
                logger.info("Sandbox is awake and responding!")
                return True
            elif response.status_code == 502 or response.status_code == 503:
                logger.info(f"Sandbox still asleep (status {response.status_code}), waiting {WAKE_DELAY} seconds...")
                time.sleep(WAKE_DELAY)
            else:
                logger.warning(f"Unexpected status code: {response.status_code}")
                time.sleep(WAKE_DELAY)
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed: {str(e)}")
            time.sleep(WAKE_DELAY)
    
    logger.error("Failed to wake up sandbox after maximum attempts")
    return False


def send_onboarding_emails():
    """
    Call the tRPC API to send pending onboarding emails.
    
    Returns:
        dict: Results of the operation
    """
    endpoint = f"{BASE_URL}/api/trpc/onboardingEmails.sendPendingEmails"
    logger.info(f"Calling onboarding email API: {endpoint}")
    
    try:
        response = requests.post(
            endpoint,
            json={},
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            logger.info("Successfully sent pending onboarding emails")
            
            # Extract email count
            emails_sent = 0
            if isinstance(result, dict):
                result_data = result.get('result', {})
                if isinstance(result_data, dict):
                    emails_sent = result_data.get('data', {}).get('emailsSent', 0)
            
            return {
                'success': True,
                'status_code': response.status_code,
                'emails_sent': emails_sent,
                'data': result,
                'timestamp': datetime.utcnow().isoformat()
            }
        else:
            logger.error(f"API request failed with status {response.status_code}")
            return {
                'success': False,
                'status_code': response.status_code,
                'error': response.text[:500],
                'timestamp': datetime.utcnow().isoformat()
            }
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }


def main():
    """Main execution flow."""
    logger.info("=" * 80)
    logger.info("BUILDWISEAI ONBOARDING EMAIL AUTOMATION")
    logger.info("=" * 80)
    logger.info(f"Started at: {datetime.utcnow().isoformat()}")
    
    # Step 1: Wake up the sandbox
    if not wake_up_sandbox():
        logger.error("Could not wake up sandbox. Exiting.")
        sys.exit(1)
    
    # Step 2: Send onboarding emails
    results = send_onboarding_emails()
    
    # Step 3: Log results
    logger.info("=" * 80)
    logger.info("EXECUTION RESULTS")
    logger.info("=" * 80)
    logger.info(f"Success: {results.get('success', False)}")
    logger.info(f"Timestamp: {results.get('timestamp', 'N/A')}")
    
    if results.get('success'):
        logger.info(f"Emails Sent: {results.get('emails_sent', 0)}")
        logger.info(f"Status Code: {results.get('status_code', 'N/A')}")
    else:
        logger.error(f"Error: {results.get('error', 'Unknown error')}")
        logger.error(f"Status Code: {results.get('status_code', 'N/A')}")
    
    logger.info("=" * 80)
    logger.info(f"Completed at: {datetime.utcnow().isoformat()}")
    logger.info("=" * 80)
    
    sys.exit(0 if results.get('success') else 1)


if __name__ == '__main__':
    main()
