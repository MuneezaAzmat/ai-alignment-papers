# Deployment Guide

This guide covers several options for deploying your AI Alignment Papers app online.

## Option 1: Railway (Recommended - Easiest)

**Pros:** Free tier, automatic deployments, easy setup
**Cons:** Limited free hours per month

### Steps:

1. **Initialize Git Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Sign up for Railway:**
   - Go to https://railway.app/
   - Sign up with GitHub

3. **Deploy:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account and select this repository
   - Railway will auto-detect it's a Python app

4. **Set Environment Variables:**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add:
     - `ANTHROPIC_API_KEY` = your API key
     - `FLASK_SECRET_KEY` = random secret string
     - `CHECK_INTERVAL_HOURS` = 24

5. **Access Your App:**
   - Railway will give you a URL like `https://your-app.up.railway.app`

---

## Option 2: Render

**Pros:** Free tier with no time limits, persistent storage available
**Cons:** Slower cold starts on free tier

### Steps:

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/ai-alignment-papers.git
   git push -u origin main
   ```

2. **Sign up for Render:**
   - Go to https://render.com/
   - Sign up with GitHub

3. **Create New Web Service:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name:** ai-alignment-papers
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python run.py`

4. **Add Environment Variables:**
   - In Render dashboard, go to "Environment"
   - Add the same variables as above

5. **Deploy:**
   - Click "Create Web Service"
   - Render will build and deploy your app

---

## Option 3: Heroku

**Pros:** Mature platform, lots of documentation
**Cons:** No longer has free tier (starts at $5/month)

### Steps:

1. **Install Heroku CLI:**
   ```bash
   brew install heroku/brew/heroku
   ```

2. **Login and Create App:**
   ```bash
   heroku login
   heroku create ai-alignment-papers
   ```

3. **Set Environment Variables:**
   ```bash
   heroku config:set ANTHROPIC_API_KEY=your_key_here
   heroku config:set FLASK_SECRET_KEY=your_secret_here
   heroku config:set CHECK_INTERVAL_HOURS=24
   ```

4. **Deploy:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Open App:**
   ```bash
   heroku open
   ```

---

## Option 4: DigitalOcean App Platform

**Pros:** Good performance, $5/month tier
**Cons:** Not free, more complex setup

### Steps:

1. **Push to GitHub** (same as Render)

2. **Sign up for DigitalOcean:**
   - Go to https://www.digitalocean.com/
   - Create account

3. **Create App:**
   - Go to "Apps" → "Create App"
   - Select GitHub and connect repository
   - Choose branch to deploy

4. **Configure:**
   - App Spec will be auto-detected
   - Add environment variables in settings
   - Choose $5/month Basic plan

5. **Deploy:**
   - Click "Create Resources"

---

## Option 5: AWS (Most Control)

**Pros:** Full control, scalable, many services
**Cons:** Complex, can be expensive, steep learning curve

### Using AWS Elastic Beanstalk:

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   eb init -p python-3.9 ai-alignment-papers
   eb create ai-alignment-papers-env
   ```

3. **Set Environment Variables:**
   ```bash
   eb setenv ANTHROPIC_API_KEY=your_key FLASK_SECRET_KEY=your_secret
   ```

4. **Deploy:**
   ```bash
   eb deploy
   ```

---

## Option 6: Self-Hosted VPS

**Pros:** Full control, cheap if you know what you're doing
**Cons:** Requires server management knowledge

### Using a VPS (DigitalOcean Droplet, Linode, etc.):

1. **Create VPS** ($5-10/month)

2. **SSH into server:**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install dependencies:**
   ```bash
   apt update
   apt install python3 python3-pip nginx
   ```

4. **Clone your repository:**
   ```bash
   git clone https://github.com/yourusername/ai-alignment-papers.git
   cd ai-alignment-papers
   ```

5. **Install Python packages:**
   ```bash
   pip3 install -r requirements.txt
   ```

6. **Set up systemd service:**
   Create `/etc/systemd/system/alignment-papers.service`:
   ```ini
   [Unit]
   Description=AI Alignment Papers
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/root/ai-alignment-papers
   Environment="ANTHROPIC_API_KEY=your_key"
   Environment="FLASK_SECRET_KEY=your_secret"
   ExecStart=/usr/bin/python3 /root/ai-alignment-papers/run.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start service:**
   ```bash
   systemctl start alignment-papers
   systemctl enable alignment-papers
   ```

8. **Configure Nginx** to reverse proxy to port 5000

---

## Recommended: Railway or Render

For most users, I recommend **Railway** or **Render** because they:
- Have generous free tiers
- Auto-deploy from GitHub
- Handle HTTPS automatically
- Require minimal configuration
- Are beginner-friendly

## Important Notes

### Database Persistence
- SQLite database will be lost on restart with some platforms
- For production, consider:
  - Using a persistent volume (Railway, Render support this)
  - Upgrading to PostgreSQL for multi-user scenarios
  - Backing up the database regularly

### Environment Variables
Always set these in your deployment platform:
- `ANTHROPIC_API_KEY` - Your Claude API key
- `FLASK_SECRET_KEY` - Random secret for Flask sessions
- `CHECK_INTERVAL_HOURS` - How often to check for new papers (default: 24)
- `PORT` - Usually set automatically by platform

### Security Considerations
- Never commit `.env` file to Git (already in .gitignore)
- Use platform's secret management for API keys
- Consider adding authentication if making truly public
- Monitor API usage to avoid unexpected charges

### Cost Estimates
- **Railway Free Tier:** $5 credit/month (enough for hobby use)
- **Render Free Tier:** Unlimited but with cold starts
- **Heroku:** Starting at $5/month
- **DigitalOcean:** $5/month minimum
- **AWS:** Variable, can be free tier eligible for 12 months

## Quick Start: Railway Deployment

The fastest way to get online:

```bash
# 1. Initialize git
git init
git add .
git commit -m "Initial commit"

# 2. Push to GitHub
# (Create a new repository on GitHub first)
git remote add origin https://github.com/yourusername/ai-alignment-papers.git
git push -u origin main

# 3. Go to railway.app
# - Sign up with GitHub
# - Click "New Project" → "Deploy from GitHub repo"
# - Select your repository
# - Add environment variables in the dashboard
# - Done! Your app is live
```

Your app will be live at a URL like: `https://ai-alignment-papers.up.railway.app`
