from screens.base_screen import BaseScreen
from kivy.properties import BooleanProperty, NumericProperty
from kivy.app import App
from kivy.animation import Animation
from kivy.factory import Factory


class SettingsScreen(BaseScreen):
    sounds = BooleanProperty(True)
    weekly_goal = NumericProperty(100)
    rotation = NumericProperty(0)

    def on_pre_enter(self):
        self.load_settings()

    def load_settings(self):
        app = App.get_running_app()
        settings = app.store.get_settings()

        self.sounds = settings.get("sounds", True)
        self.weekly_goal = settings.get("weekly_goal", 100)

    def save_settings(self):
        app = App.get_running_app()
        data = app.store.get_data()

        data["settings"]["sounds"] = self.sounds
        data["settings"]["weekly_goal"] = self.weekly_goal
        data["settings"]["theme"] = app.theme.mode
        app.store.save()
        app.apply_settings()
        Factory.FinishPopup(title="Настройки сохранены").open()

    def reset_settings(self):
        self.weekly_goal = 100
        self.sounds = True
        theme = App.get_running_app().theme
        theme.set_dark()
        self.save_settings()

    def toggle_theme(self):
        self.rotation += 180
        Animation(rotation=self.rotation, duration=0.25).start(self)
        theme = App.get_running_app().theme
        if theme.mode == "dark":
            theme.set_light()
        else:
            theme.set_dark()
