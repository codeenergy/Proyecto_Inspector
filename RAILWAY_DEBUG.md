# 🔧 Railway Deployment Debugging Guide

## Current Status
- Railway URL: `https://proyectoinspector-production.up.railway.app`
- Status: ❌ **502 Error - Application failed to respond**

---

## 🔍 Steps to Debug Railway Deployment

### 1. Check Railway Deployment Logs

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Open your `proyectoinspector-production` project
3. Click on the service
4. Go to **"Deployments"** tab
5. Click on the latest deployment
6. Check the **"Build Logs"** and **"Deploy Logs"**

**Look for:**
- ❌ Errors during `pip install`
- ❌ Errors during database initialization
- ❌ Python import errors
- ❌ Port binding errors
- ✅ "Uvicorn running on..." message

### 2. Verify Environment Variables

Railway needs these environment variables to be set:

1. In Railway Dashboard → Your Service → **"Variables"** tab
2. Add these variables:

```env
ENVIRONMENT=production
GEMINI_API_KEY=your-actual-gemini-api-key-here
CORS_ORIGINS=https://proyecto-inspector.vercel.app
DATABASE_URL=sqlite:///./inspector.db
LOG_LEVEL=INFO
HEADLESS_BROWSER=true
```

**Critical:** `GEMINI_API_KEY` must be set or the app may crash!

### 3. Check Railway Service Configuration

In Railway Dashboard:
1. Go to **Settings** tab
2. Verify:
   - ✅ **Root Directory**: Should be `/backend` or empty
   - ✅ **Start Command**: Should be auto-detected from `Procfile` or `railway.json`
   - ✅ **Port**: Railway auto-assigns PORT environment variable

### 4. Force Redeploy

Sometimes Railway needs a manual redeploy:
1. In Railway Dashboard → Deployments
2. Click **"⋮"** menu on latest deployment
3. Select **"Redeploy"**

### 5. Check if Port is Correctly Configured

The backend code reads `PORT` from environment:
```python
port = int(os.getenv("PORT", settings.API_PORT))
```

Railway should automatically set `PORT`. Check logs for:
```
INFO: Uvicorn running on http://0.0.0.0:XXXX
```

---

## 🐛 Common Issues and Fixes

### Issue: "ModuleNotFoundError" in logs
**Cause:** Dependencies not installed correctly
**Fix:**
1. Verify `requirements-minimal.txt` exists in `backend/` folder
2. Check build logs show: `Successfully installed fastapi uvicorn...`
3. Try redeploying

### Issue: "GEMINI_API_KEY is required" error
**Cause:** Environment variable not set
**Fix:**
1. Add `GEMINI_API_KEY` in Railway Variables
2. Redeploy after adding

### Issue: Application starts but immediately crashes
**Cause:** Database initialization error or import error
**Fix:**
1. Check deploy logs for Python traceback
2. Look for file `inspector.db` creation message
3. Ensure `start.sh` has execute permissions

### Issue: "Address already in use"
**Cause:** Port conflict (shouldn't happen on Railway)
**Fix:** Railway handles this automatically, redeploy

---

## 📋 Deployment Checklist

- [ ] Repository connected to Railway
- [ ] Root directory set to `backend/` (or Railway auto-detects it)
- [ ] Environment variables configured (at minimum: `GEMINI_API_KEY`)
- [ ] Latest deploy shows "Success" status
- [ ] Build logs show "Successfully installed..." for all packages
- [ ] Deploy logs show "Uvicorn running on..."
- [ ] No error traces in logs

---

## 🚨 Alternative: Test Locally First

Before debugging Railway, test the minimal deployment locally:

```bash
cd backend

# Install minimal requirements
pip install -r requirements-minimal.txt

# Set environment variables
export ENVIRONMENT=production
export PORT=8000
export GEMINI_API_KEY=your-key-here

# Initialize database
python init_database.py

# Start server
python -m api.server
```

Then test: `curl http://localhost:8000/health`

If this works locally but not on Railway, the issue is Railway-specific.

---

## 🔄 Alternative Deployment: Render.com

If Railway continues to fail, try Render.com:

1. Create account at [Render.com](https://render.com)
2. New Web Service
3. Connect GitHub repo: `codeenergy/Proyecto_Inspector`
4. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements-minimal.txt`
   - **Start Command**: `python -m api.server`
   - **Environment Variables**: Add `GEMINI_API_KEY`, `CORS_ORIGINS`, etc.

---

## 📞 Next Steps

1. **Check Railway logs** (most important!)
2. **Verify environment variables** are set
3. **Try manual redeploy**
4. **Test locally** to isolate the issue
5. **Consider Render.com** as alternative

The logs will show the exact error. Without access to Railway dashboard, we can't see what's failing.
