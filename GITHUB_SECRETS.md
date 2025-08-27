# 🔐 GitHub Secrets Quick Reference

## Weather Bot Specific Secrets

Use these **weather-specific** secret names to avoid conflicts with other Caprover deployments:

### Required Secrets:
```
WEATHER_CAPROVER_SERVER = https://captain.yourdomain.com
WEATHER_APP_NAME = bratislava-weather-bot
WEATHER_APP_TOKEN = <app-token-from-caprover-dashboard>
```

### How to Add Secrets:

1. Go to your **GitHub repository**
2. Navigate to **Settings > Secrets and variables > Actions**
3. Click **"New repository secret"**
4. Add each secret with the exact names above

### Secret Sources:

| Secret Name | Where to Get It | Example |
|-------------|-----------------|---------|
| `WEATHER_CAPROVER_SERVER` | Your Caprover URL | `https://captain.mydomain.com` |
| `WEATHER_APP_NAME` | App name in Caprover | `bratislava-weather-bot` |
| `WEATHER_APP_TOKEN` | Apps > [app] > Deployment > Enable App Token | `eyJ0eXAiOiJKV1Q...` |

### Why Weather-Specific Names?

- ✅ **Avoid Conflicts**: Multiple Caprover apps in same GitHub account
- ✅ **Clear Purpose**: Easy to identify which secrets are for weather bot
- ✅ **Organization**: Better secret management
- ✅ **Security**: Separate tokens for different environments

### GitHub Actions Usage:

The workflow automatically uses these secrets:
```yaml
server: '${{ secrets.WEATHER_CAPROVER_SERVER }}'
app: '${{ secrets.WEATHER_APP_NAME }}'
token: '${{ secrets.WEATHER_APP_TOKEN }}'
```

### ⚠️ Important Notes:

1. **Case Sensitive**: Use exact names (all uppercase)
2. **No Spaces**: Ensure no leading/trailing spaces in values
3. **Token Security**: App tokens are sensitive - keep them secret!
4. **URL Format**: Caprover server must include `https://captain.` prefix

### Troubleshooting:

**If deployment fails with "invalid secrets":**
1. Check secret names match exactly (copy-paste recommended)
2. Verify app token is not expired
3. Ensure Caprover server URL is correct format
4. Re-generate app token in Caprover if needed

---

✅ **Ready**: Once these 3 secrets are added, push to `devel` branch to deploy!
