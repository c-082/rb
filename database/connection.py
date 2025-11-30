import aiosqlite as sqlite

async def get_database():
    connection = await sqlite.connect("database.db")
    connection.row_factory = sqlite.Row
    return connection
