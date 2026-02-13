from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio

from market_values.services import fetch_all_stocks, get_candlestick_data
from market_values.config import get_stock_codes, load_config

STATIC_DIR = Path(__file__).parent / "static"


def create_app() -> FastAPI:
    app = FastAPI(title="Market Values")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- API routes (registered before static catch-all) ---

    @app.get("/stocks")
    async def get_stocks():
        codes = get_stock_codes()
        data = await fetch_all_stocks(codes)
        return {"data": data}

    @app.websocket("/ws/stocks")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                config = load_config()
                codes = get_stock_codes()
                interval = config.get("refresh_interval_seconds", 5)
                data = await fetch_all_stocks(codes)
                await websocket.send_json(data)
                await asyncio.sleep(interval)
        except WebSocketDisconnect:
            print("Client disconnected")

    @app.get("/candles/{symbol}")
    def get_candles(symbol: str):
        data = get_candlestick_data(symbol)
        return {"data": data}

    # --- Static file serving (SPA) ---

    if STATIC_DIR.is_dir():
        app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            """Catch-all: serve index.html for any non-API route (SPA routing)."""
            return FileResponse(STATIC_DIR / "index.html")

    return app
