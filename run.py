import os
import sys
import uvicorn

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    is_prod = os.getenv("ENVIRONMENT", "").lower() == "production"
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=not is_prod)
