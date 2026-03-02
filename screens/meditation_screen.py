from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen

from app.meditation.controller import BreathingController
from app.meditation.states import BreathPhase, SessionState
from services.sounds import Sounds


class MeditationScreen(Screen):
    show_finish_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_state = SessionState.IDLE
        self.sounds = Sounds()
        self.breathing = BreathingController(
            on_phase_change=self._on_phase_change,
            on_state_change=self._on_state_change,
            on_timer_tick=self._on_timer_tick,
        )

    def _on_timer_tick(self, total_sec: int):
        label = self.ids.get("timer_label")
        if not label:
            return
        mm, ss = divmod(total_sec, 60)
        label.text = f"{mm:02d}:{ss:02d}"

    def _on_phase_change(self, phase: BreathPhase, duration: float):
        circle = self.ids.get("circle")
        if not circle:
            return
        if phase == BreathPhase.INHALE:
            circle.animate_inhale(duration)
        elif phase == BreathPhase.EXHALE:
            circle.animate_exhale(duration)

    def _on_state_change(self, state: SessionState):
        self.session_state = state

        if state == SessionState.RUNNING:
            self._apply_running_state()
        elif state == SessionState.PAUSED:
            self._apply_paused_state()
        elif state in (SessionState.IDLE, SessionState.STOPPED):
            self._apply_stopped_state()

    def _apply_running_state(self):
        self.show_finish_button = True
        play_btn = self.ids.get("play_btn")
        if play_btn:
            play_btn.text = "Пауза"

    def _apply_paused_state(self):
        circle = self.ids.get("circle")
        play_btn = self.ids.get("play_btn")
        label = self.ids.get("breathing_label")

        if circle:
            circle.pause_animation()
        if play_btn:
            play_btn.text = "Продолжить"
        if label:
            label.text = "Пауза"

    def _apply_stopped_state(self):
        self.show_finish_button = False
        circle = self.ids.get("circle")
        play_btn = self.ids.get("play_btn")
        label = self.ids.get("breathing_label")

        if circle:
            circle.reset_animation()
        if play_btn:
            play_btn.text = "Начать"
        if label:
            label.text = "МЕДИТАЦИЯ"

    def on_play_button_press(self, _button):
        if self.session_state in (SessionState.IDLE, SessionState.STOPPED):
            self.breathing.infinity_repeating()
            self.sounds.play_start()
        elif self.session_state == SessionState.RUNNING:
            self.breathing.pause_breathing()
        elif self.session_state == SessionState.PAUSED:
            self.breathing.resume_breathing()

    def on_finish_button_press(self):
        self.breathing.stop_breathing()
        self.sounds.play_finish()
