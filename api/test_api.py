from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Adaugă un scor nou
response = client.post("/scores/", json={"player": "Vasi", "score": 1000})
print("POST /scores/", response.json())

# Listează scorurile
response = client.get("/scores/")
print("GET /scores/", response.json())

# Șterge scorul adăugat
score_id = response.json()[0]["id"] if response.json() else None
if score_id:
    response = client.delete(f"/scores/{score_id}")
    print(f"DELETE /scores/{score_id}", response.json())
else:
    print("Nu există scoruri de șters.")
