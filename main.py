from kivy.app import App
from kivy.config import Config
from kivy.factory import Factory
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from core.theme import Theme
from data.datastore import DataStore
from screens import BaseScreen, MeditationScreen, SettingsScreen, StatsScreen  # noqa
from widgets import AnimatedCircle
from services.sounds import Sounds

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

    def build(self):
        self.store = DataStore()
        self.store.init()

        self.sounds = Sounds(enabled=True)
        self.theme = Theme(mode="dark")

        self.apply_settings()

        Builder.load_file("ui/root.kv")
        return RootManager()


if __name__ == "__main__":
    MeditationApp().run()
