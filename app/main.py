import sys
from pathlib import Path

from kivy.app import App
from kivy.config import Config
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager

from app.services.theme import Theme
from app.data.datastore import DataStore
from app.screens import (  # noqa
    BaseScreen,
    MeditationScreen,
    SettingsScreen,
    StatsScreen,
)
from app.services.sounds import Sounds
from app.widgets import AnimatedCircle

Config.set("kivy", "log_level", "debug")
Config.set("graphics", "multisamples", "8")
Config.set("input", "mouse", "mouse,disable_multitouch")

Factory.register("AnimatedCircle", cls=AnimatedCircle)


class RootManager(ScreenManager):
    """
    Менеджер экранов, отвечает за навигацию
    """

    current_screen_name = StringProperty("meditation")

    def switch(self, screen_name: str):
        if screen_name in self.screen_names:
            self.current = screen_name
            self.current_screen_name = screen_name


class MeditationApp(App):
    """
    Meditation App
    """

    sounds_enabled = BooleanProperty(True)

    def build_config(self, config):
        config.setdefaults(
            "graphics",
            {"width": "400", "height": "600", "maxfps": "60", "resizable": "0"},
        )

    def apply_settings(self):
        settings = self.store.get_settings()

        self.sounds_enabled = settings.get("sounds", True)
        self.sounds.enabled = self.sounds_enabled

        theme_mode = settings.get("theme", "dark")
        if theme_mode == "dark":
            self.theme.set_dark()
        else:
            self.theme.set_light()

    def load_all_kv(self):
        base = self.resource_path("ui")
        files = sorted(base.rglob("*.kv"))
        for path in files:
            Builder.load_file(str(path))

    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS) / relative_path
        return Path(__file__).parent / relative_path

    def get_asset(self, name):
        return str(self.resource_path(f"assets/{name}"))

    def build(self):
        self.assets = self.get_asset
        self.store = DataStore()
        self.sounds = Sounds(enabled=True)
        self.theme = Theme(mode="dark")
        self.apply_settings()
        self.load_all_kv()
        return RootManager()


if __name__ == "__main__":
    MeditationApp().run()
