import time
from enum import Enum

from kivy.clock import Clock
from kivy.core.audio import Sound, SoundLoader
from kivy.properties import BooleanProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class BreathPhase(Enum):
    INHALE = "inhale"
    EXHALE = "exhale"


class SessionState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


class Sounds:
    def __init__(self):
        self.sound_start: Sound | None = SoundLoader.load(
            "assets/sound_start.mp3"
        )
        self.sound_finish: Sound | None = SoundLoader.load(
            "assets/sound_finish.wav"
        )

    def play_start(self):
        if self.sound_start is not None:
            self.sound_start.play()
        else:
            return "Звук не был загружен"

    def play_finish(self):
        if self.sound_finish is not None:
            self.sound_finish.play()
        else:
            return "Звук не был загружен"


class MeditationScreen(Screen):
    show_finish_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
<<<<<<< HEAD
=======
        self.sounds = Sounds()
>>>>>>> d874412 (added animation circle)
        self.breathing = BreathingController(
            on_phase_change=self._on_phase_change,
            on_state_change=self._on_state_change,
        )

    def _on_phase_change(self, phase: BreathPhase, duration: float):
        circle = self.ids.get("circle")
        if not circle:
            return
        if phase == BreathPhase.INHALE:
            circle.animate_inhale(duration)
        elif phase == BreathPhase.EXHALE:
            circle.animate_exhale(duration)

    def _on_state_change(self, state: SessionState):
        circle = self.ids.get("circle")
        if not circle:
            return
        if state == SessionState.PAUSED:
            circle.pause_animation()
        elif state == SessionState.STOPPED:
            circle.stop_animation()

    def on_play_button_press(self, button: Button):
        if button.text == "Начать":
            self.breathing.infinity_repeating()
            self.show_finish_button = True
            button.text = "Пауза"
            self.sounds.play_start()

        elif button.text == "Пауза":
            self.breathing.pause_breathing()

            button.text = "Продолжить"

        elif button.text == "Продолжить":
            self.breathing.resume_breathing()

            button.text = "Пауза"

        else:
            raise ValueError("Неверное состояние кнопки")

    def on_finish_button_press(self):
        self.breathing.stop_breathing()
        self.sounds.play_finish()
        self.show_finish_button = False
        circle = self.ids.get("circle")
        if circle:
            circle.reset_animation()

        play_btn = self.ids.get("play_btn")
        if play_btn:
            play_btn.text = "Начать"

        label = self.ids.get("breathing_label")
        if label:
            label.text = "МЕДИТАЦИЯ"


class BreathingController:
    """
    Контроллер дыхательных упражнений: вдох 4 сек, выдох 6 сек.
    """

    INHALE_DURATION = 4.0  # секунды
    EXHALE_DURATION = 6.0  # секунды

    def __init__(self, on_phase_change=None, on_state_change=None):
        self._running = False
        self._clock_event = None
        self._on_state_change = on_state_change  # callback смены состояния
        self._on_phase_change = on_phase_change  # callback смены фазы
        self._current_phase: BreathPhase = BreathPhase.INHALE
        self._phase_duration: float = self.INHALE_DURATION
        self._phase_started_at: float = 0.0
        self._remaining_duration: float = 0.0

    def inhale(self):
        """Вдох на 4 секунды. Запускает таймер и обновляет текст."""

        if self._on_phase_change:
            self._on_phase_change(BreathPhase.INHALE, self.INHALE_DURATION)

        self._current_phase = BreathPhase.INHALE
        self._phase_duration = self.INHALE_DURATION
        self._phase_started_at = time.monotonic()

        self._clock_event = Clock.schedule_once(
            lambda dt: self._on_inhale_done(), self.INHALE_DURATION
        )

    def exhale(self):
        """Выдох на 6 секунд. Запускает таймер и обновляет текст."""

        if self._on_phase_change:
            self._on_phase_change(BreathPhase.EXHALE, self.EXHALE_DURATION)

        self._current_phase = BreathPhase.EXHALE
        self._phase_duration = self.EXHALE_DURATION
        self._phase_started_at = time.monotonic()

        self._clock_event = Clock.schedule_once(
            lambda dt: self._on_exhale_done(), self.EXHALE_DURATION
        )

    def _on_inhale_done(self):
        if self._running:
            self.exhale()

    def _on_exhale_done(self):
        if self._running:
            self.inhale()

    def pause_breathing(self):
        self._running = False

        elapsed = time.monotonic() - self._phase_started_at
        self._remaining_duration = max(0.0, self._phase_duration - elapsed)

        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None
        if self._on_state_change:
            self._on_state_change(SessionState.PAUSED)

    def resume_breathing(self):
        if self._running:
            return

        remaining = (
            self._remaining_duration
            if self._remaining_duration > 0
            else self._phase_duration
        )
        self._running = True

        if self._on_state_change:
            self._on_state_change(SessionState.RUNNING)

        if self._on_phase_change:
            self._on_phase_change(self._current_phase, remaining)

        if self._current_phase == BreathPhase.INHALE:
            self._clock_event = Clock.schedule_once(
                lambda dt: self._on_inhale_done(), remaining
            )
        else:
            self._clock_event = Clock.schedule_once(
                lambda dt: self._on_exhale_done(), remaining
            )

        self._phase_started_at = time.monotonic()
        self._phase_duration = remaining

    def stop_breathing(self):
        """Останавливает цикл дыхания."""
        self._running = False
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None

        if self._on_state_change:
            self._on_state_change(SessionState.STOPPED)

        self._remaining_duration = 0.0
        self._current_phase = BreathPhase.INHALE
        self._phase_duration = self.INHALE_DURATION

    def infinity_repeating(self):
        """Запускает бесконечный цикл: вдох → выдох → вдох → ..."""
        self._running = True
        self.inhale()  # начинаем с вдоха
