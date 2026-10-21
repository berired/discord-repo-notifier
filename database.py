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
            # A reminder is sent once per task and due date, so changing the
            # due date allows a new reminder
            await db.execute('''
                CREATE TABLE IF NOT EXISTS deadline_reminders (
                    task_id TEXT NOT NULL,
                    due_ts INTEGER NOT NULL,
                    PRIMARY KEY (task_id, due_ts)
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

    async def set_ping_role(self, role_id: int | None):
        """Set the role to ping in notifications, or clear it with None"""
        async with aiosqlite.connect(self.db_path) as db:
            if role_id is None:
                await db.execute('DELETE FROM settings WHERE key = ?', ('ping_role',))
            else:
                await db.execute(
                    'INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                    ('ping_role', str(role_id))
                )
            await db.commit()

    async def get_ping_role(self) -> int | None:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT value FROM settings WHERE key = ?',
                ('ping_role',)
            ) as cursor:
                row = await cursor.fetchone()
                return int(row[0]) if row else None

    async def was_reminded(self, task_id: str, due_ts: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                'SELECT 1 FROM deadline_reminders WHERE task_id = ? AND due_ts = ?',
                (task_id, due_ts)
            ) as cursor:
                return await cursor.fetchone() is not None

    async def mark_reminded(self, task_id: str, due_ts: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT OR IGNORE INTO deadline_reminders (task_id, due_ts) VALUES (?, ?)',
                (task_id, due_ts)
            )
            await db.commit()

    async def clear_old_reminders(self, before_ts: int):
        """Forget reminders for deadlines that have already passed"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('DELETE FROM deadline_reminders WHERE due_ts < ?', (before_ts,))
            await db.commit()

db = Database()