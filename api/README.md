# Py-Game Highscore API

Microserviciu async pentru scoruri, extensibil, cu FastAPI și SQLite.

## Funcționalitate
- Adaugă scoruri: `POST /scores/` (JSON: `{player, score}`)
- Listează scoruri: `GET /scores/?limit=10`
- Șterge scor: `DELETE /scores/{score_id}`

## Pornire rapidă
1. Instalează dependențele:
   ```bash
   pip install fastapi aiosqlite uvicorn
   ```
2. Rulează serverul:
   ```bash
   uvicorn api.main:app --reload
   ```
3. Accesează API-ul la `http://localhost:8000`.

## Extensibilitate
- Poți adăuga endpoints pentru user management, progres, etc.
- Structură MVC/MVCS, ușor de extins.

## Best practices
- Async/await pentru I/O și DB.
- SQLite pentru simplitate, se poate schimba cu orice DB.
- Standard REST (nu SOAP).

## Exemplu request
```bash
curl -X POST "http://localhost:8000/scores/" -H "Content-Type: application/json" -d '{"player": "Vasi", "score": 1234}'
```
