#!/usr/bin/env python3
"""
scripts/generate_profile.py

Fetches real-time telemetry from Chess.com Public API for `sahill17` and generates
a dark-mode, compact SVG telemetry card (`assets/chess-card.svg`).
Also caches raw data to `data/chess_cache.json` for offline resilience.

Zero pip dependencies (uses Python standard library only).
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = REPO_ROOT / "assets"
DATA_DIR = REPO_ROOT / "data"
CACHE_FILE = DATA_DIR / "chess_cache.json"
OUTPUT_SVG = ASSETS_DIR / "chess-card.svg"

USER_AGENT = "SahilPalGitHubProfile/1.0 (saahilpal17@gmail.com)"
USERNAME = "sahill17"

# Standard Cburnett vector chess pieces (viewBox="0 0 45 45")
PIECE_SYMBOLS = {
    "wP": '<path fill="#fff" stroke="#000" stroke-linecap="round" stroke-width="1.5" d="M22.5 9c-2.21 0-4 1.79-4 4 0 .89.29 1.71.78 2.38C17.33 16.5 16 18.59 16 21c0 2.03.94 3.84 2.41 5.03-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47 1.47-1.19 2.41-3 2.41-5.03 0-2.41-1.33-4.5-3.28-5.62.49-.67.78-1.49.78-2.38 0-2.21-1.79-4-4-4z"/>',
    "wN": '<g fill="none" fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path fill="#fff" d="M22 10c10.5 1 16.5 8 16 29H15c0-9 10-6.5 8-21"/><path fill="#fff" d="M24 18c.38 2.91-5.55 7.37-8 9-3 2-2.82 4.34-5 4-1.042-.94 1.41-3.04 0-3-1 0 .19 1.23-1 2-1 0-4.003 1-4-4 0-2 6-12 6-12s1.89-1.9 2-3.5c-.73-.994-.5-2-.5-3 1-1 3 2.5 3 2.5h2s.78-1.992 2.5-3c1 0 1 3 1 3"/><path fill="#000" d="M9.5 25.5a.5.5 0 1 1-1 0 .5.5 0 1 1 1 0m5.433-9.75a.5 1.5 30 1 1-.866-.5.5 1.5 30 1 1 .866.5"/></g>',
    "wB": '<g fill="none" fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><g fill="#fff" stroke-linecap="butt"><path d="M9 36c3.39-.97 10.11.43 13.5-2 3.39 2.43 10.11 1.03 13.5 2 0 0 1.65.54 3 2-.68.97-1.65.99-3 .5-3.39-.97-10.11.46-13.5-1-3.39 1.46-10.11.03-13.5 1-1.35.49-2.32.47-3-.5 1.35-1.94 3-2 3-2z"/><path d="M15 32c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2z"/><path d="M25 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 1 1 5 0z"/></g><path stroke-linejoin="miter" d="M17.5 26h10M15 30h15m-7.5-14.5v5M20 18h5"/></g>',
    "wR": '<g fill="#fff" fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path stroke-linecap="butt" d="M9 39h27v-3H9zm3-3v-4h21v4zm-1-22V9h4v2h5V9h5v2h5V9h4v5"/><path d="m34 14-3 3H14l-3-3"/><path stroke-linecap="butt" stroke-linejoin="miter" d="M31 17v12.5H14V17"/><path d="m31 29.5 1.5 2.5h-20l1.5-2.5"/><path fill="none" stroke-linejoin="miter" d="M11 14h23"/></g>',
    "wQ": '<g fill="#fff" fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path d="M8 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0m16.5-4.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0M41 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0M16 8.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0M33 9a2 2 0 1 1-4 0 2 2 0 1 1 4 0"/><path stroke-linecap="butt" d="M9 26c8.5-1.5 21-1.5 27 0l2-12-7 11V11l-5.5 13.5-3-15-3 15-5.5-14V25L7 14z"/><path stroke-linecap="butt" d="M9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z"/><path fill="none" d="M11.5 30c3.5-1 18.5-1 22 0M12 33.5c6-1 15-1 21 0"/></g>',
    "wK": '<g fill="none" fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path stroke-linejoin="miter" d="M22.5 11.63V6M20 8h5"/><path fill="#fff" stroke-linecap="butt" stroke-linejoin="miter" d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5"/><path fill="#fff" d="M11.5 37c5.5 3.5 15.5 3.5 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10z"/><path d="M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0"/></g>',
    "bP": '<path stroke="#000" stroke-linecap="round" stroke-width="1.5" d="M22.5 9a4 4 0 0 0-3.22 6.38 6.48 6.48 0 0 0-.87 10.65c-3 1.06-7.41 5.55-7.41 13.47h23c0-7.92-4.41-12.41-7.41-13.47a6.46 6.46 0 0 0-.87-10.65A4.01 4.01 0 0 0 22.5 9z"/>',
    "bN": '<g fill="none" fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path fill="#000" d="M22 10c10.5 1 16.5 8 16 29H15c0-9 10-6.5 8-21"/><path fill="#000" d="M24 18c.38 2.91-5.55 7.37-8 9-3 2-2.82 4.34-5 4-1.04-.94 1.41-3.04 0-3-1 0 .19 1.23-1 2-1 0-4 1-4-4 0-2 6-12 6-12s1.89-1.9 2-3.5c-.73-1-.5-2-.5-3 1-1 3 2.5 3 2.5h2s.78-2 2.5-3c1 0 1 3 1 3"/><path fill="#ececec" stroke="#ececec" d="M9.5 25.5a.5.5 0 1 1-1 0 .5.5 0 1 1 1 0m5.43-9.75a.5 1.5 30 1 1-.86-.5.5 1.5 30 1 1 .86.5"/><path fill="#ececec" stroke="none" d="m24.55 10.4-.45 1.45.5.15c3.15 1 5.65 2.49 7.9 6.75S35.75 29.06 35.25 39l-.05.5h2.25l.05-.5c.5-10.06-.88-16.85-3.25-21.34s-5.79-6.64-9.19-7.16z"/></g>',
    "bB": '<g fill="none" fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><g fill="#000" stroke-linecap="butt"><path d="M9 36c3.4-1 10.1.4 13.5-2 3.4 2.4 10.1 1 13.5 2 0 0 1.6.5 3 2-.7 1-1.6 1-3 .5-3.4-1-10.1.5-13.5-1-3.4 1.5-10.1 0-13.5 1-1.4.5-2.3.5-3-.5 1.4-2 3-2 3-2z"/><path d="M15 32c2.5 2.5 12.5 2.5 15 0 .5-1.5 0-2 0-2 0-2.5-2.5-4-2.5-4 5.5-1.5 6-11.5-5-15.5-11 4-10.5 14-5 15.5 0 0-2.5 1.5-2.5 4 0 0-.5.5 0 2z"/><path d="M25 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 1 1 5 0z"/></g><path stroke="#ececec" stroke-linejoin="miter" d="M17.5 26h10M15 30h15m-7.5-14.5v5M20 18h5"/></g>',
    "bR": '<g fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path stroke-linecap="butt" d="M9 39h27v-3H9zm3.5-7 1.5-2.5h17l1.5 2.5zm-.5 4v-4h21v4z"/><path stroke-linecap="butt" stroke-linejoin="miter" d="M14 29.5v-13h17v13z"/><path stroke-linecap="butt" d="M14 16.5 11 14h23l-3 2.5zM11 14V9h4v2h5V9h5v2h5V9h4v5z"/><path fill="none" stroke="#ececec" stroke-linejoin="miter" stroke-width="1" d="M12 35.5h21m-20-4h19m-18-2h17m-17-13h17M11 14h23"/></g>',
    "bQ": '<g fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><g stroke="none"><circle cx="6" cy="12" r="2.75"/><circle cx="14" cy="9" r="2.75"/><circle cx="22.5" cy="8" r="2.75"/><circle cx="31" cy="9" r="2.75"/><circle cx="39" cy="12" r="2.75"/></g><path stroke-linecap="butt" d="M9 26c8.5-1.5 21-1.5 27 0l2.5-12.5L31 25l-.3-14.1-5.2 13.6-3-14.5-3 14.5-5.2-13.6L14 25 6.5 13.5z"/><path stroke-linecap="butt" d="M9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z"/><path fill="none" stroke-linecap="butt" d="M11 38.5a35 35 1 0 0 23 0"/><path fill="none" stroke="#ececec" d="M11 29a35 35 1 0 1 23 0m-21.5 2.5h20m-21 3a35 35 1 0 0 22 0m-23 3a35 35 1 0 0 24 0"/></g>',
    "bK": '<g fill="none" fill-rule="evenodd" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path stroke-linejoin="miter" d="M22.5 11.6V6"/><path fill="#000" stroke-linecap="butt" stroke-linejoin="miter" d="M22.5 25s4.5-7.5 3-10.5c0 0-1-2.5-3-2.5s-3 2.5-3 2.5c-1.5 3 3 10.5 3 10.5"/><path fill="#000" d="M11.5 37a22.3 22.3 0 0 0 21 0v-7s9-4.5 6-10.5c-4-6.5-13.5-3.5-16 4V27v-3.5c-3.5-7.5-13-10.5-16-4-3 6 5 10 5 10z"/><path stroke-linejoin="miter" d="M20 8h5"/><path stroke="#ececec" d="M32 29.5s8.5-4 6-9.7C34.1 14 25 18 22.5 24.6v2.1-2.1C20 18 9.9 14 7 19.9c-2.5 5.6 4.8 9 4.8 9"/><path stroke="#ececec" d="M11.5 30c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0m-21 3.5c5.5-3 15.5-3 21 0"/></g>',
}


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_cached_data() -> dict:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "stats": {
            "chess_blitz": {
                "last": {"rating": 917},
                "best": {"rating": 1124},
                "record": {"win": 2138, "loss": 2054, "draw": 113},
            },
            "chess_rapid": {
                "last": {"rating": 860},
                "best": {"rating": 1418},
                "record": {"win": 40, "loss": 32, "draw": 3},
            },
            "chess_bullet": {
                "last": {"rating": 496},
                "best": {"rating": 1388},
                "record": {"win": 2, "loss": 6, "draw": 0},
            },
            "chess_daily": {
                "last": {"rating": 1381},
                "best": {"rating": 1685},
                "record": {"win": 15, "loss": 8, "draw": 1},
            },
            "tactics": {"highest": {"rating": 1556}},
            "puzzle_rush": {"best": {"score": 27}},
        },
        "latest_game": {
            "url": "https://www.chess.com/game/live/172939473130",
            "fen": "2kr3r/2p3p1/4p3/2p5/pp2PR2/6Q1/PPPqn1PP/1N3RK1 w - - 2 22",
            "opening": "Giuoco Piano Game",
            "opponent": "Littleboy3atu",
            "opponent_rating": 1006,
            "sahil_rating": 917,
            "result_str": "0-1",
            "time_class": "Blitz",
            "last_move": "21... Ne2+",
            "highlight_sq": "e2",
            "check_sq": "g1",
        },
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def clean_opening_name(eco_url: str | None, pgn: str | None) -> str:
    if eco_url:
        match = re.search(r"/openings/([^/]+)", eco_url)
        if match:
            slug = match.group(1).replace("-", " ")
            parts = slug.split()
            cleaned = []
            for p in parts:
                if re.match(r"^\d+\.", p):
                    break
                cleaned.append(p)
            if cleaned:
                return " ".join(cleaned)
    if pgn:
        eco_m = re.search(r'\[ECO "([^"]+)"\]', pgn)
        if eco_m:
            return f"ECO {eco_m.group(1)}"
    return "Giuoco Piano Game"


def parse_fen(fen: str) -> list[list[str | None]]:
    board_part = fen.split()[0]
    ranks = board_part.split("/")
    board = []
    for r in ranks:
        row: list[str | None] = []
        for ch in r:
            if ch.isdigit():
                row.extend([None] * int(ch))
            else:
                row.append(ch)
        board.append(row)
    return board


def sq_to_coords(sq: str) -> tuple[int, int]:
    if len(sq) >= 2:
        col = ord(sq[0].lower()) - ord("a")
        rank = int(sq[1])
        row = 8 - rank
        return (row, col)
    return (6, 4)


def get_live_data() -> dict:
    data = load_cached_data()
    try:
        stats = fetch_json(f"https://api.chess.com/pub/player/{USERNAME}/stats")
        data["stats"] = stats

        archives = fetch_json(f"https://api.chess.com/pub/player/{USERNAME}/games/archives").get("archives", [])
        if archives:
            latest_archive_url = archives[-1]
            games_data = fetch_json(latest_archive_url)
            games = games_data.get("games", [])
            if games:
                last_game = games[-1]
                fen = last_game.get("fen", data["latest_game"]["fen"])
                url = last_game.get("url", f"https://www.chess.com/member/{USERNAME}")
                pgn = last_game.get("pgn", "")
                eco = last_game.get("eco", "")

                is_white = last_game.get("white", {}).get("username", "").lower() == USERNAME.lower()
                me = last_game.get("white", {}) if is_white else last_game.get("black", {})
                opp = last_game.get("black", {}) if is_white else last_game.get("white", {})

                res_white = last_game.get("white", {}).get("result", "")
                res_black = last_game.get("black", {}).get("result", "")
                result_str = "1-0" if res_white == "win" else "0-1" if res_black == "win" else "½-½"

                # Clean PGN comments and trailing results
                clean_pgn = re.sub(r"\{[^}]*\}", "", pgn)
                clean_pgn = re.sub(r"\s*(1-0|0-1|1/2-1/2|\*)\s*$", "", clean_pgn).strip()

                moves = re.findall(r"(\d+\.+|\d+\.\.\.)\s*([Oa-hKQRBN][a-h1-8x+#=\-O]*)", clean_pgn)
                if moves:
                    last_num, last_san = moves[-1]
                    last_move = f"{last_num} {last_san}".strip()
                else:
                    last_move = "21... Ne2+"
                    last_san = "Ne2+"

                highlight_sq = "e2"
                sq_matches = re.findall(r"([a-h][1-8])", last_san)
                if sq_matches:
                    highlight_sq = sq_matches[-1]

                check_sq = None
                if "+" in last_san or "#" in last_san:
                    target_king = "K" if " w " in fen else "k"
                    board_rep = parse_fen(fen)
                    for r_idx in range(8):
                        for c_idx in range(8):
                            if board_rep[r_idx][c_idx] == target_king:
                                file_char = chr(ord("a") + c_idx)
                                rank_char = str(8 - r_idx)
                                check_sq = f"{file_char}{rank_char}"
                                break

                data["latest_game"] = {
                    "url": url,
                    "fen": fen,
                    "opening": clean_opening_name(eco, pgn),
                    "opponent": opp.get("username", "Opponent"),
                    "opponent_rating": opp.get("rating", 1000),
                    "sahil_rating": me.get("rating", 917),
                    "result_str": result_str,
                    "time_class": f"{last_game.get('time_class', 'blitz').capitalize()}",
                    "last_move": last_move,
                    "highlight_sq": highlight_sq,
                    "check_sq": check_sq,
                }

        data["updated_at"] = datetime.now(timezone.utc).isoformat()

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    except Exception as e:
        print(f"[WARN] Failed to fetch live Chess.com telemetry: {e}. Using cached data.")

    return data


def generate_svg(data: dict) -> str:
    stats = data["stats"]
    game = data["latest_game"]

    blitz = stats.get("chess_blitz", {})
    blitz_rating = blitz.get("last", {}).get("rating", 917)
    blitz_best = blitz.get("best", {}).get("rating", 1124)
    blitz_rec = blitz.get("record", {})
    blitz_total = blitz_rec.get("win", 2138) + blitz_rec.get("loss", 2054) + blitz_rec.get("draw", 113)

    rapid = stats.get("chess_rapid", {})
    rapid_rating = rapid.get("last", {}).get("rating", 860)
    rapid_best = rapid.get("best", {}).get("rating", 1418)
    rapid_rec = rapid.get("record", {})
    rapid_total = rapid_rec.get("win", 40) + rapid_rec.get("loss", 32) + rapid_rec.get("draw", 3)

    bullet = stats.get("chess_bullet", {})
    bullet_total = bullet.get("record", {}).get("win", 2) + bullet.get("record", {}).get("loss", 6)

    daily = stats.get("chess_daily", {})
    daily_total = daily.get("record", {}).get("win", 15) + daily.get("record", {}).get("loss", 8)

    tactics_peak = stats.get("tactics", {}).get("highest", {}).get("rating", 1556)
    total_games_played = blitz_total + rapid_total + bullet_total + daily_total

    board = parse_fen(game["fen"])

    # Compact Board layout: 96x96 px (12x12 per square)
    board_x = 16
    board_y = 14
    sq_size = 12

    hl_row, hl_col = sq_to_coords(game.get("highlight_sq", "e2"))
    check_coords = sq_to_coords(game["check_sq"]) if game.get("check_sq") else None

    # Piece defs symbols
    symbols_xml = []
    for piece_id, inner_svg in PIECE_SYMBOLS.items():
        symbols_xml.append(f'    <symbol id="piece-{piece_id}" viewBox="0 0 45 45">\n      {inner_svg}\n    </symbol>')
    symbols_str = "\n".join(symbols_xml)

    # Squares & Pieces SVG elements
    squares_svg = []
    for r in range(8):
        for c in range(8):
            x = board_x + c * sq_size
            y = board_y + r * sq_size
            is_light = (r + c) % 2 == 0
            sq_fill = "#b0bcc9" if is_light else "#334155"

            is_hl = (r == hl_row and c == hl_col)
            is_chk = (check_coords and r == check_coords[0] and c == check_coords[1])

            squares_svg.append(f'      <rect x="{x}" y="{y}" width="{sq_size}" height="{sq_size}" fill="{sq_fill}" />')

            if is_hl:
                squares_svg.append(
                    f'      <rect x="{x}" y="{y}" width="{sq_size}" height="{sq_size}" fill="#f59e0b" fill-opacity="0.5" stroke="#f59e0b" stroke-width="1" />'
                )
            if is_chk:
                squares_svg.append(
                    f'      <rect x="{x}" y="{y}" width="{sq_size}" height="{sq_size}" fill="#ef4444" fill-opacity="0.5" stroke="#ef4444" stroke-width="1" />'
                )

            p = board[r][c]
            if p:
                piece_id = f"w{p}" if p.isupper() else f"b{p.upper()}"
                squares_svg.append(
                    f'      <use href="#piece-{piece_id}" x="{x}" y="{y}" width="{sq_size}" height="{sq_size}" />'
                )

    board_elements = "\n".join(squares_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 124" width="100%" height="124" style="background:#0d1117; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <linearGradient id="card-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#161b22"/>
      <stop offset="100%" stop-color="#0e131a"/>
    </linearGradient>
    <linearGradient id="metric-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1c2128"/>
      <stop offset="100%" stop-color="#13171f"/>
    </linearGradient>
{symbols_str}
  </defs>

  <style>
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.35; }}
    }}
    .pulse-live {{ animation: pulse 2.2s infinite ease-in-out; }}
    .mono {{ font-family: 'SF Mono', 'JetBrains Mono', Consolas, 'Liberation Mono', Menlo, monospace; }}
  </style>

  <!-- Outer Card Container -->
  <rect x="1" y="1" width="818" height="122" rx="10" fill="url(#card-grad)" stroke="#30363d" stroke-width="1" />

  <!-- ======================================================== -->
  <!-- LEFT: MINI 8x8 BOARD (96x96 px)                          -->
  <!-- ======================================================== -->
  <rect x="{board_x - 1}" y="{board_y - 1}" width="98" height="98" fill="none" stroke="#475569" stroke-width="1" rx="2" />
{board_elements}

  <!-- ======================================================== -->
  <!-- MIDDLE-LEFT: GAME TELEMETRY BRIEF                        -->
  <!-- ======================================================== -->
  <g transform="translate(126, 16)">
    <!-- Header with Pulse Indicator -->
    <circle cx="4" cy="9" r="3.5" fill="#3fb950" class="pulse-live" />
    <text x="14" y="12" fill="#3fb950" font-size="9" font-weight="700" class="mono" letter-spacing="0.5">CHESS.COM LIVE TELEMETRY</text>

    <!-- Opening Title -->
    <text x="0" y="34" fill="#f0f6fc" font-size="12" font-weight="700" class="mono">{game['opening'][:26]}</text>

    <!-- Opponent & Result -->
    <text x="0" y="52" fill="#8b949e" font-size="10" class="mono">vs {game['opponent']} ({game['opponent_rating']}) · {game['result_str']} ({game['time_class']})</text>

    <!-- Last Move Pill -->
    <rect x="0" y="66" width="168" height="22" rx="4" fill="#1c2128" stroke="#30363d" stroke-width="0.8" />
    <text x="8" y="81" fill="#f59e0b" font-size="9.5" font-weight="700" class="mono">Last: {game.get('last_move', '21... Ne2+')}</text>
  </g>

  <!-- ======================================================== -->
  <!-- RIGHT: 4 COMPACT METRIC CARDS                            -->
  <!-- ======================================================== -->
  <!-- Card 1: Blitz -->
  <g transform="translate(320, 14)">
    <rect x="0" y="0" width="114" height="96" rx="6" fill="url(#metric-grad)" stroke="#30363d" stroke-width="1" />
    <text x="10" y="20" fill="#8b949e" font-size="8.5" font-weight="700" class="mono">BLITZ (3+0 / 5m)</text>
    <text x="10" y="48" fill="#f0f6fc" font-size="20" font-weight="800" class="mono">{blitz_rating}</text>
    <text x="10" y="68" fill="#3fb950" font-size="9" font-weight="600" class="mono">Peak: {blitz_best}</text>
    <text x="10" y="84" fill="#6e7681" font-size="8" class="mono">{blitz_total:,} games</text>
  </g>

  <!-- Card 2: Rapid -->
  <g transform="translate(442, 14)">
    <rect x="0" y="0" width="114" height="96" rx="6" fill="url(#metric-grad)" stroke="#30363d" stroke-width="1" />
    <text x="10" y="20" fill="#8b949e" font-size="8.5" font-weight="700" class="mono">RAPID (10m+)</text>
    <text x="10" y="48" fill="#f0f6fc" font-size="20" font-weight="800" class="mono">{rapid_rating}</text>
    <text x="10" y="68" fill="#58a6ff" font-size="9" font-weight="600" class="mono">Peak: {rapid_best}</text>
    <text x="10" y="84" fill="#6e7681" font-size="8" class="mono">{rapid_total} games (53% W)</text>
  </g>

  <!-- Card 3: Tactics -->
  <g transform="translate(564, 14)">
    <rect x="0" y="0" width="114" height="96" rx="6" fill="url(#metric-grad)" stroke="#30363d" stroke-width="1" />
    <text x="10" y="20" fill="#8b949e" font-size="8.5" font-weight="700" class="mono">TACTICS PEAK</text>
    <text x="10" y="48" fill="#f0b429" font-size="20" font-weight="800" class="mono">{tactics_peak}</text>
    <text x="10" y="68" fill="#f0b429" font-size="9" font-weight="600" class="mono">All-time high</text>
    <text x="10" y="84" fill="#6e7681" font-size="8" class="mono">Puzzle Rush: 27</text>
  </g>

  <!-- Card 4: Battles -->
  <g transform="translate(686, 14)">
    <rect x="0" y="0" width="118" height="96" rx="6" fill="url(#metric-grad)" stroke="#30363d" stroke-width="1" />
    <text x="10" y="20" fill="#8b949e" font-size="8.5" font-weight="700" class="mono">TOTAL BATTLES</text>
    <text x="10" y="48" fill="#f0f6fc" font-size="20" font-weight="800" class="mono">{total_games_played:,}</text>
    <text x="10" y="68" fill="#8b949e" font-size="9" font-weight="600" class="mono">Across all modes</text>
    <text x="10" y="84" fill="#3fb950" font-size="8" class="mono">sahill17 ↗</text>
  </g>
</svg>
"""
    return svg


def main() -> None:
    print(f"Fetching Chess.com telemetry for {USERNAME}...")
    data = get_live_data()

    print(f"Generating {OUTPUT_SVG.name}...")
    svg_content = generate_svg(data)

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"Successfully generated {OUTPUT_SVG} ({len(svg_content)} bytes)")


if __name__ == "__main__":
    main()
