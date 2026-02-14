# main.py

from fastapi import FastAPI
from api import router as api_router

# ===============================
# 🚀 Initialisation FastAPI
# ===============================
app = FastAPI(
    title="VrSOCCER API",
    version="2.0"
)

# ===============================
# 🏥 Route Health Check
# ===============================
@app.get("/health")
def health_check():
    """
    Vérifie que l'API est active
    """
    return {"status": "API Pronostics active"}

# ===============================
# 🔗 Inclusion des routes API
# ===============================
app.include_router(api_router)
