
from __future__ import annotations

from pathlib import Path

from core import db as core_db
from core.state import AppState


def ask_lang() -> str:
    raw = input("[1] - English\n[2] - Русский\n>>> ").strip()
    return "ru" if raw == "2" else "en"

def ask_sport(t) -> str:
    raw = input(f'\n{t("select_sport","Select a sport")}:\n[1] - {t("basketball","Basketball")}\n[2] - {t("soccer","Soccer")}\n>>> ').strip()
    return "soccer" if raw == "2" else "basketball"

def main():
    state = AppState(lang=ask_lang(), sport="basketball", storage_path=Path("source").resolve())
    state.sport = ask_sport(state.t)
    db = core_db.load_db(state)

    while True:
        print()
        print(f'{state.t("currently_in","Currently in")} {state.t(state.sport, state.sport.title())}')
        print(f'[1] - {state.t("add_game","Add game")}')
        print(f'[2] - {state.t("view_games","View games")}')
        print(f'[3] - {state.t("stats_review","Statistics")}')
        print(f'[4] - {state.t("data_export","Export")}')
        print(f'[5] - {state.t("change_sport","Change sport")}')
        print(f'[6] - {state.t("change_lang","Change language")}')
        print(f'[7] - {state.t("exit","Exit")}')
        choice = input(f'{state.t("select","Select")} >> ').strip()

        if choice == "1":
            # very minimal CLI add: just name/date/minutes; better use GUI
            name = input(state.t("game_name","Game name")+": ")
            date = input(state.t("game_date","Date")+": ")
            minutes = input(state.t("game_minutes","Minutes")+": ")
            game = {"name": name, "date": date, "minutes": int(minutes or 0)}
            core_db.add_game(state, db, game)
            db = core_db.load_db(state)
            input(state.t("enter_to_continue","Enter to continue")+"... ")

        elif choice == "2":
            games = core_db.list_games(db)
            for i,g in enumerate(games,1):
                print(f"{i} - {g.get('name','')}")
            sel = input(state.t("game_to_show","Select game to show")+": ").strip()
            if sel.isdigit():
                idx = int(sel)-1
                if 0 <= idx < len(games):
                    for k,v in core_db.game_details(state, games[idx]):
                        print(f"{k}: {v}")
            input(state.t("enter_to_continue","Enter to continue")+"... ")

        elif choice == "3":
            st = core_db.compute_stats(state, db)
            if st["games"] == 0:
                print(state.t("no_saved_games","No saved games")+".")
            else:
                print(f'{state.t("stat","Stat"): <20} {state.t("all_time","All time"): <10} {state.t("per_game","Per game")}')
                print("-"*50)
                for stat, ag, pg in st["table"]:
                    print(f"{stat:<20} {ag:<10} {'' if pg is None else pg}")
                print("-"*50)
                print(f'{state.t("games","Games")}: {st["games"]}')
                if "efficiency" in st.get("extra",{}):
                    print(f'{state.t("efficiency","Efficiency")}: {st["extra"]["efficiency"]}')
            input(state.t("enter_to_continue","Enter to continue")+"... ")

        elif choice == "4":
            try:
                out = core_db.export_to_csv(state, db)
                print(f"OK: {out}")
            except Exception:
                print(state.t("no_games","No games"))
            input(state.t("enter_to_continue","Enter to continue")+"... ")

        elif choice == "5":
            state.sport = ask_sport(state.t)
            db = core_db.load_db(state)

        elif choice == "6":
            state.lang = ask_lang()
            state.reload_texts()

        elif choice == "7":
            break

if __name__ == "__main__":
    main()
