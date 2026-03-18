import math
import time
from typing import Callable, Optional

from kivy.app import App
from kivy.clock import Clock

from app.meditation.states import BreathPhase, SessionState


class BreathingController:
    """
    Контроллер дыхательных упражнений: вдох 4 сек, выдох 6 сек.
    """

    INHALE_DURATION = 4.0  # секунды
    EXHALE_DURATION = 6.0  # секунды

    def __init__(
        self, on_phase_change=None, on_state_change=None, on_timer_tick=None
    ):
        self._running = False
        self._clock_event = None

        self._on_timer_tick = on_timer_tick
        self._session_started_at: float = 0.0
        self._elapsed_before_pause: float = 0.0
        self._timer_event = None
        self._duration_limit_sec: int | None = None
        self._last_emitted_sec = -1
        self._stop_requested = False

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

    def _emit_timer_tick(self):
        if not self._on_timer_tick:
            return

        total = self._elapsed_before_pause
        if self._running and self._session_started_at > 0:
            total += time.monotonic() - self._session_started_at

        if (
            self._duration_limit_sec is not None
            and total >= self._duration_limit_sec
        ):
            self._on_timer_tick(self._duration_limit_sec)
            Clock.schedule_once(lambda dt: self.stop_breathing(), 0)
            return

        self._on_timer_tick(int(total))

    def get_elapsed_seconds(self) -> int:
        """
        Возвращает общее прошедшее время сессии в секундах
        (с учётом пауз).
        """
        total = self._elapsed_before_pause
        if self._running and self._session_started_at > 0:
            total += time.monotonic() - self._session_started_at
        return int(total)

    def set_duration_limit(self, limit_sec: int | None):
        self._duration_limit_sec = limit_sec

    def _start_session_timer(self):
        self._session_started_at = time.monotonic()
        self._last_emitted_sec = -1
        if self._timer_event is None:
            self._timer_event = Clock.schedule_interval(
                lambda dt: self._emit_timer_tick(),
                0,
            )
        self._emit_timer_tick()

    def _pause_session_timer(self):
        if self._session_started_at > 0:
            self._elapsed_before_pause += (
                time.monotonic() - self._session_started_at
            )
        self._session_started_at = 0.0
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None
        self._emit_timer_tick()

    def _stop_session_timer(self):
        if self._timer_event:
            self._timer_event.cancel()
            self._timer_event = None
        self._session_started_at = 0.0
        self._elapsed_before_pause = 0.0
        self._emit_timer_tick()

    def _on_inhale_done(self):
        if self._running:
            self.exhale()

    def _on_exhale_done(self):
        if self._running:
            self.inhale()

    def pause_breathing(self):
        self._running = False
        self._pause_session_timer()

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
        self._start_session_timer()

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
        self._stop_session_timer()
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
        self._start_session_timer()
        if self._on_state_change:
            self._on_state_change(SessionState.RUNNING)
        self.inhale()  # начинаем с вдоха


class Meditation:
    """
    Высокоуровневый контроллер медитации.

    Внутри использует `BreathingController`:
    - следит за временем сессии;
    - предоставляет обратный отсчёт;
    - управляет старт/пауза/завершение;
    - сохраняет результат сессии.
    """

    def __init__(
        self,
        breathing: BreathingController,
        on_countdown: Optional[Callable[[int], None]] = None,
        on_session_saved: Optional[Callable[[dict], None]] = None,
    ):
        self._session_type = None
        self._breathing = breathing
        self._on_countdown = on_countdown
        self._on_session_saved = on_session_saved
        self._target_duration_sec: Optional[int] = None
        self._state: SessionState = SessionState.IDLE

    # 1) ОБРАТНЫЙ ОТСЧЁТ
    def get_countdown(self) -> Optional[int]:
        """
        Возвращает оставшееся время в секундах
        (если лимит не задан, вернёт None).
        """
        if self._target_duration_sec is None:
            return None
        elapsed = self._breathing.get_elapsed_seconds()
        return max(0, self._target_duration_sec - elapsed)

    def update_countdown(self):
        """
        Вызывает callback `on_countdown` с текущим оставшимся временем.
        Предполагается вызывать из обработчика тика таймера.
        """
        if not self._on_countdown:
            return
        remaining = self.get_countdown()
        if remaining is not None:
            self._on_countdown(remaining)

    # 2) СТАРТ
    def start(
        self, duration_limit_sec: Optional[int] = None, session_type: int = 1
    ):
        """
        Запускает медитацию:
        - запоминает целевую длительность (для обратного отсчёта);
        - настраивает лимит в `BreathingController`;
        - запускает дыхание.
        """
        self._target_duration_sec = duration_limit_sec
        self._session_type = session_type
        self._breathing.set_duration_limit(duration_limit_sec)
        self._state = SessionState.RUNNING
        self._breathing.infinity_repeating()

    # 3) ПАУЗА
    def pause(self):
        """Ставит медитацию на паузу."""
        if self._state != SessionState.RUNNING:
            return
        self._breathing.pause_breathing()
        self._state = SessionState.PAUSED

    # 4) ЗАВЕРШЕНИЕ
    def finish(self):
        """
        Останавливает медитацию и сохраняет результат.
        """
        if self._state in (SessionState.IDLE, SessionState.STOPPED):
            return

        self._breathing.stop_breathing()
        duration_sec = self._breathing.get_elapsed_seconds()
        self._state = SessionState.STOPPED
        self.save_session(duration_sec)

    # 5) СВЯЗКА ТАЙМЕР + ДЫХАНИЕ реализована через `BreathingController`,
    #    а этот класс добавляет поверх логику сессии и отслеживание времени.

    # 6) СОХРАНЕНИЕ СЕССИИ
    def save_session(self, duration_sec: int):
        """
        Сохраняет сессию в хранилище:
        - добавляет запись в `sessions`;
        - обновляет суммарные минуты в `stats.total_minutes`.
        """
        app = App.get_running_app()
        store = app.store
        minutes = max(1, math.ceil(duration_sec / 60))

        session_type = getattr(self, "_session_type", 1)
        session = store.new_session(minutes, session_type)

        if self._on_session_saved:
            self._on_session_saved(session)
