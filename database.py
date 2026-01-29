import aiosqlite
import asyncio
from config import Config

class Database:
    def __init__(self, db_path: str = Config.DATABASE_PATH):
        self.db_path = db_path
        
    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            ''')
            await db.commit()
            
    async def set_announcement_channel(self, channel_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                ('announcement_channel', str(channel_id))
            )
            await db.commit()
            
    async def get_announcement_channel(self) -> int | None:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT value FROM settings WHERE key = ?',
                ('announcement_channel',)
            ) as cursor:
                row = await cursor.fetchone()
                return int(row[0]) if row else None
            
db = Database()