from fastapi import FastAPI
from routes import health, matches, pre_match, live
from legacy import live_engine
from routes import matches
from routes import prematch

app.include_router(prematch.router, prefix="/prematch")
app.include_router(matches.router, prefix="/matches")
app = FastAPI(title="PRONO API IA")

app.include_router(health.router)
app.include_router(matches.router, prefix="/matches")
app.include_router(pre_match.router, prefix="/pre-match")

# expose ton ancien système live
app.get("/signal")(live_engine.signal)
app.get("/alert")(live_engine.alert)
