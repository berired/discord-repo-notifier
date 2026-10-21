# Discord GitHub Notifier Bot

A Discord bot that sends real-time notifications to your server whenever commits are pushed to your GitHub repository.

## Features

- 🔔 **Real-time Webhook Notifications** - Get instant notifications when commits are pushed
- 📝 **Slash Commands** - Interactive commands to view commit information
- 🎨 **Beautiful Embeds** - Clean, formatted commit information
- 🚀 **Wispbyte Deployment** - Runs on Wispbyte's Python hosting
- 📋 **ClickUp Task Embeds** - Title, status, assignee and deadline, on demand or via ClickUp webhook
- 💾 **Persistent Storage** - Remembers notification channel settings

## Commands

- `/showbot` - Display welcome message with interactive button
- `/lastcommit` - Fetch and display the latest commit
- `/lasttask` - Fetch and display the latest updated ClickUp task
- `/alltasks` - List open ClickUp tasks in the Space with status, assignee, urgency and deadline. A private menu first asks for **No Filter**, or a filter by **Assignee**, **Status** or **Urgency** (ClickUp priority); the filtered list is then posted to the channel
- `/announcementchannel [role]` - Set the channel for webhook notifications, optionally choosing the role to ping (Admin only)
- `/pingrole [role]` - Change the role pinged on notifications; run with no role to reset (Admin only)

If no role is set, commit notifications ping `@everyone` and ClickUp task notifications ping nobody.

The `/showbot` message also has **Last Task** and **All Tasks** buttons next to **Last Commit**. **All Tasks** opens the same filter menu as `/alltasks`.

## Deploy to Wispbyte

### Manual Deployment Steps

#### 1. Prerequisites

- GitHub account
- Discord Bot Token ([Get it here](https://discord.com/developers/applications))
- GitHub Personal Access Token (optional but recommended)
- Wispbyte account ([Sign up here](https://wispbyte.com))

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

#### 4. Deploy to Wispbyte

1. **Create a Python server** in the Wispbyte dashboard (Python 3.12 if available).

2. **Add the code:**
   - Clone this repository onto the server, or
   - Upload these files via the File Manager: `main.py`, `bot.py`, `config.py`, `database.py`, `embeds.py`, `github_api.py`, `clickup_api.py`, `webhook_server.py`, `requirements.txt`

3. **Set the startup file** to `main.py` (startup command: `python main.py`). Dependencies are installed from `requirements.txt`.

4. **Configure environment variables** in the panel's variables section, or upload a `.env` file next to `main.py`:

   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   GITHUB_TOKEN=your_github_personal_access_token (optional)
   GITHUB_REPO_OWNER=your_github_username
   GITHUB_REPO_NAME=your_repository_name
   WEBHOOK_SECRET=your_random_secret_key (optional but recommended)
   DISCORD_GUILD_ID=your_discord_server_id (optional, instant command sync)
   PORT=<the port allocated to your Wispbyte server>
   ```

5. **Start the server** and check the console for the bot login message.

#### 5. Configure GitHub Webhook

The Flask server must be reachable from the internet, so `PORT` must be a port Wispbyte exposes for your server.

1. Go to your GitHub repository
2. **Settings** → **Webhooks** → **Add webhook**
3. Configure:
   - **Payload URL:** `http://<your-wispbyte-address>:<port>/webhook` (use your assigned domain instead if you have one)
   - **Content type:** `application/json`
   - **Secret:** (same as `WEBHOOK_SECRET`)
   - **Events:** Select "Just the push event"
   - **Active:** ✅ Checked
4. Click **"Add webhook"**

#### 6. Connect ClickUp (Optional)

1. In ClickUp, go to **Settings** → **Apps** and generate a **Personal API Token**. Set it as `CLICKUP_API_TOKEN`.
2. The Workspace (team) ID is the first number in your ClickUp URL (`app.clickup.com/<team_id>/...`). Set it as `CLICKUP_TEAM_ID`.
3. Find the Space ID by listing your Spaces and copying the `id` of the one to track, then set it as `CLICKUP_SPACE_ID`:

   ```bash
   curl "https://api.clickup.com/api/v2/team/<TEAM_ID>/space" -H "Authorization: <CLICKUP_API_TOKEN>"
   ```

4. Restart the bot. `/lasttask` and the **Last Task** button now show the most recently updated task across all Lists in that Space.
5. For automatic notifications, register a webhook (ClickUp has no UI for this):

   ```bash
   curl -X POST "https://api.clickup.com/api/v2/team/<TEAM_ID>/webhook" \
     -H "Authorization: <CLICKUP_API_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"endpoint": "http://<your-wispbyte-address>:<port>/clickup-webhook", "events": ["taskCreated", "taskStatusUpdated", "taskAssigneeUpdated", "taskDueDateUpdated"], "space_id": "<CLICKUP_SPACE_ID>"}'
   ```

   The response includes a `secret`. Set it as `CLICKUP_WEBHOOK_SECRET` and restart the bot. Task updates are posted to the channel set with `/announcementchannel`.

#### 7. Test Your Bot

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
| `DISCORD_GUILD_ID` | ❌ No | Server ID for instant slash command sync |
| `CLICKUP_API_TOKEN` | ❌ No | ClickUp personal API token (enables task embeds) |
| `CLICKUP_TEAM_ID` | ❌ No | ClickUp Workspace (team) ID |
| `CLICKUP_SPACE_ID` | ❌ No | ClickUp Space to read the latest task from |
| `CLICKUP_WEBHOOK_SECRET` | ❌ No | Secret returned when registering the ClickUp webhook |
| `PORT` | ❌ No | Server port (default: 10000); set to the port Wispbyte allocates |


## Tech Stack

- **Python 3.12+**
- **discord.py** - Discord bot framework
- **Flask** - Webhook server
- **aiosqlite** - Async SQLite database
- **requests** - HTTP client for GitHub API
