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
