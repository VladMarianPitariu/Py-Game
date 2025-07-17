import aiosqlite
import asyncio

async def create_table():
    async with aiosqlite.connect("./api/highscores.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        """)
        await db.commit()
    print("Tabela 'scores' a fost creată sau există deja.")

if __name__ == "__main__":
    asyncio.run(create_table())
