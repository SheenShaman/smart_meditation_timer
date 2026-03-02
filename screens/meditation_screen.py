from kivy.clock import Clock
from kivy.core.audio import Sound, SoundLoader
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class Sounds:
    def __init__(self):
        self.sound: Sound = (
            SoundLoader.load("assets/sound.mp3") or Sound()
        )  # TODO: Добавить fallback

    def play_sound(self):
        if self.sound is not None:
            self.sound.play()
        else:
            raise ValueError("Звук не был загружен!")


class MeditationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
<<<<<<< HEAD
=======
        self.sounds = Sounds()
>>>>>>> d874412 (added animation circle)
        self.breathing = BreathingController(
            on_text_change=self._on_breathing_text
        )

    def _on_breathing_text(self, text):
        # ids доступны только после построения дерева из KV
        if "breathing_label" in self.ids:
            self.ids.breathing_label.text = text

    def play_sound(self):
        self.sounds.play_sound()

    def on_play_button_press(self, button: Button):
        if self.sounds.sound is not None:
            self.sounds.play_sound()
            if button.text == "Начать":
                button.text = "Пауза"
            elif button.text == "Пауза":
                button.text = "Начать"
            else:
                raise ValueError("Неверное состояние кнопки")


class BreathingController:
    """
    Контроллер дыхательных упражнений: вдох 4 сек, выдох 6 сек.
    """

    INHALE_DURATION = 4.0  # секунды
    EXHALE_DURATION = 6.0  # секунды

    def __init__(self, on_text_change=None):
        self._running = False
        self._clock_event = None
        self._on_text_change = on_text_change  # callback для смены текста

    def inhale(self):
        """Вдох на 4 секунды. Запускает таймер и обновляет текст."""
        self.change_text("Вдох")
        self._clock_event = Clock.schedule_once(
            lambda dt: self._on_inhale_done(), self.INHALE_DURATION
        )

    def exhale(self):
        """Выдох на 6 секунд. Запускает таймер и обновляет текст."""
        self.change_text("Выдох")
        self._clock_event = Clock.schedule_once(
            lambda dt: self._on_exhale_done(), self.EXHALE_DURATION
        )

    def _on_inhale_done(self):
        if self._running:
            self.exhale()

    def _on_exhale_done(self):
        if self._running:
            self.inhale()

    def stop_breathing(self):
        """Останавливает цикл дыхания."""
        self._running = False
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None
        self.change_text("Остановлено")

    def change_text(self, text: str):
        """Меняет отображаемый текст (через callback в UI)."""
        if self._on_text_change:
            self._on_text_change(text)

    def infinity_repeating(self):
        """Запускает бесконечный цикл: вдох → выдох → вдох → ..."""
        self._running = True
        self.inhale()  # начинаем с вдоха
