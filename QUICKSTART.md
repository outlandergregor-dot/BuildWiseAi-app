# Quick Start Guide - BuildWiseAI Onboarding Email Automation

## 🚀 Get Started in 3 Steps

### Step 1: Ensure the BuildWiseAI Application is Running

Before running the script, make sure the BuildWiseAI application is accessible:

1. Open your browser and navigate to: `https://3000-i15h83mk6ch6w41lvgs8n-f6f9bf8a.us2.manus.computer`
2. If you see a "Wake up" button, click it and wait for the application to start
3. Verify the application loads successfully

### Step 2: Run the Script Manually

Test the script to ensure it works:

```bash
cd /home/ubuntu/BuildWiseAi-app
./run_onboarding_emails.sh
```

You should see output like:

```
[INFO] Starting BuildWiseAI Onboarding Email Sender
[INFO] Timestamp: 2026-02-17 19:00:00
[INFO] Executing onboarding email sender...
2026-02-17 19:00:00,123 - INFO - Starting onboarding email send process
2026-02-17 19:00:01,456 - INFO - Successfully sent pending onboarding emails
2026-02-17 19:00:01,457 - INFO - Emails Sent: 5
```

### Step 3: Set Up Automated Hourly Execution

Schedule the script to run automatically every hour:

```bash
# Open crontab editor
crontab -e

# Add this line (copy and paste):
0 * * * * /home/ubuntu/BuildWiseAi-app/run_onboarding_emails.sh >> /home/ubuntu/BuildWiseAi-app/cron.log 2>&1

# Save and exit (Ctrl+X, then Y, then Enter in nano)
```

**That's it!** The script will now run automatically every hour.

---

## 📊 Monitor Execution

### View Recent Activity

```bash
tail -n 50 /home/ubuntu/BuildWiseAi-app/onboarding_emails.log
```

### Watch Real-Time Execution

```bash
tail -f /home/ubuntu/BuildWiseAi-app/onboarding_emails.log
```

### Check Cron Job Status

```bash
# List active cron jobs
crontab -l

# View cron execution log
tail -n 50 /home/ubuntu/BuildWiseAi-app/cron.log
```

---

## ⚙️ Configuration Options

### Use Custom URL

```bash
./run_onboarding_emails.sh --url https://your-custom-url.com
```

### Add Authentication Token

```bash
./run_onboarding_emails.sh --auth-token your_token_here
```

### Set Environment Variables (Persistent)

```bash
# Add to ~/.bashrc or ~/.profile
export BUILDWISE_API_URL="https://your-app-url.com"
export BUILDWISE_AUTH_TOKEN="your_token_here"

# Reload configuration
source ~/.bashrc
```

---

## 🔧 Troubleshooting

### Issue: "Service unavailable" or 502/503 errors

**Solution**: The application is asleep. Wake it up by visiting the URL in your browser and clicking "Wake up".

### Issue: "Authentication failed"

**Solution**: Add an authentication token using `--auth-token` or set the `BUILDWISE_AUTH_TOKEN` environment variable.

### Issue: Script doesn't run automatically

**Solution**: 
1. Verify cron job is installed: `crontab -l`
2. Check cron log for errors: `tail /home/ubuntu/BuildWiseAi-app/cron.log`
3. Ensure script is executable: `chmod +x /home/ubuntu/BuildWiseAi-app/run_onboarding_emails.sh`

### Issue: "0 emails sent"

**Explanation**: This is normal when there are no pending onboarding emails. The script will send emails when new users sign up.

---

## 📚 Additional Resources

- **Full Documentation**: See `ONBOARDING_EMAIL_SETUP.md` for comprehensive details
- **Cron Examples**: See `crontab.example` for alternative scheduling options
- **Python Script**: See `send_onboarding_emails.py` for the underlying implementation

---

## 🎯 What This Script Does

The onboarding email automation:

1. **Connects** to the BuildWiseAI tRPC API endpoint
2. **Calls** the `onboardingEmails.sendPendingEmails` mutation
3. **Sends** pending onboarding emails to new users
4. **Logs** the number of emails sent and any errors
5. **Retries** automatically if the request fails (up to 3 times)

This helps improve user activation and retention by ensuring timely delivery of onboarding email sequences.

---

## 💡 Pro Tips

1. **Test First**: Always run the script manually before setting up automation
2. **Monitor Logs**: Check logs regularly during the first few days to ensure everything works
3. **Keep Application Awake**: For production use, ensure the BuildWiseAI application doesn't go to sleep
4. **Adjust Frequency**: If hourly is too frequent, modify the cron schedule (see `crontab.example`)
5. **Set Up Alerts**: Configure email notifications for failures (see full documentation)

---

## 📞 Need Help?

If you encounter issues:

1. Check the log file: `/home/ubuntu/BuildWiseAi-app/onboarding_emails.log`
2. Review the troubleshooting section above
3. Consult the full documentation: `ONBOARDING_EMAIL_SETUP.md`
4. Verify the BuildWiseAI application is running and accessible

---

**Version**: 1.0.0  
**Last Updated**: February 17, 2026
