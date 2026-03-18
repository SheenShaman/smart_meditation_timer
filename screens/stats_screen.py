from calendar import monthrange
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.label import Label

from data.statistics import Statistics
from screens.base_screen import BaseScreen


class StatsScreen(BaseScreen):
    selected_month = StringProperty("Март")

    def on_enter(self, *args):
        Clock.schedule_once(self._update_chart, 0)

    def _update_chart(self, *_):
        app = App.get_running_app()
        store = app.store

        stats = Statistics()
        stats.data = store.get_data()
        stats.sessions = store.get_sessions()

        # фильтр по месяцу
        month_index = [
            "Январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь",
        ].index(self.selected_month) + 1

        filtered = []
        for s in stats.sessions:
            dt = datetime.strptime(s["date"], "%Y-%m-%d")
            if dt.month == month_index:
                filtered.append(s)

        year = datetime.now().year
        days_in_month = monthrange(year, month_index)[1]
        days_map = [0] * days_in_month

        for s in filtered:
            dt = datetime.strptime(s["date"], "%Y-%m-%d")
            days_map[dt.day - 1] = s["type"]
        self.ids.pie_chart.set_data(days_map)

        stats.sessions = filtered
        week = stats.group_day()
        self._update_week_ui(week)

        best_name, best_minutes = stats.best_day(week)
        self.ids.best_day_label.text = f"Лучший день: {best_name}"
        self.ids.best_day_time.text = f"{best_minutes} мин"

        total = sum(s["minutes"] for s in filtered)
        self.ids.total_label.text = (
            f"Общее время: {total // 60} ч {total % 60} мин"
        )

    def _update_week_ui(self, week_data):
        container = self.ids.week_values_row
        container.clear_widgets()

        for day in week_data.values():
            container.add_widget(Label(text=str(day)))

    def on_month_selected(self, month_name):
        self.selected_month = month_name
        Clock.schedule_once(self._update_chart, 0)
