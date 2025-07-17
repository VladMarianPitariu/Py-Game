from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio
import aiosqlite

app = FastAPI(title="Py-Game Highscore API")

DB_PATH = "./api/highscores.db"

class ScoreIn(BaseModel):
    player: str
    score: int

class ScoreOut(ScoreIn):
    id: int

@app.on_event("startup")
async def startup():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            score INTEGER NOT NULL
        )
        """)
        await db.commit()

@app.post("/scores/", response_model=ScoreOut)
async def add_score(score: ScoreIn):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO scores (player, score) VALUES (?, ?)",
            (score.player, score.score)
        )
        await db.commit()
        score_id = cursor.lastrowid
        return ScoreOut(id=score_id, **score.dict())

@app.get("/scores/", response_model=List[ScoreOut])
async def list_scores(limit: int = 10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, player, score FROM scores ORDER BY score DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [ScoreOut(id=row[0], player=row[1], score=row[2]) for row in rows]

@app.delete("/scores/{score_id}")
async def delete_score(score_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM scores WHERE id = ?", (score_id,))
        await db.commit()
    return {"ok": True}
