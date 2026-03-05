from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget


class StatsScreen(Screen):
    def on_enter(self, *args):
        self.clear_widgets()
        self.add_widget(PieChartMonth())


class PieChartMonth(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(self.draw, 0)

    def _calculate_chart_geometry(self):
        chart_radius = 0.30 * min(self.width, self.height)
        chart_diameter = chart_radius * 2

        chart_center_x = self.center_x
        chart_center_y = self.center_y

        chart_pos_x = chart_center_x - chart_radius
        chart_pos_y = chart_center_y - chart_radius

        return chart_pos_x, chart_pos_y, chart_diameter

    def draw(self, *args):
        self.canvas.clear()

        if self.width <= 0 or self.height <= 0:
            return

        chart_pos_x, chart_pos_y, chart_diameter = self._calculate_chart_geometry()

        with self.canvas:
            Color(1, 0, 0, 1)
            Ellipse(
                pos=(chart_pos_x, chart_pos_y),
                size=(chart_diameter, chart_diameter)
            )