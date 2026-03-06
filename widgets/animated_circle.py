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
    Круг = 31 день выбранного месяца
    31 равный сектор = 31 день
    Цвет сектора = тип медитации за этот день:
      0 - нет
      1 - синяя
      2 - фиолетовая
      3 - розовая
    """

    data = ListProperty([])
    appear = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.data = [0] * 31
        self._segment_colors = []
        self._segments = []
        self._scheduled = False

        if self.canvas is None:
            return

        # ВАЖНО: это ДОЛЖНО быть внутри __init__ (поэтому self доступен)
        with self.canvas.before:
            for _ in range(31):
                c = Color(0.10, 0.10, 0.13, 0.25)
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
        days = list(days)[:31]
        if len(days) < 31:
            days += [0] * (31 - len(days))
        self.data = days
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

        days = list(self.data)[:31]
        if len(days) < 31:
            days += [0] * (31 - len(days))

        radius = 0.42 * min(self.width, self.height)
        diameter = radius * 2
        pos = (self.center_x - radius, self.center_y - radius)

        sector = 360.0 / 31.0

        max_angle = 360.0 * float(self.appear)
        drawn = 0.0

        start = 0.0
        i = -1

        for idx in range(31):
            remaining = max_angle - drawn
            if remaining <= 0:
                break

            sweep = min(sector, remaining)
            drawn += sweep

            r, g, b, a = self._color_for_type(int(days[idx]))
            self._segment_colors[idx].rgba = (r, g, b, a)

            self._segments[idx].pos = pos
            self._segments[idx].size = (diameter, diameter)
            self._segments[idx].angle_start = start
            self._segments[idx].angle_end = start + sweep

            start += sector
            i = idx

        # остальные спрячем
        for j in range(i + 1, 31):
            self._segment_colors[j].rgba = (0, 0, 0, 0)
            self._segments[j].angle_start = 0
            self._segments[j].angle_end = 0
            self._segments[j].pos = pos
            self._segments[j].size = (diameter, diameter)