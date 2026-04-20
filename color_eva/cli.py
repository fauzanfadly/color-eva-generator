from __future__ import annotations
import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path
import os
import logging
import re
import time
from typing import Any

API_BASE = "https://eva-painter-gvaya9bycrf6aacm.westus-01.azurewebsites.net/generate_support"


def _get_downloads_dir() -> Path:
    home = Path.home()
    downloads = home / "Downloads"
    return downloads


def _parse_color(s: str) -> str:
    s = s.strip()
    if s.startswith("#"):
        s = s[1:]
    s = s.strip().upper()
    if len(s) not in (3, 6):
        raise ValueError("expected 3 or 6 hex digits")
    if len(s) == 3:
        s = "".join([c * 2 for c in s])
    if not re.fullmatch(r"[0-9A-F]{6}", s):
        raise ValueError("color contains non-hex characters")
    return s


def _fetch_color(color_hex: str, timeout: int = 30, retries: int = 2, backoff: float = 1.0, verbose: bool = False) -> Any:
    params = {"color": color_hex}
    url = API_BASE + "?" + urllib.parse.urlencode(params)
    attempt = 0
    while True:
        try:
            if verbose:
                logging.debug("GET %s (attempt %d)", url, attempt + 1)
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                raw = resp.read()
                try:
                    return json.loads(raw.decode("utf-8"))
                except Exception:
                    return {"raw": raw.decode("utf-8", errors="replace")}
        except Exception as e:
            attempt += 1
            if attempt > retries:
                logging.debug("All retries exhausted: %s", e)
                raise
            sleep_time = backoff * (2 ** (attempt - 1))
            logging.debug("Request failed (attempt %d/%d): %s — retrying in %ss", attempt, retries, e, sleep_time)
            time.sleep(sleep_time)


def _save_json(data, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="color-eva")
    parser.add_argument("command", choices=["generate"])
    parser.add_argument("color", help='Color code, with or without leading "#"')
    parser.add_argument("-o", "--out", help="Output file path (optional)")
    parser.add_argument("--open", action="store_true", help="Open saved file after writing")
    parser.add_argument("--retries", type=int, default=2, help="Number of retries on failure (default: 2)")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds (default: 30)")
    parser.add_argument("--backoff", type=float, default=1.0, help="Base backoff seconds for retries (default: 1.0)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose/debug output")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s: %(message)s")

    try:
        color_hex = _parse_color(args.color)
    except Exception as e:
        logging.error("Invalid color: %s", e)
        return 2

    if args.command == "generate":
        logging.info("Sending color %s to EVA painter...", color_hex)
        try:
            data = _fetch_color(color_hex, timeout=args.timeout, retries=args.retries, backoff=args.backoff, verbose=args.verbose)
        except Exception as e:
            logging.error("Request failed: %s", e)
            return 3
        if args.out:
            out_path = Path(args.out)
        else:
            out_path = _get_downloads_dir() / f"color-eva-generate-{color_hex}.json"
        _save_json(data, out_path)
        logging.info("Saved JSON to %s", out_path)
        if args.open:
            try:
                if os.name == "nt":
                    os.startfile(str(out_path))
                else:
                    import webbrowser

                    webbrowser.open(str(out_path))
            except Exception:
                pass
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
