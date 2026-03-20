# Discord GitHub Notifier Bot

A Discord bot that sends real-time notifications to your server whenever commits are pushed to your GitHub repository.

## Features

- 🔔 **Real-time Webhook Notifications** - Get instant notifications when commits are pushed
- 📝 **Slash Commands** - Interactive commands to view commit information
- 🎨 **Beautiful Embeds** - Clean, formatted commit information
- 🚀 **Railway Deployment** - Easy deployment on Railway's platform
- 💾 **Persistent Storage** - Remembers notification channel settings

## Commands

- `/showbot` - Display welcome message with interactive button
- `/lastcommit` - Fetch and display the latest commit
- `/announcementchannel` - Set the channel for webhook notifications (Admin only)

## Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

### Manual Deployment Steps

#### 1. Prerequisites

- GitHub account
- Discord Bot Token ([Get it here](https://discord.com/developers/applications))
- GitHub Personal Access Token (optional but recommended)
- Railway account ([Sign up here](https://railway.app))

#### 2. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and name it
3. Go to **"Bot"** section → **"Add Bot"**
4. Enable these intents:
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Copy the **Bot Token** (save it securely)
6. Go to **OAuth2** → **URL Generator**
7. Select scopes: `bot`, `applications.commands`
8. Select permissions: `Send Messages`, `Embed Links`, `Mention Everyone`
9. Copy the URL and invite bot to your server

#### 3. Get GitHub Personal Access Token (Optional)

1. Go to GitHub **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
2. Click **"Generate new token (classic)"**
3. Select scope: `public_repo`
4. Copy the token

#### 4. Deploy to Railway

1. **Create New Project:**
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Connect your GitHub account and select this repository

2. **Configure Environment Variables:**
   Click on your service → **Variables** tab → Add these:

   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   GITHUB_TOKEN=your_github_personal_access_token (optional)
   GITHUB_REPO_OWNER=your_github_username
   GITHUB_REPO_NAME=your_repository_name
   WEBHOOK_SECRET=your_random_secret_key (optional but recommended)
   PORT=8080
   ```

3. **Generate Domain:**
   - Go to **Settings** tab
   - Scroll to **Networking**
   - Click **"Generate Domain"**
   - Copy your Railway URL (e.g., `https://your-app.up.railway.app`)

4. **Deploy:**
   - Railway auto-deploys on push
   - Check **Deployments** tab for logs

#### 5. Configure GitHub Webhook

1. Go to your GitHub repository
2. **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   - **Payload URL:** `https://your-railway-url.up.railway.app/webhook`
   - **Content type:** `application/json`
   - **Secret:** (same as `WEBHOOK_SECRET` in Railway)
   - **Events:** Select "Just the push event"
   - **Active:** ✅ Checked
4. Click **"Add webhook"**

#### 6. Test Your Bot

1. In Discord, use `/announcementchannel` in your desired channel
2. Use `/showbot` to see the welcome message
3. Click the "Last Commit" button or use `/lastcommit`
4. Push a commit to your repository
5. Verify the notification appears with @everyone mention

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | ✅ Yes | Your Discord bot token |
| `GITHUB_REPO_OWNER` | ✅ Yes | GitHub username/organization |
| `GITHUB_REPO_NAME` | ✅ Yes | Repository name |
| `GITHUB_TOKEN` | ❌ No | GitHub PAT (recommended for higher rate limits) |
| `WEBHOOK_SECRET` | ❌ No | Secret for webhook signature verification |
| `PORT` | ❌ No | Server port (default: 10000, Railway uses 8080) |


## Tech Stack

- **Python 3.12+**
- **discord.py** - Discord bot framework
- **Flask** - Webhook server
- **aiosqlite** - Async SQLite database
- **requests** - HTTP client for GitHub API

