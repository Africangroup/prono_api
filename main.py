from fastapi import FastAPI
from supabase_client import supabase

app = FastAPI(title="PRONO API", version="1.0")

# ===============================
# 🟢 ROUTE TEST
# ===============================
@app.get("/")
def home():
    return {"message": "API Pronostics active"}


# ===============================
# 🔵 RECUPERER STATS PREMATCH
# ===============================
@app.get("/prematch")
def get_prematch():
    response = supabase.table("prematch_stats").select("*").execute()
    return response.data
