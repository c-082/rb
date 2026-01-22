import aiosqlite
import asyncio

_db = None
_db_lock = asyncio.Lock()

async def get_database():
    global _db
    async with _db_lock:
        if _db is None:
            _db = await aiosqlite.connect("database.db")
            await _db.execute("PRAGMA journal_mode=WAL;")
            await _db.execute("PRAGMA foreign_keys=ON;")
            await _db.commit()
        return _db
