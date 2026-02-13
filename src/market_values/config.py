import os
from pathlib import Path
import yaml

CONFIG_DIR = Path.home() / ".market-values"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

DEFAULT_CONFIG = {
    "stock_codes": [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
    ],
    "server": {
        "host": "127.0.0.1",
        "port": 8000,
    },
    "refresh_interval_seconds": 5,
}


def ensure_config():
    """Create default config file if it doesn't exist."""
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False, sort_keys=False)
        print(f"Created default config at {CONFIG_FILE}")


def load_config() -> dict:
    """Load config from YAML file, falling back to defaults."""
    ensure_config()
    try:
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f)
        if not isinstance(config, dict):
            return DEFAULT_CONFIG.copy()
        return config
    except Exception:
        return DEFAULT_CONFIG.copy()


def get_stock_codes() -> list:
    """Get stock codes from config. Re-reads file each call for live editing."""
    config = load_config()
    return config.get("stock_codes", DEFAULT_CONFIG["stock_codes"])
