from api.main import app

if __name__ == "__main__":
    import os
    import sys
    from fastapi.testclient import TestClient
    import uvicorn
    # Fallback: run with TestClient for quick test (sync, not async)
    client = TestClient(app)
    print("API test: GET /scores/")
    print(client.get("/scores/").json())
    # For local dev, you can also run with uvicorn if installed
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    print("Test completat. Pentru API real, folosește uvicorn sau gunicorn.")
