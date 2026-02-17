# BuildWiseAI Onboarding Email Automation

## Overview

This automation script sends pending onboarding emails to new BuildWiseAI users through the tRPC API endpoint. The script is designed to run automatically on an hourly schedule to ensure timely delivery of onboarding email sequences, which improves user activation and retention.

## Features

- **Automated Email Delivery**: Calls the `trpc.onboardingEmails.sendPendingEmails.mutate()` endpoint
- **Retry Logic**: Automatically retries failed requests up to 3 times (configurable)
- **Comprehensive Logging**: Logs all operations to both console and file
- **Error Handling**: Gracefully handles timeouts, authentication failures, and service unavailability
- **Flexible Configuration**: Supports environment variables and command-line arguments

## Prerequisites

- Python 3.11 or higher
- `requests` library (install with: `sudo pip3 install requests`)
- Access to the BuildWiseAI application API
- Optional: Authentication token for API requests

## Installation

1. **Install Dependencies**:
   ```bash
   sudo pip3 install requests
   ```

2. **Make Script Executable**:
   ```bash
   chmod +x /home/ubuntu/BuildWiseAi-app/send_onboarding_emails.py
   ```

## Usage

### Basic Usage

Run the script with default settings:

```bash
python3 /home/ubuntu/BuildWiseAi-app/send_onboarding_emails.py
```

### Advanced Usage

Specify custom URL and authentication token:

```bash
python3 /home/ubuntu/BuildWiseAi-app/send_onboarding_emails.py \
  --url https://your-buildwise-app.com \
  --auth-token your_auth_token_here \
  --retry 5
```

### Environment Variables

Set environment variables for persistent configuration:

```bash
export BUILDWISE_API_URL="https://3000-i15h83mk6ch6w41lvgs8n-f6f9bf8a.us2.manus.computer"
export BUILDWISE_AUTH_TOKEN="your_auth_token_here"
```

Then run the script:

```bash
python3 /home/ubuntu/BuildWiseAi-app/send_onboarding_emails.py
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | Base URL of the BuildWiseAI application | `BUILDWISE_API_URL` env var or default sandbox URL |
| `--auth-token` | Authentication token for API requests | `BUILDWISE_AUTH_TOKEN` env var or none |
| `--retry` | Number of retry attempts on failure | 3 |

## Scheduling Automated Execution

### Option 1: Cron Job (Recommended for Linux/Unix)

Add a cron job to run the script every hour:

```bash
# Edit crontab
crontab -e

# Add this line to run every hour at minute 0
0 * * * * /usr/bin/python3 /home/ubuntu/BuildWiseAi-app/send_onboarding_emails.py >> /home/ubuntu/BuildWiseAi-app/cron.log 2>&1
```

### Option 2: Systemd Timer (Linux)

Create a systemd service and timer for more robust scheduling:

**Service file** (`/etc/systemd/system/buildwise-onboarding.service`):
```ini
[Unit]
Description=BuildWiseAI Onboarding Email Sender
After=network.target

[Service]
Type=oneshot
User=ubuntu
WorkingDirectory=/home/ubuntu/BuildWiseAi-app
ExecStart=/usr/bin/python3 /home/ubuntu/BuildWiseAi-app/send_onboarding_emails.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Timer file** (`/etc/systemd/system/buildwise-onboarding.timer`):
```ini
[Unit]
Description=Run BuildWiseAI Onboarding Email Sender hourly
Requires=buildwise-onboarding.service

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start the timer:
```bash
sudo systemctl daemon-reload
sudo systemctl enable buildwise-onboarding.timer
sudo systemctl start buildwise-onboarding.timer
```

### Option 3: Manus Schedule Tool

Use the Manus scheduling tool to run the script at regular intervals:

```python
# This would be configured through the Manus interface
schedule.every().hour.do(run_onboarding_emails)
```

## Logging

The script logs all operations to two locations:

1. **Console Output**: Real-time logging to stdout
2. **Log File**: `/home/ubuntu/BuildWiseAi-app/onboarding_emails.log`

### Log Format

```
2026-02-17 19:00:00,123 - INFO - Starting onboarding email send process
2026-02-17 19:00:00,124 - INFO - Target URL: https://3000-i15h83mk6ch6w41lvgs8n-f6f9bf8a.us2.manus.computer
2026-02-17 19:00:00,125 - INFO - Calling tRPC endpoint: https://3000-i15h83mk6ch6w41lvgs8n-f6f9bf8a.us2.manus.computer/api/trpc/onboardingEmails.sendPendingEmails
2026-02-17 19:00:01,456 - INFO - Successfully sent pending onboarding emails
2026-02-17 19:00:01,457 - INFO - ================================================================================
2026-02-17 19:00:01,457 - INFO - ONBOARDING EMAIL SEND RESULTS
2026-02-17 19:00:01,457 - INFO - ================================================================================
2026-02-17 19:00:01,457 - INFO - Timestamp: 2026-02-17T19:00:01.456789
2026-02-17 19:00:01,457 - INFO - Success: True
2026-02-17 19:00:01,457 - INFO - Emails Sent: 5
2026-02-17 19:00:01,457 - INFO - ================================================================================
```

## Monitoring and Troubleshooting

### Check Recent Logs

```bash
tail -n 50 /home/ubuntu/BuildWiseAi-app/onboarding_emails.log
```

### Monitor Real-Time Execution

```bash
tail -f /home/ubuntu/BuildWiseAi-app/onboarding_emails.log
```

### Common Issues

#### 1. Service Unavailable (503)

**Symptom**: Script logs "Service unavailable. Application may be asleep."

**Solution**: The BuildWiseAI sandbox is in sleep mode. Wake it up by:
- Visiting the application URL in a browser
- Clicking the "Wake up" button
- Waiting for the application to fully start

#### 2. Authentication Failed (401)

**Symptom**: Script logs "Authentication failed. Please check your auth token."

**Solution**: 
- Verify your authentication token is correct
- Ensure the token hasn't expired
- Check that the token has appropriate permissions

#### 3. Connection Timeout

**Symptom**: Script logs "Request timeout"

**Solution**:
- Check network connectivity
- Verify the application URL is correct
- Ensure the application is running and accessible

#### 4. No Emails Sent

**Symptom**: Script succeeds but reports 0 emails sent

**Explanation**: This is normal behavior when there are no pending onboarding emails in the queue. The script will continue to run on schedule and send emails when new users sign up.

## API Response Format

The tRPC endpoint returns a response in the following format:

```json
{
  "result": {
    "data": {
      "emailsSent": 5,
      "errors": [],
      "timestamp": "2026-02-17T19:00:01.456Z"
    }
  }
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - emails sent successfully |
| 1 | Failure - error occurred during execution |

## Security Considerations

1. **Authentication Tokens**: Store authentication tokens securely using environment variables, not in code
2. **Log Files**: Ensure log files have appropriate permissions (readable only by authorized users)
3. **API Access**: Restrict API access to authorized IP addresses or networks when possible
4. **Credentials**: Never commit authentication tokens or credentials to version control

## Performance Notes

- **Execution Time**: Typically completes in 1-3 seconds
- **Retry Delay**: 5 seconds between retry attempts
- **Timeout**: 30 seconds per API request
- **Resource Usage**: Minimal CPU and memory footprint

## Integration with BuildWiseAI

This script integrates with the BuildWiseAI onboarding email system by:

1. Calling the tRPC mutation endpoint: `onboardingEmails.sendPendingEmails`
2. Processing the queue of pending onboarding emails
3. Sending emails to users based on their onboarding stage
4. Tracking email delivery status and errors

The onboarding email sequences are designed to:
- Welcome new users to BuildWiseAI
- Guide users through key features
- Encourage activation and engagement
- Improve user retention rates

## Support and Maintenance

For issues or questions:
1. Check the log file for detailed error messages
2. Review the troubleshooting section above
3. Verify the BuildWiseAI application is running and accessible
4. Contact the BuildWiseAI development team for API-specific issues

## Version History

- **v1.0.0** (2026-02-17): Initial release
  - Basic email sending functionality
  - Retry logic and error handling
  - Comprehensive logging
  - Command-line and environment variable configuration
