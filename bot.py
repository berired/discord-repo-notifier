import discord
from discord.ext import commands
from discord import app_commands
from database import db
from github_api import github_api
from embeds import embed_builder
from config import Config

class LastCommitButton(discord.ui.View):
    """Persistent button for last commit"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="Last Commit",
        style=discord.ButtonStyle.primary,
        custom_id="last_commit_button",
        emoji="📝"
    )
    async def last_commit_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        """Handle last commit button click"""
        await interaction.response.defer(thinking=True)
        
        commit_data = github_api.get_latest_commit()
        if commit_data:
            embed = embed_builder.create_commit_embed(commit_data)
            await interaction.followup.send(embed=embed)
        else:
            embed = embed_builder.create_error_embed(
                "Failed to fetch the latest commit. Please try again later."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

class GitHubBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
        
    async def setup_hook(self):
        """Setup hook called when bot is starting"""
        # Add persistent view
        self.add_view(LastCommitButton())
        
        # Sync commands
        await self.tree.sync()
        print("Commands synced successfully!")
    
    async def on_ready(self):
        """Called when bot is ready"""
        if self.user:
            print(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Connected to {len(self.guilds)} guilds')
        print('------')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="GitHub commits"
            )
        )

# Initialize bot
bot = GitHubBot()

@bot.tree.command(name="showbot", description="Display welcome message and bot information")
async def show_bot(interaction: discord.Interaction):
    """Show welcome message with persistent button"""
    embed = embed_builder.create_welcome_embed()
    view = LastCommitButton()
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="lastcommit", description="Fetch and display the latest commit from the repository")
async def last_commit(interaction: discord.Interaction):
    """Fetch the latest commit from GitHub"""
    await interaction.response.defer(thinking=True)
    
    commit_data = github_api.get_latest_commit()
    if commit_data:
        embed = embed_builder.create_commit_embed(commit_data)
        await interaction.followup.send(embed=embed)
    else:
        embed = embed_builder.create_error_embed(
            "Failed to fetch the latest commit. Please check the repository configuration."
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="announcementchannel", description="Set the current channel for GitHub notifications")
@app_commands.checks.has_permissions(administrator=True)
async def announcement_channel(interaction: discord.Interaction):
    """Set the announcement channel for webhook notifications"""
    if interaction.channel_id is None:
        embed = embed_builder.create_error_embed(
            "Unable to determine the channel. Please try again."
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    await db.set_announcement_channel(interaction.channel_id)
    
    channel_mention = f"<#{interaction.channel_id}>"
    embed = embed_builder.create_success_embed(
        f"✅ Announcement channel set to {channel_mention}\n\n"
        f"All GitHub push notifications will be sent here!"
    )
    await interaction.response.send_message(embed=embed)

@announcement_channel.error
async def announcement_channel_error(interaction: discord.Interaction, error):
    """Handle errors for announcement channel command"""
    if isinstance(error, app_commands.errors.MissingPermissions):
        embed = embed_builder.create_error_embed(
            "You need Administrator permissions to set the announcement channel."
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def send_webhook_notification(commit_data: dict):
    """Send notification to the announcement channel"""
    channel_id = await db.get_announcement_channel()
    
    if not channel_id:
        print("No announcement channel set. Skipping notification.")
        return
    
    channel = bot.get_channel(channel_id)
    if not channel:
        print(f"Channel {channel_id} not found. Skipping notification.")
        return
    
    if not isinstance(channel, discord.TextChannel):
        print(f"Channel {channel_id} is not a text channel. Skipping notification.")
        return
    
    try:
        embed = embed_builder.create_commit_embed(commit_data)
        await channel.send(content="@everyone 🚀 **New Commit Pushed!**", embed=embed)
        print(f"Notification sent to channel {channel_id}")
    except Exception as e:
        print(f"Error sending notification: {e}")

def run_bot():
    """Run the Discord bot"""
    token = Config.DISCORD_TOKEN
    if not token:
        raise ValueError("DISCORD_TOKEN is not set in configuration")
    bot.run(token)