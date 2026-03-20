from kivy.core.audio import Sound, SoundLoader
from kivy.app import App


class Sounds:
    def __init__(self, enabled: bool):
        self.enabled = enabled
        app = App.get_running_app()

        self.sound_start: Sound | None = SoundLoader.load(
            app.assets("sound_start.mp3")
        )
        self.sound_finish: Sound | None = SoundLoader.load(
            app.assets("sound_finish.wav")
        )
        self.sound_click: Sound | None = SoundLoader.load(
            app.assets("sound_click.wav")
        )

    def play_start(self):
        if not self.enabled:
            return
        if self.sound_start is not None:
            self.sound_start.play()
        else:
            return "Звук не был загружен"

    def play_finish(self):
        if not self.enabled:
            return
        if self.sound_finish is not None:
            self.sound_finish.play()
        else:
            return "Звук не был загружен"

    def play_click(self):
        if not self.enabled:
            return
        if self.sound_click is not None:
            self.sound_click.play()
        else:
            return "Звук не был загружен"
