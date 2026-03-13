from kivy.storage.jsonstore import JsonStore
from screens.base_screen import BaseScreen
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
from kivy.app import App
from kivy.animation import Animation
from kivy.factory import Factory


class SettingsScreen(BaseScreen):
    sounds = BooleanProperty(True)
    weekly_goal = NumericProperty(100)
    rotation = NumericProperty(0)

    def on_pre_enter(self):
        if not hasattr(self, "_settings_loaded"):
            self.load_settings()
            self._settings_loaded = True

    def load_settings(self):
        store = JsonStore("app_data.json")
        if store.exists("settings"):
            settings = store.get("settings")

            self.sounds = settings.get("sounds", True)
            self.weekly_goal = settings.get("weekly_goal", 100)

            theme_mode = settings.get("theme", "dark")
            app_theme = App.get_running_app().theme
            if theme_mode == "dark":
                app_theme.set_dark()
            else:
                app_theme.set_light()

    def save_settings(self):
        store = JsonStore("app_data.json")
        app = App.get_running_app()
        store.put(
            "settings",
            weekly_goal=self.weekly_goal,
            sounds=self.sounds,
            theme=app.theme.mode,
        )

        app.sounds_enabled = self.sounds
        Factory.FinishPopup(title="Настройки сохранены").open()

    def reset_settings(self):
        self.weekly_goal = 100
        self.sounds = True
        theme = App.get_running_app().theme
        theme.set_dark()

    def toggle_theme(self):
        self.rotation += 180
        Animation(rotation=self.rotation, duration=0.25).start(self)
        theme = App.get_running_app().theme
        if theme.mode == "dark":
            theme.set_light()
        else:
            theme.set_dark()
