from kivy.factory import Factory
from kivy.properties import BooleanProperty, ListProperty
from app.meditation.controller import BreathingController, Meditation
from app.meditation.states import BreathPhase, SessionState
from screens.base_screen import BaseScreen
from kivy.app import App

DURATION_PRESETS = {
    "10 сек": 10,
    "5 мин": 5 * 60,
    "10 мин": 10 * 60,
    "Свободная": None,
}


class MeditationScreen(BaseScreen):
    show_finish_button = BooleanProperty(False)
    duration_options = ListProperty(list(DURATION_PRESETS))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_state = SessionState.IDLE
        self.sounds = App.get_running_app().sounds
        self._selected_duration_sec = None
        self.breathing = BreathingController(
            on_phase_change=self._on_phase_change,
            on_state_change=self._on_state_change,
            on_timer_tick=self._on_timer_tick,
        )
        self.meditation = Meditation(
            breathing=self.breathing,
            on_countdown=self._on_countdown,
        )

    def _on_timer_tick(self, total_sec: int):
        # тик низкоуровневого таймера дыхания
        # обновляем обратный отсчёт (если есть лимит)
        self.meditation.update_countdown()

        # если лимита нет (режим "Свободная") — показываем прошедшее время
        if self.meditation.get_countdown() is None:
            label = self.ids.get("timer_label")
            if not label:
                return
            mm, ss = divmod(total_sec, 60)
            label.text = f"{mm:02d}:{ss:02d}"

    def _on_countdown(self, remaining_sec: int):
        """Обновление лейбла таймера при обратном отсчёте."""
        label = self.ids.get("timer_label")
        if not label:
            return
        mm, ss = divmod(remaining_sec, 60)
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
            self.sounds.play_start()
        elif state == SessionState.PAUSED:
            self._apply_paused_state()
        elif state in (SessionState.IDLE, SessionState.STOPPED):
            self._apply_stopped_state()
            self._show_finish_popup()
            self.sounds.play_finish()

    def on_duration_mode_change(self, mode_text: str):
        self._selected_duration_sec = DURATION_PRESETS.get(mode_text, None)
        # заодно передаём лимит и в дыхательный контроллер
        self.breathing.set_duration_limit(self._selected_duration_sec)

    def _apply_running_state(self):
        self.show_finish_button = True
        play_btn = self.ids.get("play_btn")
        if play_btn:
            play_btn.text = "Пауза"

    def _show_finish_popup(self):
        Factory.FinishPopup(title="Отличная работа").open()

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
            # запускаем медитацию через высокоуровневый контроллер
            self.meditation.start(self._selected_duration_sec)
        elif self.session_state == SessionState.RUNNING:
            # ставим на паузу
            self.meditation.pause()
        elif self.session_state == SessionState.PAUSED:
            # продолжаем дыхание напрямую (возобновление сессии)
            self.breathing.resume_breathing()

    def on_finish_button_press(self):
        # завершение медитации и сохранение сессии
        self.meditation.finish()
