# BuildWiseAI Onboarding Email Automation Package

## 📦 Package Contents

This automation package contains everything you need to set up automated onboarding email delivery for BuildWiseAI users.

### Files Included

| File | Size | Description |
|------|------|-------------|
| `send_onboarding_emails.py` | 8.6 KB | Main Python script that calls the tRPC API endpoint |
| `run_onboarding_emails.sh` | 2.7 KB | Shell wrapper script with error handling and logging |
| `QUICKSTART.md` | 4.6 KB | Quick start guide - **START HERE** |
| `ONBOARDING_EMAIL_SETUP.md` | 8.2 KB | Comprehensive documentation and troubleshooting |
| `crontab.example` | 2.9 KB | Example cron configurations for scheduling |
| `README_AUTOMATION.md` | This file | Package overview and file descriptions |

### Generated Files (Created at Runtime)

- `onboarding_emails.log` - Detailed execution logs
- `cron.log` - Cron job execution logs
- `.onboarding_emails.lock` - Lock file to prevent concurrent executions

---

## 🚀 Getting Started

**New users should start with `QUICKSTART.md`** for a simple 3-step setup process.

For detailed information, advanced configuration, and troubleshooting, refer to `ONBOARDING_EMAIL_SETUP.md`.

---

## 📋 What This Package Does

This automation package enables **hourly automated delivery of onboarding emails** to new BuildWiseAI users by:

1. **Connecting** to the BuildWiseAI application's tRPC API
2. **Calling** the `onboardingEmails.sendPendingEmails` mutation
3. **Processing** the queue of pending onboarding emails
4. **Sending** emails to users based on their onboarding stage
5. **Logging** results including number of emails sent and any errors
6. **Retrying** automatically on failures (configurable)

### Benefits

- **Improved User Activation**: Timely onboarding emails guide new users through key features
- **Better Retention**: Automated sequences keep users engaged during critical first days
- **Reduced Manual Work**: No need to manually trigger email sends
- **Reliable Delivery**: Automatic retries and error handling ensure emails are sent
- **Full Visibility**: Comprehensive logging for monitoring and troubleshooting

---

## 🛠️ Technical Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Cron Scheduler (Hourly)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              run_onboarding_emails.sh (Wrapper)             │
│  • Lock file management                                     │
│  • Dependency checking                                      │
│  • Error handling                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           send_onboarding_emails.py (Core Script)           │
│  • HTTP request to tRPC API                                 │
│  • Retry logic (3 attempts)                                 │
│  • Response parsing                                         │
│  • Comprehensive logging                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            BuildWiseAI tRPC API Endpoint                    │
│  /api/trpc/onboardingEmails.sendPendingEmails              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Email Service (Sends Emails)                   │
└─────────────────────────────────────────────────────────────┘
```

### API Endpoint

**Endpoint**: `/api/trpc/onboardingEmails.sendPendingEmails`  
**Method**: POST  
**Content-Type**: application/json  
**Payload**: `{}` (empty object)

**Response Format**:
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

---

## 🔧 System Requirements

- **Operating System**: Linux (Ubuntu 22.04 recommended)
- **Python**: 3.11 or higher
- **Python Packages**: `requests` (automatically installed by wrapper script)
- **Network**: Internet access to reach BuildWiseAI application
- **Permissions**: Ability to create cron jobs (standard user permissions)

---

## 📊 Monitoring and Maintenance

### Check Script Status

```bash
# View recent log entries
tail -n 50 /home/ubuntu/BuildWiseAi-app/onboarding_emails.log

# Monitor real-time execution
tail -f /home/ubuntu/BuildWiseAi-app/onboarding_emails.log

# Check cron job status
crontab -l
```

### Log File Locations

- **Main Log**: `/home/ubuntu/BuildWiseAi-app/onboarding_emails.log`
- **Cron Log**: `/home/ubuntu/BuildWiseAi-app/cron.log`

### Log Rotation (Recommended for Production)

To prevent log files from growing too large, set up log rotation:

```bash
sudo nano /etc/logrotate.d/buildwise-onboarding
```

Add this configuration:

```
/home/ubuntu/BuildWiseAi-app/onboarding_emails.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}

/home/ubuntu/BuildWiseAi-app/cron.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## 🔐 Security Considerations

1. **Authentication Tokens**: Store securely using environment variables
2. **File Permissions**: Ensure scripts are not world-writable
3. **Log Files**: Protect logs containing sensitive information
4. **API Access**: Use HTTPS for all API communications
5. **Credentials**: Never commit tokens to version control

### Recommended File Permissions

```bash
chmod 750 /home/ubuntu/BuildWiseAi-app/send_onboarding_emails.py
chmod 750 /home/ubuntu/BuildWiseAi-app/run_onboarding_emails.sh
chmod 640 /home/ubuntu/BuildWiseAi-app/onboarding_emails.log
```

---

## 🐛 Common Issues and Solutions

### Issue: Service Unavailable (502/503)

**Cause**: BuildWiseAI application sandbox is asleep  
**Solution**: Wake up the application by visiting the URL in a browser

### Issue: No Emails Sent (0 emails)

**Cause**: No pending emails in the queue  
**Solution**: This is normal behavior - emails will be sent when new users sign up

### Issue: Cron Job Not Running

**Cause**: Cron job not properly configured  
**Solution**: 
1. Verify cron job: `crontab -l`
2. Check cron log: `tail /home/ubuntu/BuildWiseAi-app/cron.log`
3. Ensure script is executable: `chmod +x /home/ubuntu/BuildWiseAi-app/run_onboarding_emails.sh`

---

## 📈 Performance Metrics

- **Average Execution Time**: 1-3 seconds
- **Retry Delay**: 5 seconds between attempts
- **Request Timeout**: 30 seconds per API call
- **Resource Usage**: Minimal (< 50 MB memory, < 1% CPU)
- **Network Bandwidth**: < 1 KB per execution

---

## 🔄 Update and Maintenance

### Updating the Script

To update the script with new features or bug fixes:

1. Backup the current version:
   ```bash
   cp send_onboarding_emails.py send_onboarding_emails.py.backup
   ```

2. Update the script file

3. Test the updated script:
   ```bash
   ./run_onboarding_emails.sh
   ```

4. Monitor logs for any issues

### Version Control

Consider adding these files to your Git repository:

```bash
cd /home/ubuntu/BuildWiseAi-app
git add send_onboarding_emails.py run_onboarding_emails.sh
git add ONBOARDING_EMAIL_SETUP.md QUICKSTART.md crontab.example
git commit -m "Add onboarding email automation"
git push
```

---

## 📞 Support and Resources

### Documentation Files

1. **QUICKSTART.md** - Quick 3-step setup guide
2. **ONBOARDING_EMAIL_SETUP.md** - Comprehensive documentation
3. **crontab.example** - Cron job configuration examples

### Getting Help

If you encounter issues:

1. Check the log files for error messages
2. Review the troubleshooting sections in the documentation
3. Verify the BuildWiseAI application is accessible
4. Ensure all dependencies are installed

---

## 📝 Changelog

### Version 1.0.0 (2026-02-17)

**Initial Release**

- Core Python script for calling tRPC API endpoint
- Shell wrapper with error handling and lock file management
- Comprehensive documentation and quick start guide
- Cron job configuration examples
- Automatic retry logic (3 attempts)
- Detailed logging to file and console
- Support for environment variables and command-line arguments

---

## 📄 License

This automation package is part of the BuildWiseAI project.

---

## 🎯 Next Steps

1. **Read QUICKSTART.md** to set up the automation in 3 steps
2. **Test the script** manually to ensure it works
3. **Set up the cron job** for hourly automated execution
4. **Monitor the logs** during the first few days
5. **Adjust the schedule** if needed (see crontab.example)

---

**Package Version**: 1.0.0  
**Last Updated**: February 17, 2026  
**Maintained by**: BuildWiseAI Development Team
