#!/usr/bin/env python3
"""
BuildWiseAI Onboarding Email Sender

This script calls the tRPC API endpoint to send pending onboarding emails
to new users, improving activation and retention through automated email sequences.

Usage:
    python3 send_onboarding_emails.py [--url BASE_URL] [--auth-token TOKEN]

Environment Variables:
    BUILDWISE_API_URL: Base URL of the BuildWiseAI application
    BUILDWISE_AUTH_TOKEN: Optional authentication token for API requests
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

import requests

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


class OnboardingEmailSender:
    """Handles sending pending onboarding emails via tRPC API."""
    
    def __init__(self, base_url: str, auth_token: Optional[str] = None):
        """
        Initialize the email sender.
        
        Args:
            base_url: Base URL of the BuildWiseAI application
            auth_token: Optional authentication token for API requests
        """
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.session = requests.Session()
        
        # Set up headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        
        if self.auth_token:
            self.session.headers.update({
                'Authorization': f'Bearer {self.auth_token}'
            })
    
    def send_pending_emails(self, retry_count: int = 3) -> Dict[str, Any]:
        """
        Call the tRPC mutation to send pending onboarding emails.
        
        Args:
            retry_count: Number of times to retry on failure
            
        Returns:
            Dictionary containing the API response with email send results
        """
        endpoint = f"{self.base_url}/api/trpc/onboardingEmails.sendPendingEmails"
        
        logger.info(f"Calling tRPC endpoint: {endpoint}")
        
        for attempt in range(1, retry_count + 1):
            try:
                # Make the API request
                response = self.session.post(
                    endpoint,
                    json={},  # Empty payload for mutation
                    timeout=30
                )
                
                # Check if request was successful
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Successfully sent pending onboarding emails")
                    return {
                        'success': True,
                        'status_code': response.status_code,
                        'data': result,
                        'timestamp': datetime.utcnow().isoformat(),
                        'attempt': attempt
                    }
                elif response.status_code == 401:
                    logger.error("Authentication failed. Please check your auth token.")
                    return {
                        'success': False,
                        'status_code': response.status_code,
                        'error': 'Authentication failed',
                        'timestamp': datetime.utcnow().isoformat(),
                        'attempt': attempt
                    }
                elif response.status_code == 503:
                    logger.warning(f"Service unavailable (attempt {attempt}/{retry_count}). Application may be asleep.")
                    if attempt < retry_count:
                        logger.info(f"Retrying in 5 seconds...")
                        import time
                        time.sleep(5)
                        continue
                else:
                    logger.error(f"API request failed with status {response.status_code}: {response.text}")
                    if attempt < retry_count:
                        logger.info(f"Retrying in 5 seconds...")
                        import time
                        time.sleep(5)
                        continue
                    
                    return {
                        'success': False,
                        'status_code': response.status_code,
                        'error': response.text,
                        'timestamp': datetime.utcnow().isoformat(),
                        'attempt': attempt
                    }
                    
            except requests.exceptions.Timeout:
                logger.error(f"Request timeout (attempt {attempt}/{retry_count})")
                if attempt < retry_count:
                    logger.info(f"Retrying in 5 seconds...")
                    import time
                    time.sleep(5)
                    continue
                    
                return {
                    'success': False,
                    'error': 'Request timeout',
                    'timestamp': datetime.utcnow().isoformat(),
                    'attempt': attempt
                }
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt}/{retry_count}): {str(e)}")
                if attempt < retry_count:
                    logger.info(f"Retrying in 5 seconds...")
                    import time
                    time.sleep(5)
                    continue
                    
                return {
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat(),
                    'attempt': attempt
                }
        
        return {
            'success': False,
            'error': f'Failed after {retry_count} attempts',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def log_results(self, results: Dict[str, Any]) -> None:
        """
        Log the results of the email sending operation.
        
        Args:
            results: Dictionary containing the operation results
        """
        logger.info("=" * 80)
        logger.info("ONBOARDING EMAIL SEND RESULTS")
        logger.info("=" * 80)
        logger.info(f"Timestamp: {results.get('timestamp', 'N/A')}")
        logger.info(f"Success: {results.get('success', False)}")
        
        if results.get('success'):
            data = results.get('data', {})
            
            # Extract email count from response
            if isinstance(data, dict):
                result_data = data.get('result', {})
                if isinstance(result_data, dict):
                    emails_sent = result_data.get('data', {}).get('emailsSent', 0)
                    logger.info(f"Emails Sent: {emails_sent}")
                else:
                    logger.info(f"Response Data: {json.dumps(data, indent=2)}")
            else:
                logger.info(f"Response: {data}")
        else:
            logger.error(f"Error: {results.get('error', 'Unknown error')}")
            logger.error(f"Status Code: {results.get('status_code', 'N/A')}")
        
        logger.info("=" * 80)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Send pending onboarding emails via BuildWiseAI tRPC API'
    )
    parser.add_argument(
        '--url',
        default=os.environ.get('BUILDWISE_API_URL', 'https://buildwiseai.cloud'),
        help='Base URL of the BuildWiseAI application'
    )
    parser.add_argument(
        '--auth-token',
        default=os.environ.get('BUILDWISE_AUTH_TOKEN'),
        help='Authentication token for API requests'
    )
    parser.add_argument(
        '--retry',
        type=int,
        default=3,
        help='Number of retry attempts on failure (default: 3)'
    )
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url:
        logger.error("No URL provided. Use --url or set BUILDWISE_API_URL environment variable.")
        sys.exit(1)
    
    logger.info("Starting onboarding email send process")
    logger.info(f"Target URL: {args.url}")
    
    # Create sender and execute
    sender = OnboardingEmailSender(args.url, args.auth_token)
    results = sender.send_pending_emails(retry_count=args.retry)
    
    # Log results
    sender.log_results(results)
    
    # Exit with appropriate code
    sys.exit(0 if results.get('success') else 1)


if __name__ == '__main__':
    main()
