from kivy.app import App
from kivy.config import Config
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from screens import MeditationScreen, SettingsScreen, StatsScreen
from core.theme import Theme

Config.set("kivy", "log_level", "debug")

Factory.register("MeditationScreen", cls=MeditationScreen)
Factory.register("StatsScreen", cls=StatsScreen)
Factory.register("SettingsScreen", cls=SettingsScreen)


class RootManager(ScreenManager):
    pass


class MeditationApp(App):
    """
    Meditation App
    """
    theme = Theme()

    def build_config(self, config):
        config.setdefaults('graphics', {
            'width': '400',
            'height': '600',
            'maxfps': '60',
            'resizable': '0'
        })

    def build(self):
        Builder.load_file("meditation.kv")
        return RootManager()


if __name__ == "__main__":
    MeditationApp().run()
