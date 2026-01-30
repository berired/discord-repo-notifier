import asyncio
import threading
from bot import bot, run_bot, send_webhook_notification
from webhook_server import run_server, set_notification_callback
from database import db
from config import Config

def start_flask_server():
    """Start Flask server in a separate thread"""
    print("Starting Flask webhook server...")
    run_server()

async def init_database():
    """Initialize the database"""
    print("Initializing database...")
    await db.init_db()
    print("Database initialized!")

def main():
    """Main entry point"""
    try:
        # Validate configuration
        Config.validate()
        print("Configuration validated successfully!")
        
        # Initialize database
        asyncio.run(init_database())
        
        # Start Flask server in a separate thread
        flask_thread = threading.Thread(target=start_flask_server, daemon=True)
        flask_thread.start()
        print(f"Flask server started on port {Config.PORT}")
        
        # Start Discord bot (blocking)
        # The event loop will be set after the bot starts
        print("Starting Discord bot...")
        run_bot()
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please check your .env file and ensure all required variables are set.")
    except Exception as e:
        print(f"Fatal Error: {e}")
        raise

if __name__ == "__main__":
    main()