from kivy.clock import Clock
from screens.base_screen import BaseScreen
from kivy.properties import DictProperty, StringProperty


class StatsScreen(BaseScreen):
    selected_month = StringProperty("Март")

    month_data = DictProperty(
        {
            "Январь": [1] * 10 + [2] * 7 + [3] * 14,
            "Февраль": [1] * 8 + [2] * 6 + [3] * 14,
            "Март": [3] * 15 + [1] * 10 + [2] * 6,
            "Апрель": [1] * 9 + [2] * 10 + [3] * 11,
            "Май": [1] * 6 + [2] * 11 + [3] * 14,
            "Июнь": [1] * 12 + [2] * 10 + [3] * 8,
            "Июль": [1] * 11 + [2] * 5 + [3] * 15,
            "Август": [1] * 9 + [2] * 12 + [3] * 10,
            "Сентябрь": [1] * 7 + [2] * 13 + [3] * 10,
            "Октябрь": [1] * 8 + [2] * 9 + [3] * 14,
            "Ноябрь": [1] * 6 + [2] * 10 + [3] * 14,
            "Декабрь": [1] * 5 + [2] * 11 + [3] * 15,
        }
    )

    def on_enter(self, *args):
        Clock.schedule_once(self._update_chart, 0)

    def _update_chart(self, *_):
        chart = self.ids.get("pie_chart")
        if not chart:
            return

        days = self.month_data.get(self.selected_month, [])
        chart.set_data(days)

    def on_month_selected(self, month_name):
        self.selected_month = month_name
        Clock.schedule_once(self._update_chart, 0)
