import discord
from typing import Dict

class EmbedBuilder:
    COLOR_PRIMARY = 0x5865F2
    COLOR_SUCCESS = 0x57F287
    COLOR_INFO = 0x3498DB
    
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
                "`/announcementchannel` - Set notification channel"
            ),
            inline=False
        )
        embed.add_field(
            name="🔔 Quick Action",
            value="Click the button below to view the latest commit!",
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