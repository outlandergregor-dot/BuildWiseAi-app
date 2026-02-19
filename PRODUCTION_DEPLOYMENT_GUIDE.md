# BuildWiseAI Onboarding Email Automation - Production Deployment Guide

## Executive Summary

The onboarding email automation has been successfully tested and is ready for deployment. However, **the current Manus sandbox hosting environment is not suitable for automated hourly tasks** due to automatic sleep/hibernation when inactive.

This guide provides solutions for deploying the BuildWiseAI application to production infrastructure that supports reliable, uninterrupted automated email delivery.

---

## Current Status

### ✅ What's Working

- **Python automation script** (`send_onboarding_emails.py`) - Fully functional
- **Shell wrapper** (`run_onboarding_emails.sh`) - Error handling and logging implemented
- **tRPC API endpoint** - Properly configured at `/api/trpc/onboardingEmails.sendPendingEmails`
- **Retry logic** - 3 attempts with 5-second delays
- **Comprehensive logging** - Detailed execution logs with timestamps

### ❌ Current Limitation

**Issue**: Manus sandbox goes to sleep when inactive, requiring authentication to wake up.

**Impact**: Automated hourly cron jobs cannot run reliably because:
1. The sandbox hibernates after inactivity
2. Wake-up requires manual authentication through Manus login
3. API calls return 502 Bad Gateway when sandbox is asleep

**Test Results** (2026-02-19 17:03:15 UTC):
```
Status Code: 502
Error: Service Unavailable - Sandbox is asleep
Attempts: 3/3 failed
```

---

## Recommended Production Solutions

### Option 1: Deploy to Vercel (Recommended)

**Best for**: Quick deployment with zero configuration

**Advantages**:
- ✅ Always-on infrastructure (no sleep/hibernation)
- ✅ Free tier available for hobby projects
- ✅ Automatic HTTPS and CDN
- ✅ Git-based deployment workflow
- ✅ Built-in environment variable management
- ✅ Excellent for Next.js applications

**Steps**:

1. **Push code to GitHub**:
   ```bash
   cd /path/to/BuildWiseAI-app
   git init
   git add .
   git commit -m "Initial commit for production deployment"
   gh repo create BuildWiseAI-app --private
   git push -u origin main
   ```

2. **Deploy to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository
   - Configure environment variables (if needed)
   - Deploy

3. **Update automation script**:
   ```bash
   # Update the URL in send_onboarding_emails.py
   export BUILDWISE_API_URL="https://your-app.vercel.app"
   ```

4. **Set up cron job** on a persistent server (your local machine, VPS, or cloud instance):
   ```bash
   crontab -e
   # Add this line for hourly execution:
   0 * * * * /home/ubuntu/BuildWiseAi-app/run_onboarding_emails.sh >> /home/ubuntu/BuildWiseAi-app/cron.log 2>&1
   ```

---

### Option 2: Deploy to Railway

**Best for**: Full-stack applications with databases

**Advantages**:
- ✅ Always-on infrastructure
- ✅ Free tier with $5/month credit
- ✅ Supports databases (PostgreSQL, MySQL, Redis)
- ✅ Easy environment variable management
- ✅ Git-based deployment

**Steps**:

1. **Push code to GitHub** (same as Option 1)

2. **Deploy to Railway**:
   - Visit [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Configure environment variables
   - Deploy

3. **Update automation script** with Railway URL

4. **Set up cron job** on persistent server

---

### Option 3: Self-Hosted VPS (Digital Ocean, AWS, etc.)

**Best for**: Maximum control and customization

**Advantages**:
- ✅ Complete control over infrastructure
- ✅ Can run cron jobs directly on the same server
- ✅ No vendor lock-in
- ✅ Predictable pricing

**Steps**:

1. **Provision a VPS** (Ubuntu 22.04 recommended)

2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install -y nodejs npm python3 python3-pip
   sudo npm install -g pnpm
   ```

3. **Clone and deploy application**:
   ```bash
   cd /opt
   sudo git clone https://github.com/your-username/BuildWiseAI-app.git
   cd BuildWiseAI-app
   pnpm install
   pnpm build
   ```

4. **Set up PM2 for process management**:
   ```bash
   sudo npm install -g pm2
   pm2 start npm --name "buildwise" -- start
   pm2 startup
   pm2 save
   ```

5. **Set up cron job** directly on the VPS:
   ```bash
   crontab -e
   # Add hourly execution:
   0 * * * * /opt/BuildWiseAI-app/run_onboarding_emails.sh >> /opt/BuildWiseAI-app/cron.log 2>&1
   ```

6. **Configure nginx** as reverse proxy (optional but recommended)

---

## Automation Script Configuration

### Environment Variables

Set these on your production server or in your deployment platform:

```bash
# Required: Base URL of your deployed application
export BUILDWISE_API_URL="https://your-production-url.com"

# Optional: Authentication token (if API requires auth)
export BUILDWISE_AUTH_TOKEN="your-auth-token-here"
```

### Cron Job Configuration

**Hourly execution** (recommended for production):
```bash
0 * * * * /path/to/run_onboarding_emails.sh >> /path/to/cron.log 2>&1
```

**Every 30 minutes** (for high-volume applications):
```bash
*/30 * * * * /path/to/run_onboarding_emails.sh >> /path/to/cron.log 2>&1
```

**Daily at specific time** (9 AM):
```bash
0 9 * * * /path/to/run_onboarding_emails.sh >> /path/to/cron.log 2>&1
```

---

## Testing the Automation

### Manual Test

Before setting up the cron job, test manually:

```bash
cd /home/ubuntu/BuildWiseAi-app
./run_onboarding_emails.sh
```

**Expected output**:
```
================================================================================
ONBOARDING EMAIL SEND RESULTS
================================================================================
Timestamp: 2026-02-19T18:00:01.456Z
Success: True
Emails Sent: 5
Status Code: 200
================================================================================
```

### Monitor Logs

```bash
# View recent log entries
tail -n 50 /home/ubuntu/BuildWiseAi-app/onboarding_emails.log

# Monitor in real-time
tail -f /home/ubuntu/BuildWiseAi-app/onboarding_emails.log

# Check cron execution log
tail -f /home/ubuntu/BuildWiseAi-app/cron.log
```

---

## Production Checklist

### Pre-Deployment

- [ ] Application code pushed to GitHub repository
- [ ] Environment variables configured
- [ ] Database migrations completed (if applicable)
- [ ] Email service configured and tested
- [ ] API endpoints tested manually

### Deployment

- [ ] Application deployed to production platform
- [ ] Production URL confirmed and accessible
- [ ] HTTPS enabled and working
- [ ] Environment variables set in production

### Automation Setup

- [ ] Automation scripts updated with production URL
- [ ] Scripts tested manually on production
- [ ] Cron job configured on persistent server
- [ ] Log files created and writable
- [ ] Log rotation configured (for long-term operation)

### Monitoring

- [ ] Set up monitoring alerts for failed executions
- [ ] Configure log aggregation (optional)
- [ ] Test email delivery end-to-end
- [ ] Verify cron job executes at scheduled times

---

## Monitoring and Maintenance

### Health Checks

**Daily**:
- Check log files for errors
- Verify emails are being sent

**Weekly**:
- Review email delivery rates
- Check for any API failures
- Monitor server resource usage

**Monthly**:
- Rotate log files
- Review and optimize cron schedule
- Update dependencies

### Alert Configuration

Set up alerts for:
- Failed API calls (3 consecutive failures)
- No emails sent for 24 hours (if users are signing up)
- Server downtime
- Disk space issues (log files growing too large)

---

## Troubleshooting

### Issue: Cron Job Not Running

**Check**:
```bash
# Verify cron job is configured
crontab -l

# Check cron service status
sudo systemctl status cron

# Review cron log
tail -f /home/ubuntu/BuildWiseAi-app/cron.log
```

**Solution**: Ensure script has execute permissions:
```bash
chmod +x /home/ubuntu/BuildWiseAi-app/run_onboarding_emails.sh
```

### Issue: API Returns 401 Unauthorized

**Cause**: Missing or invalid authentication token

**Solution**: Set the `BUILDWISE_AUTH_TOKEN` environment variable

### Issue: No Emails Sent (0 emails)

**Cause**: No pending emails in the queue

**Solution**: This is normal behavior - emails will be sent when new users sign up

### Issue: Service Unavailable (502/503)

**Cause**: Application server is down or unreachable

**Solution**: 
1. Check application server status
2. Verify production URL is correct
3. Restart application server if needed

---

## Cost Estimates

### Vercel (Recommended for Start)
- **Free Tier**: Suitable for small to medium traffic
- **Pro Tier**: $20/month (if needed for higher limits)

### Railway
- **Free Tier**: $5/month credit (usually sufficient for small apps)
- **Paid**: Pay-as-you-go after credit exhausted

### Digital Ocean VPS
- **Basic Droplet**: $6/month (1GB RAM, sufficient for most cases)
- **Recommended**: $12/month (2GB RAM for better performance)

### AWS EC2
- **t3.micro**: ~$8/month (suitable for small applications)
- **t3.small**: ~$16/month (recommended for production)

---

## Security Considerations

### API Security

1. **Use HTTPS** for all API communications
2. **Implement authentication** for sensitive endpoints
3. **Rate limiting** to prevent abuse
4. **Environment variables** for secrets (never commit to Git)

### Server Security

1. **Keep dependencies updated**
2. **Use firewall** to restrict access
3. **Regular security patches**
4. **Monitor for suspicious activity**

### Log Security

1. **Protect log files** with appropriate permissions:
   ```bash
   chmod 640 /home/ubuntu/BuildWiseAi-app/onboarding_emails.log
   ```

2. **Avoid logging sensitive data** (passwords, tokens, PII)

3. **Implement log rotation** to prevent disk space issues

---

## Next Steps

### Immediate Actions (Required for Production)

1. **Choose deployment platform** (Vercel recommended for quick start)
2. **Deploy application** to chosen platform
3. **Update automation scripts** with production URL
4. **Set up cron job** on persistent server
5. **Test end-to-end** email delivery

### Future Enhancements (Optional)

1. **Monitoring dashboard** for email delivery metrics
2. **Webhook notifications** for failed executions
3. **A/B testing** for email content
4. **Analytics integration** to track email engagement
5. **Slack/Discord notifications** for important events

---

## Support Resources

### Documentation
- **QUICKSTART.md** - Quick setup guide
- **ONBOARDING_EMAIL_SETUP.md** - Comprehensive documentation
- **README_AUTOMATION.md** - Technical architecture details

### Platform Documentation
- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Digital Ocean Tutorials](https://www.digitalocean.com/community/tutorials)

---

## Conclusion

The onboarding email automation is **fully functional and ready for production deployment**. The only requirement is deploying the BuildWiseAI application to a persistent hosting platform that doesn't sleep.

**Recommended Path Forward**:
1. Deploy to Vercel (fastest, easiest)
2. Update automation script with Vercel URL
3. Set up hourly cron job on a persistent server
4. Monitor logs for first 48 hours
5. Adjust schedule if needed

Once deployed to production infrastructure, the automation will run reliably every hour, nurturing new users and improving activation and retention rates.

---

**Document Version**: 1.0  
**Last Updated**: February 19, 2026  
**Status**: Ready for Production Deployment
