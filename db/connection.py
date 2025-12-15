import aiosqlite as sqlite

_db = None

async def get_database():
    global _db
    if _db is None:
        _db = await sqlite.connect("database.db")
        _db.row_factory = aiosqlite.Row
    return _db
