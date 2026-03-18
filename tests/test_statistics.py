import json
import pytest
from data.statistics import Statistics, StatisticsErrors
from data.datastore import DataStore


class TestStatistics:
    """
    Тестирует класс Statistics
    """

    def test_init(self):
        """
        Тестируем инициализацию
        """
        statistic = Statistics()
        assert statistic.file_name == "app_data.json"

    def test_load(self, tmp_path):
        """
        Тестируем загрузку данных
        """
        test_file = tmp_path / "app_data.json"
        test_data = {
            "sessions": [
                {"date": "2025-03-15", "minutes": 30},
                {"date": "2025-03-14", "minutes": 20},
            ]
        }
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        store = DataStore(str(test_file))

        class TestableStatistics(Statistics):
            def __init__(self, store):
                self.store = store
                self.data = None
                self.sessions = []

        stats = TestableStatistics(store)
        result = stats.load_data()

        assert result is True
        assert len(stats.sessions) == 2
        assert stats.sessions[0]["minutes"] == 30

    def test_load_empty_sessions(self, tmp_path):
        """
        Тест на случай отсутствие сессии
        """
        test_file = tmp_path / "app_data.json"
        test_data = {"sessions": []}

        with open(test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)

        store = DataStore(str(test_file))

        class TestableStatistics(Statistics):
            def __init__(self, store):
                self.store = store
                self.data = None
                self.sessions = []

        stats = TestableStatistics(store)

        with pytest.raises(StatisticsErrors) as exc_info:
            stats.load_data()

        assert "Загрузите сессию" in str(exc_info.value)

    def test_total_minutes(self):
        """
        Тестирует метод, который высчитывает итого количество минут со всех сессий
        """
        stats = Statistics()
        stats.sessions = [{"minutes": 30}, {"minutes": 20}, {"minutes": 45}]
        assert stats.total_minute() == 95

    def test_total_minutes_empty(self):
        """
        Если сессии отсутствуют
        """
        stats = Statistics()
        stats.sessions = [{"minutes": 0}, {"minutes": 0}, {"minutes": 0}]
        assert stats.total_minute() == 0

    def test_group_day_different_days(self):
        """
        Тест если сессии в разные дни
        """
        stats = Statistics()
        stats.sessions = [
            {"date": "2025-03-15", "minutes": 30},
            {"date": "2025-03-16", "minutes": 20},
            {"date": "2025-03-17", "minutes": 45},
        ]
        result = stats.group_day()

        expected = {
            "Понедельник": 45,
            "Вторник": 0,
            "Среда": 0,
            "Четверг": 0,
            "Пятница": 0,
            "Суббота": 30,
            "Воскресенье": 20,
        }
        assert result == expected

    def test_group_day_empty_sessions(self):
        """
        Тестирует, когда нет сессий
        """
        stats = Statistics()
        stats.sessions = [
            {"date": "2025-03-15", "minutes": 0},
            {"date": "2025-03-16", "minutes": 0},
            {"date": "2025-03-17", "minutes": 0},
            {"date": "2025-03-18", "minutes": 0},
            {"date": "2025-03-19", "minutes": 0},
            {"date": "2025-03-20", "minutes": 0},
            {"date": "2025-03-21", "minutes": 0},
        ]
        expected = {
            "Понедельник": 0,
            "Вторник": 0,
            "Среда": 0,
            "Четверг": 0,
            "Пятница": 0,
            "Суббота": 0,
            "Воскресенье": 0,
        }
        result = stats.group_day()
        assert result == expected
