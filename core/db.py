from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .state import AppState

def _safe_int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except Exception:
        return default

def _ensure_game_ids(db: Dict[str, Any]) -> bool:
    """Ensure each game has a stable id. Returns True if db was modified."""
    changed = False
    games = db.get("games") or []
    if not isinstance(games, list):
        db["games"] = []
        return True
    for g in games:
        if isinstance(g, dict) and not g.get("id"):
            g["id"] = __import__("uuid").uuid4().hex
            changed = True
    return changed

def load_db(state: AppState) -> Dict[str, Any]:
    path = state.data_file()
    try:
        with path.open("r", encoding="utf-8") as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {"player": "", "games": []}
    except json.JSONDecodeError:
        db = {"player": "", "games": []}

    if _ensure_game_ids(db):
        save_db(state, db)
    return db

def save_db(state: AppState, db: Dict[str, Any]) -> None:
    path = state.data_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def list_games(db: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(db.get("games", []) or [])

def get_game(db: Dict[str, Any], game_id: str) -> Optional[Dict[str, Any]]:
    for g in list_games(db):
        if str(g.get("id")) == str(game_id):
            return g
    return None

def add_game(state: AppState, db: Dict[str, Any], game: Dict[str, Any]) -> str:
    if not game.get("id"):
        game["id"] = __import__("uuid").uuid4().hex
    db.setdefault("games", []).append(game)
    save_db(state, db)
    return str(game["id"])

def update_game(state: AppState, db: Dict[str, Any], game_id: str, patch: Dict[str, Any]) -> bool:
    games = db.get("games") or []
    for i, g in enumerate(games):
        if str(g.get("id")) == str(game_id):
            if not isinstance(g, dict):
                return False
            g.update(patch)
            g["id"] = str(game_id)  # protect
            save_db(state, db)
            return True
    return False

def delete_game(state: AppState, db: Dict[str, Any], game_id: str) -> bool:
    games = db.get("games") or []
    for i, g in enumerate(games):
        if str(g.get("id")) == str(game_id):
            del games[i]
            save_db(state, db)
            return True
    return False

def compute_stats(state: AppState, db: Dict[str, Any]) -> Dict[str, Any]:
    games = list_games(db)
    if not games:
        return {"games": 0, "table": [], "extra": {}}

    if state.sport == "basketball":
        all_points = sum(_safe_int(g.get("points")) for g in games)
        all_minutes = sum(_safe_int(g.get("minutes")) for g in games)
        all_2ptm = sum(_safe_int(g.get("2ptshots_made")) for g in games)
        all_3ptm = sum(_safe_int(g.get("3ptshots_made")) for g in games)
        all_assists = sum(_safe_int(g.get("assists")) for g in games)
        all_rebounds = sum(_safe_int(g.get("rebounds")) for g in games)
        all_blocks = sum(_safe_int(g.get("blocks")) for g in games)
        all_steals = sum(_safe_int(g.get("steals")) for g in games)

        all_2pta = sum(_safe_int(g.get("2pt_attempts")) for g in games)
        all_3pta = sum(_safe_int(g.get("3pt_attempts")) for g in games)
        all_missed = (all_2pta - all_2ptm) + (all_3pta - all_3ptm)

        all_turnovers = sum(_safe_int(g.get("turnovers")) for g in games)
        all_missed_ft = sum(_safe_int(g.get("missedFT")) for g in games)
        n = len(games)

        efficiency = (all_points + all_rebounds + all_assists + all_steals + all_blocks) - (all_missed + all_missed_ft + all_turnovers)

        table = [
            ("Points", all_points, round(all_points / n, 2)),
            ("Minutes", all_minutes, None),
            ("2 Pointers", all_2ptm, None),
            ("3 Pointers", all_3ptm, None),
            ("Assists", all_assists, round(all_assists / n, 2)),
            ("Rebounds", all_rebounds, round(all_rebounds / n, 2)),
            ("Blocks", all_blocks, round(all_blocks / n, 2)),
            ("Steals", all_steals, round(all_steals / n, 2)),
            ("Missed", all_missed, round(all_missed / n, 2)),
            ("Missed Free Throws", all_missed_ft, round(all_missed_ft / n, 2)),
        ]
        return {"games": n, "table": table, "extra": {"efficiency": efficiency}}

    # soccer
    all_minutes = sum(_safe_int(g.get("minutes")) for g in games)
    all_goals = sum(_safe_int(g.get("goals")) for g in games)
    all_assists = sum(_safe_int(g.get("assists")) for g in games)
    all_shots = sum(_safe_int(g.get("shots")) for g in games)
    all_yellow = sum(_safe_int(g.get("yellow_cards")) for g in games)
    all_red = sum(_safe_int(g.get("red_cards")) for g in games)
    all_fouls = sum(_safe_int(g.get("fouls")) for g in games)
    n = len(games)

    table = [
        ("Minutes", all_minutes, None),
        ("Goals", all_goals, round(all_goals / n, 2)),
        ("Assists", all_assists, round(all_assists / n, 2)),
        ("Shots", all_shots, round(all_shots / n, 2)),
        ("Yellow Cards", all_yellow, round(all_yellow / n, 2)),
        ("Red Cards", all_red, round(all_red / n, 2)),
        ("Fouls", all_fouls, round(all_fouls / n, 2)),
    ]
    return {"games": n, "table": table, "extra": {}}

def game_details(state: AppState, game: Dict[str, Any]) -> List[Tuple[str, str]]:
    if state.sport == "basketball":
        def frac(made_key, att_key):
            made = _safe_int(game.get(made_key))
            att = _safe_int(game.get(att_key))
            return f"{made}/{att}"
        return [
            ("Date", str(game.get("date",""))),
            ("POS", str(game.get("position",""))),
            ("MIN", str(game.get("minutes",""))),
            ("PTS", str(game.get("points",""))),
            ("AST", str(game.get("assists",""))),
            ("2PT", frac("2ptshots_made","2pt_attempts")),
            ("3PT", frac("3ptshots_made","3pt_attempts")),
            ("REB", str(game.get("rebounds",""))),
            ("BLK", str(game.get("blocks",""))),
            ("STL", str(game.get("steals",""))),
            ("PF", str(game.get("personal_fouls",""))),
            ("Missed FT", str(game.get("missedFT",""))),
            ("TO", str(game.get("turnovers",""))),
            ("WIN", str(game.get("Won",""))),
        ]
    return [
        ("Date", str(game.get("date",""))),
        ("POS", str(game.get("position",""))),
        ("MIN", str(game.get("minutes",""))),
        ("GOALS", str(game.get("goals",""))),
        ("AST", str(game.get("assists",""))),
        ("SHOTS", str(game.get("shots",""))),
        ("YC", str(game.get("yellow_cards",""))),
        ("RC", str(game.get("red_cards",""))),
        ("Fouls", str(game.get("fouls",""))),
        ("WIN", str(game.get("Won",""))),
    ]

def export_to_csv(state: AppState, db: Dict[str, Any], filename: Optional[Path] = None) -> Path:
    games = list_games(db)
    if not games:
        raise ValueError("no_games")

    out = filename or state.export_file()
    out.parent.mkdir(parents=True, exist_ok=True)

    if state.sport == "basketball":
        headers = ['Date', 'POS', 'MIN', 'PTS', 'AST', '2PTA', '2PTM', '3PTA', '3PTM', 'REB', 'BLK', 'STL', 'PF', 'Missed Free Throws', 'Turnovers', 'WIN']
        key_mapping = {
            'Date': 'date',
            'POS': 'position',
            'MIN': 'minutes',
            'PTS': 'points',
            'AST': 'assists',
            '2PTA': '2pt_attempts',
            '2PTM': '2ptshots_made',
            '3PTA': '3pt_attempts',
            '3PTM': '3ptshots_made',
            'REB': 'rebounds',
            'BLK': 'blocks',
            'STL': 'steals',
            'PF': 'personal_fouls',
            'Missed Free Throws': 'missedFT',
            'Turnovers': 'turnovers',
            'WIN': 'Won'
        }
    else:
        headers = ['Date', 'POS', 'MIN', 'GOALS', 'AST', 'SHOTS', 'Yellow cards', 'Red cards', 'Fouls', 'WIN']
        key_mapping = {
            'Date': 'date',
            'POS': 'position',
            'MIN': 'minutes',
            'GOALS': 'goals',
            'AST': 'assists',
            'SHOTS': 'shots',
            'Yellow cards': 'yellow_cards',
            'Red cards': 'red_cards',
            'Fouls': 'fouls',
            'WIN': 'Won'
        }

    with out.open('w', newline='', encoding='utf-8') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=headers)
        writer.writeheader()
        for game in games:
            row = {csv_key: game.get(json_key, '') for csv_key, json_key in key_mapping.items()}
            writer.writerow(row)

    return out
