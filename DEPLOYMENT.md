# Deployment Guide for GitHub Pages

This guide will help you deploy the Placement Tracker frontend to GitHub Pages and connect it to your backend API.

## Prerequisites

1. Backend API deployed (e.g., on Render, Railway, Heroku, etc.)
2. GitHub repository with the code
3. GitHub Pages enabled in repository settings

## Step 1: Deploy Backend API

If you haven't deployed the backend yet, deploy it to one of these platforms:

### Option A: Render (Recommended)

1. Go to [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `cd backend && pip install -r requirements.txt`
5. Set start command: `cd backend && python run.py`
6. Add environment variable: `GITHUB_PAGES_URL` = your GitHub Pages URL (e.g., `https://username.github.io/repository-name`)
7. Note your backend URL (e.g., `https://your-app.onrender.com`)

### Option B: Railway

1. Go to [Railway.app](https://railway.app)
2. Create new project from GitHub
3. Select backend directory
4. Railway will auto-detect Python and deploy
5. Add environment variable: `GITHUB_PAGES_URL`
6. Note your backend URL

## Step 2: Update Backend CORS

The backend CORS is already configured to allow GitHub Pages. If you have a specific GitHub Pages URL, set the `GITHUB_PAGES_URL` environment variable in your backend deployment.

## Step 3: Configure GitHub Actions

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add a new secret:
   - Name: `REACT_APP_API_URL`
   - Value: Your backend API URL (e.g., `https://your-app.onrender.com/api`)

## Step 4: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select **GitHub Actions**
3. Save

## Step 5: Deploy

1. Push your code to the `main` or `master` branch
2. GitHub Actions will automatically:
   - Build the React app with the correct API URL
   - Deploy to GitHub Pages
3. Your site will be available at: `https://username.github.io/repository-name`

## Manual Deployment (Alternative)

If you prefer to deploy manually:

1. **Build the frontend:**

   ```bash
   cd frontend
   npm install
   REACT_APP_API_URL=https://your-backend-url.onrender.com/api npm run build
   ```

2. **Deploy the build folder:**
   - Go to repository **Settings** → **Pages**
   - Select **Deploy from a branch**
   - Choose branch: `gh-pages` or `main`
   - Select folder: `/frontend/build` or `/` (if you move build to root)
   - Save

## Troubleshooting

### Frontend shows "Error fetching companies"

- **Check:** Backend API is accessible (visit `https://your-backend-url.onrender.com/api/companies`)
- **Check:** CORS is configured correctly in backend
- **Check:** `REACT_APP_API_URL` secret is set correctly in GitHub Actions

### CORS errors in browser console

- **Solution:** Add your GitHub Pages URL to backend CORS configuration
- Set `GITHUB_PAGES_URL` environment variable in backend deployment

### Build fails in GitHub Actions

- **Check:** `REACT_APP_API_URL` secret is set
- **Check:** Backend URL is correct (should end with `/api` if your backend serves at root, or just the domain if backend serves at `/api`)

## Testing Locally with Production API

To test the frontend locally with your production backend:

1. Create `.env` file in `frontend/` directory:

   ```
   REACT_APP_API_URL=https://your-backend-url.onrender.com/api
   ```

2. Restart the frontend dev server:
   ```bash
   cd frontend
   npm start
   ```

## Current Configuration

- **Frontend:** Uses `REACT_APP_API_URL` environment variable or defaults to `/api`
- **Backend CORS:** Allows localhost, Render URLs, and GitHub Pages (via regex)
- **GitHub Actions:** Automatically builds and deploys on push to main/master

## Notes

- The database is SQLite and stored on the backend server
- For production, consider migrating to PostgreSQL or another database service
- The backend needs to be running 24/7 for the frontend to work
- Free tiers on Render/Railway may spin down after inactivity
