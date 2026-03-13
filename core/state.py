from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional

THIS_DIR = Path(__file__).resolve().parent
LOCALISATION_DIR = (THIS_DIR.parent / "localization").resolve()

def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)

@dataclass
class AppState:
    """Runtime state + file locations.

    - storage_path: where basketball.json / soccer.json / export.csv live
    - config_dir: where config.json lives (we keep it stable on mobile in App.user_data_dir)
    - storage_mode: "app" | "project" (only meaningful on desktop)
    """
    lang: str = "en"          # "en" | "ru"
    sport: str = "basketball" # "basketball" | "soccer"
    storage_path: Path = Path("").resolve()
    config_dir: Path = Path("").resolve()
    storage_mode: str = "app"

    texts: Dict[str, str] = None  # loaded on init

    def __post_init__(self) -> None:
        self.reload_texts()

    # ---- localization ----
    def reload_texts(self) -> None:
        path = LOCALISATION_DIR / f"lang_{self.lang}.json"
        self.texts = _read_json(path)

    def t(self, key: str, default: Optional[str] = None) -> str:
        if self.texts and key in self.texts:
            return str(self.texts[key])
        return default if default is not None else key

    # ---- config ----
    def config_file(self) -> Path:
        return self.config_dir / "config.json"

    def load_config(self) -> None:
        path = self.config_file()
        try:
            cfg = _read_json(path)
        except FileNotFoundError:
            return
        except Exception:
            return
        self.lang = str(cfg.get("lang", self.lang) or self.lang)
        self.sport = str(cfg.get("sport", self.sport) or self.sport)
        self.storage_mode = str(cfg.get("storage_mode", self.storage_mode) or self.storage_mode)

    def save_config(self) -> None:
        _write_json(self.config_file(), {
            "lang": self.lang,
            "sport": self.sport,
            "storage_mode": self.storage_mode,
        })

    # ---- data locations ----
    def data_file(self) -> Path:
        if self.sport == "basketball":
            return self.storage_path / "basketball.json"
        return self.storage_path / "soccer.json"

    def export_file(self) -> Path:
        return self.storage_path / "export.csv"
