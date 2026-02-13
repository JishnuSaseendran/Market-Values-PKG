import argparse
import threading
import time
import webbrowser

from market_values.config import ensure_config, load_config


def main():
    config = load_config()
    server_cfg = config.get("server", {})
    default_host = server_cfg.get("host", "127.0.0.1")
    default_port = server_cfg.get("port", 8000)

    parser = argparse.ArgumentParser(description="Market Values — live stock market dashboard")
    parser.add_argument("--host", default=default_host, help=f"Bind host (default: {default_host})")
    parser.add_argument("--port", type=int, default=default_port, help=f"Bind port (default: {default_port})")
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open the browser")
    args = parser.parse_args()

    ensure_config()

    if not args.no_browser:
        def open_browser():
            time.sleep(1.5)
            webbrowser.open(f"http://{args.host}:{args.port}")
        threading.Thread(target=open_browser, daemon=True).start()

    import uvicorn
    uvicorn.run(
        "market_values.app:create_app",
        host=args.host,
        port=args.port,
        factory=True,
    )


if __name__ == "__main__":
    main()
