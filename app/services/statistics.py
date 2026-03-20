from datetime import datetime

from app.data.datastore import DataStore


class StatisticsErrors(Exception):
    pass


class Statistics:
    """
    Класс для подсчета статистики
    """

    def __init__(self) -> None:
        """
        Создает объект статистики
        """
        self.store = DataStore()  # создаем объект для работы с файлом
        self.data = None  # место для данных (пока пусто)
        self.sessions = []  # место для сессий (пока пусто)

    def load_data(self) -> bool:
        """
        Загружает данные из файла и проверяет все основные виды исключений
        """
        self.data = self.store.load()
        self.sessions = self.data.get("sessions", [])

        if not self.sessions:
            raise StatisticsErrors("Загрузите сессию")

        return True

    def total_minute(self) -> float:
        """
        Считает общее количество минут
        """
        total = 0
        for session in self.sessions:
            total += session["minutes"]
        return total

    def group_day(self) -> dict:
        """
        Группирует по дням недели
        """
        weekdays = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье",
        }

        result = {}
        for day in weekdays.values():
            result[day] = 0
        for session in self.sessions:
            try:
                session_date = datetime.strptime(session["date"], "%Y-%m-%d")
                weekday_num = session_date.weekday()
                weekday_name = weekdays[weekday_num]
                result[weekday_name] += session["minutes"]
            except (KeyError, ValueError) as e:
                raise ValueError(f"Ошибка в сессии {session}: {e}")
        return result

    def best_day(self, weekday_stats: dict) -> tuple:
        """
        Выбирает лучший день
        """
        has_data = any(minutes > 0 for minutes in weekday_stats.values())
        if not has_data:
            return "—", 0

        best_day = max(weekday_stats.items(), key=lambda x: x[1])
        return best_day[0], best_day[1]

    def average_duration(self, total_minutes: float) -> float:
        """
        Считает среднюю длительность
        """
        return round(total_minutes / len(self.sessions), 1)

    def calculate(self) -> dict:
        """
        Считаем всю статистику
        """
        self.load_data()

        total_minutes = self.total_minute()
        weeks_status = self.group_day()
        best_day, best_minutes = self.best_day(weeks_status)
        average_duration = self.average_duration(total_minutes)
        return {
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 1),
            "sessions_count": len(self.sessions),
            "avg_duration": average_duration,
            "by_weekday": weeks_status,
            "best_day": {"name": best_day, "minutes": best_minutes},
        }
