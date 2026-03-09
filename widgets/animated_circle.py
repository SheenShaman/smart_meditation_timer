from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class AnimatedCircle(Widget):
    radius = NumericProperty(40)
    dot_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text="Вдох", color="black")
        self.label.halign = "center"
        self.label.bind(  # pyright: ignore
            size=lambda *_: setattr(self.label, "text_size", self.label.size)
        )
        self.add_widget(self.label)
        self._update_label()

        if self.canvas is None:
            return
        with self.canvas.before:
            self._ring_color = Color()
            self._ring = Line(
                circle=(self.center_x, self.center_y, self.radius), width=1.5
            )

            self._color = Color(*self.dot_color)
            self._ellipse = Ellipse()

        self.bind(  # pyright: ignore
            pos=self._redraw,
            size=self._redraw,
            center=self._redraw,
            radius=self._redraw,
            dot_color=self._on_color,
        )

        Clock.schedule_once(lambda dt: self._redraw(), 0)

    def animate_inhale(self, duration: float):
        Animation.cancel_all(self, "radius")
        animation = Animation(radius=70, duration=duration)
        animation.bind(on_start=lambda *_: self._set_phase("Вдох"))
        animation.start(self)

    def animate_exhale(self, duration: float):
        Animation.cancel_all(self, "radius")
        animation = Animation(radius=40, duration=duration)
        animation.bind(on_start=lambda *_: self._set_phase("Выдох"))
        animation.start(self)

    def pause_animation(self):
        Animation.cancel_all(self, "radius")
        self._set_phase("Пауза")

    def stop_animation(self):
        Animation.cancel_all(self, "radius")

    def reset_animation(self):
        Animation.cancel_all(self, "radius")
        self.radius = 40
        self._set_phase("Вдох")

    def _redraw(self, *_):
        d = self.radius * 2

        self._ring.circle = (self.center_x, self.center_y, 70)

        self._ellipse.size = (d, d)
        self._ellipse.pos = (
            self.center_x - self.radius,
            self.center_y - self.radius,
        )
        self._update_label()

    def _on_color(self, *_):
        self._color.rgba = self.dot_color

    def _set_phase(self, text: str):
        self.label.text = text

    def _update_label(self, *_):
        self.label.center = self.center

class PieChartMonth(Widget):
    """
    Круговая диаграмма по типам медитации за месяц.

    data = список дней месяца:
    0 - нет
    1 - синяя / быстрая
    2 - фиолетовая / короткая
    3 - розовая / глубокая

    Диаграмма суммирует количество каждого типа
    и рисует 3 итоговых сектора.
    """

    data = ListProperty([])
    appear = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.data = []
        self._segment_colors = []
        self._segments = []
        self._scheduled = False

        with self.canvas.before:
            for _ in range(3):
                c = Color(0, 0, 0, 0)
                e = Ellipse()
                self._segment_colors.append(c)
                self._segments.append(e)

        self.bind(  # pyright: ignore
            pos=self._schedule_redraw,
            size=self._schedule_redraw,
            center=self._schedule_redraw,
            data=self._schedule_redraw,
            appear=self._schedule_redraw,
        )

        Clock.schedule_once(lambda *_: self._start_appear(), 0)

    def set_data(self, days):
        self.data = list(days)
        self._start_appear()
        self._schedule_redraw()

    def _start_appear(self, *_):
        if self.width <= 0 or self.height <= 0:
            Clock.schedule_once(self._start_appear, 0.05)
            return

        Animation.cancel_all(self, "appear")
        self.appear = 0.0
        Animation(appear=1.0, duration=0.35, t="out_quad").start(self)

    def _schedule_redraw(self, *_):
        if self._scheduled:
            return
        self._scheduled = True
        Clock.schedule_once(self._redraw, 0)

    def _color_for_type(self, t: int):
        if t == 1:
            return (0.40, 0.46, 0.92, 0.95)  # синяя
        if t == 2:
            return (0.46, 0.30, 0.73, 0.95)  # фиолетовая
        if t == 3:
            return (0.91, 0.33, 0.38, 0.95)  # розовая
        return (0.10, 0.10, 0.13, 0.25)      # пусто

    def _redraw(self, *_):
        self._scheduled = False

        if self.width <= 0 or self.height <= 0:
            return

        days = list(self.data)
        if not days:
            return

        fast_count = sum(1 for day in days if day == 1)
        short_count = sum(1 for day in days if day == 2)
        deep_count = sum(1 for day in days if day == 3)

        total_count = fast_count + short_count + deep_count
        if total_count == 0:
            for idx in range(3):
                self._segment_colors[idx].rgba = (0, 0, 0, 0)
                self._segments[idx].angle_start = 0
                self._segments[idx].angle_end = 0
                self._segments[idx].pos = pos
                self._segments[idx].size = (diameter, diameter)
            return

        radius = 0.42 * min(self.width, self.height)
        diameter = radius * 2
        pos = (self.center_x - radius, self.center_y - radius)

        parts = [
            (fast_count, self._color_for_type(1)),
            (short_count, self._color_for_type(2)),
            (deep_count, self._color_for_type(3)),
        ]

        max_angle = 360.0 * float(self.appear)
        start_angle = 0.0

        for idx in range(3):
            self._segment_colors[idx].rgba = (0, 0, 0, 0)
            self._segments[idx].angle_start = 0
            self._segments[idx].angle_end = 0
            self._segments[idx].pos = pos
            self._segments[idx].size = (diameter, diameter)

        for idx, (value, color) in enumerate(parts):
            if value <= 0:
                self._segment_colors[idx].rgba = (0, 0, 0, 0)
                self._segments[idx].angle_start = 0
                self._segments[idx].angle_end = 0
                self._segments[idx].pos = pos
                self._segments[idx].size = (diameter, diameter)
                continue

            full_sweep = 360.0 * value / total_count
            visible_sweep = min(full_sweep, max(0.0, max_angle - start_angle))

            self._segment_colors[idx].rgba = color
            self._segments[idx].pos = pos
            self._segments[idx].size = (diameter, diameter)
            self._segments[idx].angle_start = start_angle
            self._segments[idx].angle_end = start_angle + visible_sweep

            start_angle += full_sweep
