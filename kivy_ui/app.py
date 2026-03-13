from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.utils import platform as kivy_platform

from core import db as core_db
from core.state import AppState


def _popup(title: str, text: str) -> None:
    content = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))
    lbl = Label(text=text, halign="left", valign="top")
    lbl.bind(size=lbl.setter("text_size"))
    content.add_widget(lbl)
    btn = Button(text="OK", size_hint_y=None, height=dp(44))
    content.add_widget(btn)
    p = Popup(title=title, content=content, size_hint=(0.92, 0.7))
    btn.bind(on_release=p.dismiss)
    p.open()


def _confirm(title: str, text: str, on_yes) -> None:
    content = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))
    lbl = Label(text=text, halign="left", valign="top")
    lbl.bind(size=lbl.setter("text_size"))
    content.add_widget(lbl)

    row = BoxLayout(orientation="horizontal", spacing=dp(12), size_hint_y=None, height=dp(48))
    yes = Button(text="Yes", size_hint_x=0.5)
    no = Button(text="No", size_hint_x=0.5)
    row.add_widget(yes)
    row.add_widget(no)
    content.add_widget(row)

    p = Popup(title=title, content=content, size_hint=(0.92, 0.6))

    def _yes(*_):
        p.dismiss()
        try:
            on_yes()
        except Exception as e:
            _popup("ERROR", str(e))

    yes.bind(on_release=_yes)
    no.bind(on_release=p.dismiss)
    p.open()


class LanguageScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))
        root.add_widget(Label(text="Select language / Выберите язык", font_size="20sp",
                              size_hint_y=None, height=dp(56)))
        row = BoxLayout(orientation="horizontal", spacing=dp(12), size_hint_y=None, height=dp(52))
        b1 = Button(text="English")
        b2 = Button(text="Русский")
        row.add_widget(b1)
        row.add_widget(b2)
        root.add_widget(row)
        self.add_widget(root)

        b1.bind(on_release=lambda *_: self._set_lang("en"))
        b2.bind(on_release=lambda *_: self._set_lang("ru"))

    def _set_lang(self, lang: str):
        app: "ShowoffKivyApp" = App.get_running_app()
        app.state.lang = lang
        app.state.reload_texts()
        app.state.save_config()
        self.manager.current = "sport"


class SportScreen(Screen):
    def on_enter(self):
        self.clear_widgets()
        app: "ShowoffKivyApp" = App.get_running_app()
        t = app.state.t
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))
        root.add_widget(Label(text=t("select_sport", "Select sport"), font_size="20sp",
                              size_hint_y=None, height=dp(56)))
        b1 = Button(text=t("basketball", "Basketball"), size_hint_y=None, height=dp(52))
        b2 = Button(text=t("soccer", "Soccer"), size_hint_y=None, height=dp(52))
        root.add_widget(b1)
        root.add_widget(b2)
        self.add_widget(root)

        b1.bind(on_release=lambda *_: self._set_sport("basketball"))
        b2.bind(on_release=lambda *_: self._set_sport("soccer"))

    def _set_sport(self, sport: str):
        app: "ShowoffKivyApp" = App.get_running_app()
        app.state.sport = sport
        app.state.save_config()
        app.reload_db()
        self.manager.current = "menu"


class MenuScreen(Screen):
    def on_enter(self):
        self.render()

    def render(self):
        self.clear_widgets()
        app: "ShowoffKivyApp" = App.get_running_app()
        t = app.state.t
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))

        title = f"SHOWOFF • {t('currently_in', 'Currently in')} {t(app.state.sport, app.state.sport.title())}"
        root.add_widget(Label(text=title, font_size="20sp", size_hint_y=None, height=dp(56)))

        btns = [
            (t("add_game", "Add game"), "add_game"),
            (t("view_games", "View games"), "games"),
            (t("stats_review", "Statistics"), "stats"),
            (t("data_export", "Export"), "export"),
            (t("settings", "Settings"), "settings"),
            (t("change_sport", "Change sport"), "sport"),
            (t("change_lang", "Change language"), "language"),
        ]
        for text, target in btns:
            b = Button(text=text, size_hint_y=None, height=dp(52))
            b.bind(on_release=lambda _b, tgt=target: setattr(self.manager, "current", tgt))
            root.add_widget(b)

        exit_btn = Button(text=t("exit", "Exit"), size_hint_y=None, height=dp(52))
        exit_btn.bind(on_press=self.exit_app)
        root.add_widget(exit_btn)

        self.add_widget(root)

    def exit_app(self, *_):
        App.get_running_app().stop()


class GamesScreen(Screen):
    def on_enter(self):
        self.render()

    def render(self):
        self.clear_widgets()
        app: "ShowoffKivyApp" = App.get_running_app()
        t = app.state.t
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))

        root.add_widget(Label(text=t("view_games", "View games"), font_size="20sp",
                              size_hint_y=None, height=dp(56)))

        games = core_db.list_games(app.db)
        if not games:
            root.add_widget(Label(text=t("no_saved_games", "No saved games") + ".", halign="left"))
        else:
            sv = ScrollView()
            lst = BoxLayout(orientation="vertical", spacing=dp(8), size_hint_y=None)
            lst.bind(minimum_height=lst.setter("height"))

            for idx, g in enumerate(games):
                gid = str(g.get("id") or idx)
                name = str(g.get("name") or f"Game {idx + 1}")
                date = str(g.get("date") or "")
                header = f"{idx + 1}. {name} {('— ' + date) if date else ''}"

                row = BoxLayout(orientation="horizontal", spacing=dp(8),
                                size_hint_y=None, height=dp(48))
                btn = Button(text=header, halign="left")
                btn.bind(on_release=lambda _b, game_id=gid: self._open_details(game_id))
                edit = Button(text="✎", size_hint_x=None, width=dp(48))
                edit.bind(on_release=lambda _b, game_id=gid: self._edit(game_id))
                delete = Button(text="🗑", size_hint_x=None, width=dp(48))
                delete.bind(on_release=lambda _b, game_id=gid: self._delete(game_id))

                row.add_widget(btn)
                row.add_widget(edit)
                row.add_widget(delete)
                lst.add_widget(row)

            sv.add_widget(lst)
            root.add_widget(sv)

        back = Button(text="← " + t("menu", "Menu"), size_hint_y=None, height=dp(48))
        back.bind(on_release=lambda *_: setattr(self.manager, "current", "menu"))
        root.add_widget(back)

        self.add_widget(root)

    def _open_details(self, game_id: str):
        app: "ShowoffKivyApp" = App.get_running_app()
        game = core_db.get_game(app.db, game_id)
        if not game:
            return
        details = core_db.game_details(app.state, game)
        text = "\n".join([f"{k}: {v}" for k, v in details])
        _popup("Game", text)

    def _edit(self, game_id: str):
        app: "ShowoffKivyApp" = App.get_running_app()
        app.edit_game_id = game_id
        self.manager.current = "add_game"

    def _delete(self, game_id: str):
        app: "ShowoffKivyApp" = App.get_running_app()
        t = app.state.t
        game = core_db.get_game(app.db, game_id)
        if not game:
            return

        name = str(game.get("name") or "Game")
        date = str(game.get("date") or "")
        msg = f"{t('delete', 'Delete')} «{name}» {('(' + date + ')') if date else ''}?"

        def do():
            ok = core_db.delete_game(app.state, app.db, game_id)
            if ok:
                app.reload_db()
                self.render()
            else:
                _popup("Delete", "Not found")

        _confirm(t("delete", "Delete"), msg, do)


class StatsScreen(Screen):
    def on_enter(self):
        self.render()

    def render(self):
        self.clear_widgets()
        app: "ShowoffKivyApp" = App.get_running_app()
        t = app.state.t
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))
        root.add_widget(Label(text=t("stats_review", "Statistics"), font_size="20sp",
                              size_hint_y=None, height=dp(56)))

        try:
            stats = core_db.compute_stats(app.state, app.db)
        except Exception as e:
            root.add_widget(Label(text=f"ERROR: {e}"))
            stats = {"games": 0, "table": [], "extra": {}}

        if stats["games"] == 0:
            root.add_widget(Label(text=t("no_saved_games", "No saved games") + ".", halign="left"))
        else:
            sv = ScrollView()
            box = BoxLayout(orientation="vertical", spacing=dp(6), size_hint_y=None)
            box.bind(minimum_height=box.setter("height"))

            header = f"{t('stat', 'Stat'): <15}  {t('all_time', 'All time'): <10}  {t('per_game', 'Per game')}"
            box.add_widget(Label(text=header, size_hint_y=None, height=dp(28), halign="left"))
            box.add_widget(Label(text="─" * 40, size_hint_y=None, height=dp(18), halign="left"))

            for stat, ag, pg in stats["table"]:
                line = f"{stat:<15}  {str(ag):<10}  {'' if pg is None else pg}"
                box.add_widget(Label(text=line, size_hint_y=None, height=dp(26), halign="left"))

            box.add_widget(Label(text="─" * 40, size_hint_y=None, height=dp(18), halign="left"))
            box.add_widget(Label(text=f"{t('games', 'Games')}: {stats['games']}",
                                 size_hint_y=None, height=dp(26), halign="left"))

            if "efficiency" in stats.get("extra", {}):
                box.add_widget(Label(text=f"{t('efficiency', 'Efficiency')}: {stats['extra']['efficiency']}",
                                     size_hint_y=None, height=dp(26), halign="left"))

            sv.add_widget(box)
            root.add_widget(sv)

        back = Button(text="← " + t("menu", "Menu"), size_hint_y=None, height=dp(48))
        back.bind(on_release=lambda *_: setattr(self.manager, "current", "menu"))
        root.add_widget(back)

        self.add_widget(root)


class ExportScreen(Screen):
    def on_enter(self):
        self.render()

    def render(self):
        self.clear_widgets()
        app: "ShowoffKivyApp" = App.get_running_app()
        t = app.state.t
        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))
        root.add_widget(Label(text=t("data_export", "Export"), font_size="20sp",
                              size_hint_y=None, height=dp(56)))

        info = Label(text="", halign="left", valign="top")
        info.bind(size=info.setter('text_size'))
        root.add_widget(info)

        btn = Button(text=t("data_export", "Export") + " → CSV", size_hint_y=None, height=dp(52))
        root.add_widget(btn)

        def do_export(*_):
            try:
                out = core_db.export_to_csv(app.state, app.db)
                info.text = f"OK: {out}"
            except ValueError:
                _popup("Export", t("no_games", "No games"))
            except Exception as e:
                _popup("Export", f"ERROR: {e}")

        btn.bind(on_release=do_export)

        back = Button(text="← " + t("menu", "Menu"), size_hint_y=None, height=dp(48))
        back.bind(on_release=lambda *_: setattr(self.manager, "current", "menu"))
        root.add_widget(back)

        self.add_widget(root)


class SettingsScreen(Screen):
    def on_enter(self):
        self.render()

    def render(self):
        self.clear_widgets()
        app: "ShowoffKivyApp" = App.get_running_app()
        t = app.state.t

        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))
        root.add_widget(Label(text=t("settings", "Settings"), font_size="20sp",
                              size_hint_y=None, height=dp(56)))

        # Storage info
        storage_lbl = Label(text="", halign="left", valign="top")
        storage_lbl.bind(size=storage_lbl.setter("text_size"))
        root.add_widget(storage_lbl)

        is_mobile = kivy_platform in {"android", "ios"}
        if is_mobile:
            storage_lbl.text = (
                    t("storage_mobile", "On mobile, data is always stored in app sandbox.") +
                    f"\n\n{t('data_path', 'Data path')}: {app.state.storage_path}"
            )
        else:
            storage_lbl.text = (
                    f"{t('data_path', 'Data path')}: {app.state.storage_path}\n\n"
                    + t("storage_hint", "Choose where to store JSON/CSV on desktop:")
            )

            row = BoxLayout(orientation="horizontal", spacing=dp(12), size_hint_y=None, height=dp(52))
            btn_app = Button(text=t("storage_app", "App data dir"))
            btn_proj = Button(text=t("storage_project", "Project dir"))
            row.add_widget(btn_app)
            row.add_widget(btn_proj)
            root.add_widget(row)

            def set_mode(mode: str):
                app.set_storage_mode(mode)
                storage_lbl.text = f"{t('data_path', 'Data path')}: {app.state.storage_path}\n\n" + t("storage_hint",
                                                                                                      "Choose where to store JSON/CSV on desktop:")

            btn_app.bind(on_release=lambda *_: set_mode("app"))
            btn_proj.bind(on_release=lambda *_: set_mode("project"))

        back = Button(text="← " + t("menu", "Menu"), size_hint_y=None, height=dp(48))
        back.bind(on_release=lambda *_: setattr(self.manager, "current", "menu"))
        root.add_widget(back)
        self.add_widget(root)


class AddGameScreen(Screen):
    def on_enter(self):
        self.render()

    def render(self):
        self.clear_widgets()
        app: "ShowoffKivyApp" = App.get_running_app()
        t = app.state.t

        game_id = app.edit_game_id
        editing = bool(game_id)
        current_game = core_db.get_game(app.db, game_id) if editing else None

        fields = self._fields_for_sport(app.state.sport, t)

        root = BoxLayout(orientation="vertical", padding=dp(12), spacing=dp(12))
        root.add_widget(Label(text=(t("edit_game", "Edit game") if editing else t("add_game", "Add game")),
                              font_size="20sp", size_hint_y=None, height=dp(56)))

        sv = ScrollView()
        form = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        form.bind(minimum_height=form.setter("height"))

        self.inputs: Dict[str, TextInput] = {}
        for key, label, hint in fields:
            form.add_widget(Label(text=label, size_hint_y=None, height=dp(22), halign="left"))
            ti = TextInput(hint_text=hint, multiline=False, size_hint_y=None, height=dp(44))
            if current_game and key in current_game:
                ti.text = "" if current_game.get(key) is None else str(current_game.get(key))
            self.inputs[key] = ti
            form.add_widget(ti)

        sv.add_widget(form)
        root.add_widget(sv)

        row = BoxLayout(orientation="horizontal", spacing=dp(12), size_hint_y=None, height=dp(52))
        save_btn = Button(text=t("save", "Save") if editing else t("added", "Added"))
        back_btn = Button(text="← " + t("menu", "Menu"))
        row.add_widget(save_btn)
        row.add_widget(back_btn)
        root.add_widget(row)

        def go_back(*_):
            app.edit_game_id = None
            self.manager.current = "menu"

        def do_save(*_):
            game = self._collect_game(app.state.sport)
            game.setdefault("name", "")
            game.setdefault("date", "")

            if editing and current_game:
                ok = core_db.update_game(app.state, app.db, game_id, game)
                if not ok:
                    _popup("Edit", "Not found")
                app.edit_game_id = None
            else:
                core_db.add_game(app.state, app.db, game)
            app.reload_db()
            _popup(t("add_game", "Add game"), (t("saved", "Saved") if editing else t("added", "Added")) + " ✅")
            self.manager.current = "menu"

        save_btn.bind(on_release=do_save)
        back_btn.bind(on_release=go_back)

        self.add_widget(root)

    def _fields_for_sport(self, sport: str, t):
        common = [
            ("name", t("game_name", "Game name"), t("game_name", "Game name")),
            ("date", t("game_date", "Date"), "2026-02-23"),
            ("position", t("game_position", "Position"), ""),
            ("minutes", t("game_minutes", "Minutes"), "0"),
        ]
        if sport == "basketball":
            return common + [
                ("points", t("game_points", "Points"), "0"),
                ("assists", t("game_assists", "Assists"), "0"),
                ("2pt_attempts", t("game_2pta", "2PT attempts"), "0"),
                ("2ptshots_made", t("game_2ptm", "2PT made"), "0"),
                ("3pt_attempts", t("game_3pta", "3PT attempts"), "0"),
                ("3ptshots_made", t("game_3ptm", "3PT made"), "0"),
                ("rebounds", t("game_rebounds", "Rebounds"), "0"),
                ("blocks", t("game_blocks", "Blocks"), "0"),
                ("steals", t("game_steals", "Steals"), "0"),
                ("personal_fouls", t("game_personalfouls", "Personal fouls"), "0"),
                ("missedFT", t("game_missedFT", "Missed FT"), "0"),
                ("turnovers", t("game_turnovers", "Turnovers"), "0"),
                ("Won", t("game_result", "Won (true/false)"), "true"),
            ]
        return common + [
            ("goals", t("game_goals", "Goals"), "0"),
            ("assists", t("game_assists", "Assists"), "0"),
            ("shots", t("game_shots", "Shots"), "0"),
            ("yellow_cards", t("game_yellowcards", "Yellow cards"), "0"),
            ("red_cards", t("game_redcards", "Red cards"), "0"),
            ("fouls", t("game_personalfouls", "Fouls"), "0"),
            ("Won", t("game_result", "Won (true/false)"), "true"),
        ]

    def _collect_game(self, sport: str) -> Dict[str, Any]:
        game: Dict[str, Any] = {}
        for k, ti in self.inputs.items():
            v = (ti.text or "").strip()
            if k in {"minutes", "points", "assists", "2pt_attempts", "2ptshots_made", "3pt_attempts", "3ptshots_made",
                     "rebounds", "blocks", "steals", "personal_fouls", "missedFT", "turnovers", "goals", "shots",
                     "yellow_cards", "red_cards", "fouls"}:
                try:
                    game[k] = int(v) if v != "" else 0
                except Exception:
                    game[k] = 0
            elif k == "Won":
                game[k] = v.lower() in {"1", "true", "yes", "y", "да", "ага"}
            else:
                game[k] = v
        return game


class ShowoffKivyApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.project_dir = Path(__file__).resolve().parents[1]  # .../source
        self.state = AppState(lang="en", sport="basketball", storage_path=Path("").resolve(), config_dir=Path(
            "").resolve())
        self.db: Dict[str, Any] = {"player": "", "games": []}

        # Edit flow
        self.edit_game_id: Optional[str] = None

    def set_storage_mode(self, mode: str) -> None:
        # desktop only
        if kivy_platform in {"android", "ios"}:
            self.state.storage_mode = "app"
        else:
            self.state.storage_mode = mode if mode in {"app", "project"} else "app"

        if self.state.storage_mode == "project":
            self.state.storage_path = self.project_dir.resolve()
        else:
            self.state.storage_path = Path(self.user_data_dir).resolve()

        self.state.save_config()
        self.reload_db()

    def reload_db(self):
        self.db = core_db.load_db(self.state)

    def build(self):
        # config lives in app sandbox always
        self.state.config_dir = Path(self.user_data_dir).resolve()
        self.state.load_config()
        self.state.reload_texts()

        # apply storage mode
        if kivy_platform in {"android", "ios"}:
            self.state.storage_mode = "app"
            self.state.storage_path = Path(self.user_data_dir).resolve()
        else:
            # default = app dir, but allow project dir if configured
            if self.state.storage_mode == "project":
                self.state.storage_path = self.project_dir.resolve()
            else:
                self.state.storage_path = Path(self.user_data_dir).resolve()

        self.state.save_config()
        self.reload_db()

        sm = ScreenManager()
        sm.add_widget(LanguageScreen(name="language"))
        sm.add_widget(SportScreen(name="sport"))
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(AddGameScreen(name="add_game"))
        sm.add_widget(GamesScreen(name="games"))
        sm.add_widget(StatsScreen(name="stats"))
        sm.add_widget(ExportScreen(name="export"))
        sm.add_widget(SettingsScreen(name="settings"))

        # start screen: if config exists, go straight to menu
        if self.state.lang and self.state.sport:
            sm.current = "menu"
        else:
            sm.current = "language"
        return sm


if __name__ == "__main__":
    ShowoffKivyApp().run()
