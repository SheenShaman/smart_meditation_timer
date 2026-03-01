from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class MeditationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.breathing = BreathingController(on_text_change=self._on_breathing_text)

    def _on_breathing_text(self, text):
        # ids доступны только после построения дерева из KV
        if "breathing_label" in self.ids:
            self.ids.breathing_label.text = text


class BreathingController:
    """
    Контроллер дыхательных упражнений: вдох 4 сек, выдох 6 сек.
    """

    INHALE_DURATION = 4.0   # секунды
    EXHALE_DURATION = 6.0   # секунды

    def __init__(self, on_text_change=None):
        self._running = False
        self._clock_event = None
        self._on_text_change = on_text_change  # callback для смены текста

    def vdoh(self):
        """Вдох на 4 секунды. Запускает таймер и обновляет текст."""
        self.change_text("Вдох")
        self._clock_event = Clock.schedule_once(
            lambda dt: self._on_inhale_done(),
            self.INHALE_DURATION
        )

    def vydoch(self):
        """Выдох на 6 секунд. Запускает таймер и обновляет текст."""
        self.change_text("Выдох")
        self._clock_event = Clock.schedule_once(
            lambda dt: self._on_exhale_done(),
            self.EXHALE_DURATION
        )

    def _on_inhale_done(self):
        if self._running:
            self.vydoch()

    def _on_exhale_done(self):
        if self._running:
            self.vdoh()

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
        self.vdoh()  # начинаем с вдоха