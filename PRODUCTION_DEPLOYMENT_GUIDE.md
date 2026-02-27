# SafePulse Production Deployment Guide

## Overview
SafePulse has been refactored for production-ready deployment with **Vercel** (frontend), **Render** (backend), and **Supabase** (database/auth).

## ✅ What's Been Done

### Frontend (Vercel)
- ✅ Created `.env.local` (development) with `VITE_API_URL=http://localhost:8000`
- ✅ Created `.env.production` (production) with empty `VITE_API_URL` (set via Vercel)
- ✅ Removed all hardcoded `localhost:8000` fallbacks
- ✅ All API calls now use `import.meta.env.VITE_API_URL ?? ''`
- ✅ Dev warning added if VITE_API_URL not set
- ✅ Files updated:
  - `vite.config.ts`
  - `src/services/api.ts`
  - `src/services/authService.ts`
  - `src/components/MapContainer.tsx`
  - `src/pages/AuthorityDashboard.tsx`

### Backend (Render)
- ✅ Created environment-based `backend/.env` with `FRONTEND_URL=http://localhost:5173`
- ✅ Updated CORS to dynamically read `FRONTEND_URL` from environment
- ✅ Updated email templates to use dynamic `FRONTEND_URL` instead of hardcoded localhost
- ✅ Added Supabase configuration to settings
- ✅ Files updated:
  - `backend/app/config/settings.py` - Dynamic CORS configuration
  - `backend/app/utils/email.py` - Dynamic email links

### Verification
- ✅ No hardcoded `localhost` URLs in production code (only in env defaults)
- ✅ No Cloudflare URLs in codebase (only used temporarily in dev)
- ✅ All configuration via environment variables
- ✅ Commit pushed: `0e6ad72`

---

## 📋 Next Steps for Production Deployment

### 1. Vercel Deployment (Frontend)

1. **Connect GitHub repository to Vercel**
   - GitHub repo: `github-sujal/Sujal-Sule/production-code`
   - Set root directory: (default - root)
   - Build command: `npm install && npm run build`
   - Output directory: `dist`

2. **Set Environment Variables in Vercel Dashboard**
   ```
   VITE_API_URL = https://your-render-backend-url.onrender.com
   ```
   
   Example: `https://safepulse-backend.onrender.com`

3. **Deploy** - Vercel will automatically pick up these environment variables

### 2. Render Deployment (Backend)

1. **Set Environment Variables in Render Dashboard**
   ```
   APP_ENV = production
   FRONTEND_URL = https://your-vercel-domain.vercel.app
   CORS_ORIGINS = (leave empty - will be built from FRONTEND_URL)
   SUPABASE_URL = https://avplsonmppbsjkpsqxsw.supabase.co
   SUPABASE_SERVICE_ROLE_KEY = your_service_role_key
   DATABASE_URL = (your Supabase connection string)
   (other env vars as needed)
   ```

2. **Deploy** - Render will use these environment variables at runtime

### 3. Verify Everything Works

**Local Development (Before pushing to production)**
```bash
# Terminal 1 - Frontend
npm run dev
# Should use http://localhost:8000 from .env.local

# Terminal 2 - Backend  
cd backend
python -m uvicorn app.main:app --reload
# Should read FRONTEND_URL=http://localhost:5173 from backend/.env
```

**Production Verification**
- [ ] Frontend loads from Vercel domain
- [ ] API calls go to Render backend URL
- [ ] CORS allows requests from Vercel domain
- [ ] Email links point to correct domain
- [ ] WebSocket connections work
- [ ] No console errors about mixed content (http vs https)

---

## 🔐 Security Checklist

- [x] No hardcoded localhost URLs in code
- [x] Frontend uses ANON_KEY only (safe to commit)
- [x] Backend uses SERVICE_ROLE_KEY (never commit, only in env vars)
- [x] Credentials in .gitignore
- [x] CORS properly restricted by environment
- [x] Email links use dynamic URLs

---

## 📊 Environment Variables Reference

### Frontend (.env.local for dev, .env.production for prod)
```
VITE_API_URL=http://localhost:8000           # (dev) or set in Vercel (prod)
VITE_SUPABASE_URL=...
VITE_SUPABASE_ANON_KEY=...
VITE_FIREBASE_API_KEY=...
... (other third-party keys)
```

### Backend (backend/.env for dev, Render dashboard for prod)
```
FRONTEND_URL=http://localhost:5173           # (dev) or Vercel domain (prod)
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
DATABASE_URL=...
... (other config)
```

---

## 🚀 Deployment Flow

```
1. Developer makes code changes locally
   ↓
2. Commit and push to GitHub
   ↓
3. Vercel automatically builds & deploys frontend
   (uses VITE_API_URL from Vercel dashboard → points to Render)
   ↓
4. Render automatically rebuilds & deploys backend
   (uses FRONTEND_URL from Render dashboard → points to Vercel)
   ↓
5. Everything communicates across domains seamlessly
```

---

## 📌 Important Notes

1. **Vite Development Proxy** - In local dev, Vite proxies API calls to localhost:8000
   - This is handled by vite.config.ts
   - In production, frontend directly calls the Render API URL

2. **Environment Variable Precedence**
   - `.env.local` (dev) only used locally, never committed
   - `.env.production` used during production build
   - Vercel/Render dashboard env vars override file-based ones

3. **CORS Configuration**
   - Backend automatically allows:
     - localhost dev origins (dev only)
     - FRONTEND_URL from environment (prod)
   - No hardcoding of production domains

4. **Email Links**
   - Automatically use FRONTEND_URL from environment
   - Dev emails → http://localhost:5173
   - Prod emails → https://your-vercel-domain.vercel.app

---

## ❓ Troubleshooting

**API calls return CORS error**
- Check FRONTEND_URL in Render dashboard
- Ensure it matches your Vercel domain exactly
- Check browser Network tab to see actual request URL

**Email links point to wrong domain**
- Verify FRONTEND_URL in Render environment variables
- Restart Render service after changing env vars

**API_URL undefined in frontend**
- Ensure VITE_API_URL is set in Vercel dashboard for production
- For local dev, ensure .env.local exists with VITE_API_URL=http://localhost:8000

---

**Last Updated:** February 27, 2026
**Status:** Ready for production deployment
