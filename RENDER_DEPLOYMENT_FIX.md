# Render Deployment Database Fix - Step by Step Guide

## Problem

Data added through the GUI appears temporarily but doesn't persist in the database file. This happens because:

1. Render's filesystem is ephemeral (data is lost on restart)
2. Database path might not be using persistent storage
3. Need to configure Render to use persistent disk storage

## Solution Overview

We've updated the code to:

1. Automatically detect cloud environments (Render)
2. Use persistent storage paths when available
3. Fall back gracefully for local development

## Step-by-Step Fix Instructions

### Step 1: Update Your Code (Already Done ✅)

The code has been updated to automatically use persistent storage on Render. The changes are in:

- `backend/app/database.py` - Now detects Render environment and uses persistent paths
- `backend/Dockerfile` - Creates data directory for persistence

### Step 2: Configure Render for Persistent Storage

1. **Go to your Render Dashboard**

   - Visit https://dashboard.render.com
   - Select your backend service

2. **Enable Persistent Disk (IMPORTANT)**

   - Go to **Settings** → **Advanced**
   - Scroll to **Persistent Disk**
   - Click **Enable Persistent Disk**
   - Set disk size to at least **1 GB** (recommended: 2 GB)
   - Mount path: `/opt/render/project/src` (this is the default)
   - Click **Save Changes**

3. **Add Environment Variables**

   - Go to **Environment** tab
   - Add/verify these variables:
     ```
     ADMIN_TOKEN=your-secure-admin-token-here
     GITHUB_PAGES_URL=https://your-username.github.io/your-repo-name
     ```
   - **DO NOT** set `DATABASE_URL` (let it use SQLite with persistent disk)

4. **Redeploy Your Service**
   - Go to **Manual Deploy** → **Deploy latest commit**
   - Or push a new commit to trigger auto-deploy

### Step 3: Verify Database Location

After deployment, check the database location:

1. **Visit the debug endpoint:**

   ```
   https://your-app.onrender.com/api/debug/db-info
   ```

2. **Verify:**
   - `database_file` should show: `/opt/render/project/src/data/placement_tracker.db`
   - `database_exists` should be `true`
   - `database_size_bytes` should increase as you add data

### Step 4: Test Data Persistence

1. **Add a test company** through your deployed frontend
2. **Restart your Render service** (Settings → Restart)
3. **Check if the data persists** after restart
4. **Verify in database** by checking the debug endpoint again

## Alternative: Use PostgreSQL (Recommended for Production)

For better reliability, consider migrating to PostgreSQL:

### Option A: Render PostgreSQL (Free Tier Available)

1. **Create PostgreSQL Database:**

   - In Render Dashboard → **New** → **PostgreSQL**
   - Name: `placement-tracker-db`
   - Plan: Free (or paid for better performance)
   - Note the **Internal Database URL**

2. **Update Backend Service:**

   - Go to your backend service → **Environment**
   - Add variable:
     ```
     DATABASE_URL=postgresql://user:pass@host:5432/dbname
     ```
   - Use the **Internal Database URL** from step 1

3. **Update database.py** (if needed):
   - The code already supports PostgreSQL via `DATABASE_URL`
   - Just set the environment variable and redeploy

### Option B: Keep SQLite with Persistent Disk

If you prefer SQLite (simpler, no separate service):

- Follow Step 2 above to enable persistent disk
- This works fine for small to medium datasets
- Data persists across restarts

## Troubleshooting

### Data Still Not Persisting

1. **Check Persistent Disk is Enabled:**

   - Render Dashboard → Your Service → Settings → Advanced
   - Verify "Persistent Disk" shows as "Enabled"

2. **Check Database Location:**

   - Visit: `https://your-app.onrender.com/api/debug/db-info`
   - Verify path includes `/opt/render/project/src/data/`

3. **Check Render Logs:**

   - Go to **Logs** tab in Render dashboard
   - Look for any database-related errors
   - Check if database file is being created

4. **Verify Environment Variables:**
   - Make sure `DATABASE_URL` is NOT set (unless using PostgreSQL)
   - Let the code auto-detect the path

### Database File Not Found

If `database_exists: false` in debug endpoint:

1. **Check Render Logs** for initialization errors
2. **Verify persistent disk is mounted** correctly
3. **Try manual initialization:**
   - The database should auto-create on first API call
   - Visit: `https://your-app.onrender.com/api/companies`
   - Then check debug endpoint again

### CORS Errors

If frontend can't connect to backend:

1. **Set GITHUB_PAGES_URL** in Render environment variables:

   ```
   GITHUB_PAGES_URL=https://your-username.github.io/your-repo-name
   ```

2. **Verify CORS in backend logs:**
   - Check if requests are being blocked
   - Backend should allow your GitHub Pages URL

## Current Configuration Summary

✅ **Database Path:** Auto-detects Render and uses `/opt/render/project/src/data/placement_tracker.db`
✅ **Persistent Storage:** Requires Render Persistent Disk to be enabled
✅ **Error Handling:** Proper rollback on errors
✅ **Debug Endpoint:** `/api/debug/db-info` to verify database location

## Next Steps After Fix

1. ✅ Enable Persistent Disk on Render
2. ✅ Redeploy your backend service
3. ✅ Test adding data through frontend
4. ✅ Verify data persists after service restart
5. ✅ Check debug endpoint to confirm database location

## Important Notes

- **Persistent Disk is required** for SQLite to work on Render
- **Free tier** includes 1 GB persistent disk (sufficient for most use cases)
- **Data persists** across deployments and restarts when persistent disk is enabled
- **Consider PostgreSQL** for production apps with high traffic
