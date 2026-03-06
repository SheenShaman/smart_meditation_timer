from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class StatsScreen(Screen):
    def on_enter(self, *args):
        # Обновление диаграммы после входа на экран
        Clock.schedule_once(self._update_chart, 0)

    def _update_chart(self, *_):
        chart = self.ids.get("pie_chart")
        if not chart:
            return

        # ТЕСТ по комментарию: 31 день = 31 сектор
        # 15 розовых, 10 синих, 6 фиолетовых
        days = [3] * 15 + [1] * 10 + [2] * 6

        chart.set_data(days)
