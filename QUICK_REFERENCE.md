# BuildWiseAI Onboarding Email Automation - Quick Reference

## 🚀 Quick Commands

### Test Manually
```bash
cd /home/ubuntu/BuildWiseAi-app
./run_onboarding_emails.sh
```

### Check Logs
```bash
# View recent entries
tail -n 50 /home/ubuntu/BuildWiseAi-app/onboarding_emails.log

# Monitor in real-time
tail -f /home/ubuntu/BuildWiseAi-app/onboarding_emails.log
```

### Check Cron Status
```bash
# List cron jobs
crontab -l

# View cron execution log
tail -f /home/ubuntu/BuildWiseAi-app/cron.log
```

---

## 📋 Current Status

**Environment**: Manus Sandbox (Development)  
**Status**: ⚠️ Not suitable for automated tasks (hibernates when inactive)  
**Action Required**: Deploy to production hosting

---

## 🎯 Production Deployment (Quick Steps)

### Option 1: Vercel (Recommended - 15 minutes)

1. **Deploy app to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Import from GitHub: `outlandergregor-dot/BuildWiseAi-app`
   - Click "Deploy"

2. **Update automation URL**:
   ```bash
   export BUILDWISE_API_URL="https://your-app.vercel.app"
   ```

3. **Set up cron job** (on persistent server):
   ```bash
   crontab -e
   # Add: 0 * * * * /path/to/run_onboarding_emails.sh >> /path/to/cron.log 2>&1
   ```

### Option 2: Railway (30 minutes)

1. Visit [railway.app](https://railway.app)
2. Deploy from GitHub
3. Update URL and set up cron

### Option 3: VPS (1-2 hours)

See `PRODUCTION_DEPLOYMENT_GUIDE.md` for detailed steps.

---

## 📊 API Endpoint

**URL**: `/api/trpc/onboardingEmails.sendPendingEmails`  
**Method**: POST  
**Payload**: `{}`  
**Response**: 
```json
{
  "result": {
    "data": {
      "emailsSent": 5,
      "errors": [],
      "timestamp": "2026-02-19T18:00:01.456Z"
    }
  }
}
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Required
export BUILDWISE_API_URL="https://your-production-url.com"

# Optional
export BUILDWISE_AUTH_TOKEN="your-token-here"
```

### Cron Schedule Options
```bash
# Every hour (recommended)
0 * * * * /path/to/run_onboarding_emails.sh

# Every 30 minutes
*/30 * * * * /path/to/run_onboarding_emails.sh

# Daily at 9 AM
0 9 * * * /path/to/run_onboarding_emails.sh
```

---

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `send_onboarding_emails.py` | Core automation script |
| `run_onboarding_emails.sh` | Shell wrapper with error handling |
| `wake_and_send.py` | Enhanced version with wake-up logic |
| `PRODUCTION_DEPLOYMENT_GUIDE.md` | Detailed deployment instructions |
| `EXECUTION_REPORT.md` | Test results and analysis |
| `QUICKSTART.md` | Quick setup guide |
| `ONBOARDING_EMAIL_SETUP.md` | Comprehensive documentation |

---

## 🐛 Troubleshooting

### Issue: 502 Bad Gateway
**Cause**: Application is asleep or unreachable  
**Solution**: Deploy to production hosting (no hibernation)

### Issue: Cron not running
**Check**: `crontab -l` and `chmod +x run_onboarding_emails.sh`

### Issue: 0 emails sent
**Cause**: No pending emails (normal behavior)  
**Solution**: Wait for new user signups

---

## 📖 Documentation

- **Quick Start**: `QUICKSTART.md`
- **Production Guide**: `PRODUCTION_DEPLOYMENT_GUIDE.md`
- **Execution Report**: `EXECUTION_REPORT.md`
- **Full Documentation**: `ONBOARDING_EMAIL_SETUP.md`

---

## ✅ Next Steps

1. [ ] Deploy BuildWiseAI to production hosting
2. [ ] Update automation script URL
3. [ ] Set up cron job on persistent server
4. [ ] Monitor logs for first 24 hours
5. [ ] Verify email delivery

---

**Last Updated**: February 19, 2026  
**Version**: 1.0  
**Status**: Ready for Production
