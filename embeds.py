import discord
from typing import Dict

class EmbedBuilder:
    COLOR_PRIMARY = 0x5865F2
    COLOR_SUCCESS = 0x57F287
    COLOR_INFO = 0x3498DB
    COLOR_CLICKUP = 0x7B68EE

    @staticmethod
    def create_welcome_embed() -> discord.Embed:
        """Create the welcome embed"""
        embed = discord.Embed(
            title="🤖 Welcome to GitHub Repo Notification Bot",
            description="Stay updated with real-time GitHub repository notifications!",
            color=EmbedBuilder.COLOR_PRIMARY
        )
        embed.add_field(
            name="📋 Available Commands",
            value=(
                "`/showbot` - Display this welcome message\n"
                "`/lastcommit` - View the latest commit\n"
                "`/lasttask` - View the latest ClickUp task\n"
                "`/announcementchannel` - Set notification channel (and ping role)\n"
                "`/pingrole` - Choose which role is pinged"
            ),
            inline=False
        )
        embed.add_field(
            name="🔔 Quick Action",
            value="Click a button below to view the latest commit or ClickUp task!",
            inline=False
        )
        embed.set_footer(text="GitHub Notification Bot • Powered by discord.py")
        return embed
    
    @staticmethod
    def create_commit_embed(commit_data: Dict) -> discord.Embed:
        """Create an embed for a commit"""
        embed = discord.Embed(
            title=f"📝 {commit_data['title']}",
            description=commit_data['description'] if commit_data['description'] else "*No additional description*",
            color=EmbedBuilder.COLOR_SUCCESS,
            url=commit_data['url']
        )
        
        embed.add_field(
            name="🔀 Branch",
            value=f"`{commit_data['branch']}`",
            inline=True
        )
        
        embed.add_field(
            name="👤 Author",
            value=commit_data['author'],
            inline=True
        )
        
        embed.add_field(
            name="🕒 Time",
            value=commit_data['timestamp'],
            inline=False
        )
        
        embed.add_field(
            name="🔗 Commit Hash",
            value=f"[`{commit_data['sha']}`]({commit_data['url']})",
            inline=True
        )
        
        embed.set_footer(text="GitHub Repository Update")
        return embed
    
    @staticmethod
    def create_task_embed(task_data: Dict) -> discord.Embed:
        """Create an embed for a ClickUp task"""
        color = EmbedBuilder.COLOR_CLICKUP
        status_color = task_data.get('status_color')
        if status_color:
            try:
                color = int(status_color.lstrip('#'), 16)
            except ValueError:
                pass

        embed = discord.Embed(
            title=f"📋 {task_data['title']}",
            color=color,
            url=task_data['url'] or None
        )

        embed.add_field(
            name="📌 Status",
            value=task_data['status'].title(),
            inline=True
        )

        embed.add_field(
            name="👤 Assigned To",
            value=", ".join(task_data['assignees']),
            inline=True
        )

        embed.add_field(
            name="⏰ Deadline",
            value=task_data['due_date'],
            inline=False
        )

        embed.set_footer(text="ClickUp Task Update")
        return embed

    @staticmethod
    def create_error_embed(message: str) -> discord.Embed:
        """Create an error embed"""
        embed = discord.Embed(
            title="❌ Error",
            description=message,
            color=0xED4245
        )
        return embed
    
    @staticmethod
    def create_success_embed(message: str) -> discord.Embed:
        """Create a success embed"""
        embed = discord.Embed(
            title="✅ Success",
            description=message,
            color=EmbedBuilder.COLOR_SUCCESS
        )
        return embed

embed_builder = EmbedBuilder()