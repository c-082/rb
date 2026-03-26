import os
import aiosqlite
import asyncio
from contextlib import asynccontextmanager

DB_PATH = "database.db"
setup_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup.sql")

_db = None
_lock = asyncio.Lock()

async def get_database():
    global _db
    async with _lock:
        if _db is None:
            _db = await aiosqlite.connect(DB_PATH)
            await _db.execute("PRAGMA journal_mode=WAL;")
            await _db.execute("PRAGMA foreign_keys=ON;")
            await _db.commit()
            _db.row_factory = aiosqlite.Row
        return _db

async def close_database():
    global _db
    async with _lock:
        if _db is not None:
            await _db.close()
            _db = None

@asynccontextmanager
async def get_db():
    db = await get_database()
    try:
        yield db
    finally:
        pass

async def init_database():
    async with aiosqlite.connect(DB_PATH) as db:
        with open(setup_path, "r") as f:
            await db.executescript(f.read())
        await db.commit()
        await db.execute("CREATE INDEX IF NOT EXISTS idx_user_guild_id ON user(guild_id);")
        await db.commit()
