from kivy.app import App
from kivy.config import Config
from kivy.factory import Factory
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager

from core.theme import Theme
from screens import MeditationScreen, SettingsScreen, StatsScreen

Config.set("kivy", "log_level", "debug")

Factory.register("MeditationScreen", cls=MeditationScreen)
Factory.register("StatsScreen", cls=StatsScreen)
Factory.register("SettingsScreen", cls=SettingsScreen)


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

    theme = Theme()

    def build_config(self, config):
        config.setdefaults(
            "graphics",
            {"width": "400", "height": "600", "maxfps": "60", "resizable": "0"},
        )

    def build(self):
        return RootManager()


if __name__ == "__main__":
    MeditationApp().run()
