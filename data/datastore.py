import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "app_data.json"
DEFAULT_DATA = {
    "sessions": [],
    "settings": {
        "sounds": True,
        "theme": "dark",
        "weekly_goal": 200,
    },
    "stats": {
        "total_minutes": 0,
    },
}


class DataStore:
    def __init__(self, file_name=DATA_FILE):
        self.file_name = file_name
        self.data = self.load()

    def init(self):
        if not self.file_name.exists():
            self.data = self._create_seed_data()
            self.save()
        else:
            self.load()

    def _create_seed_data(self):
        data = deepcopy(DEFAULT_DATA)

        # тестовые сессии (март)
        data["sessions"] = [
            {"date": "2026-03-01", "minutes": 10, "type": 1},
            {"date": "2026-03-02", "minutes": 15, "type": 2},
            {"date": "2026-03-03", "minutes": 20, "type": 3},
            {"date": "2026-03-04", "minutes": 5, "type": 1},
            {"date": "2026-03-05", "minutes": 25, "type": 3},
        ]

        data["stats"]["total_minutes"] = sum(
            s["minutes"] for s in data["sessions"]
        )

        return data

    def load(self):
        """
        Читает данные из файла и поверяет, что он есть
        """
        try:
            with open(self.file_name, "r", encoding="utf-8") as file_input:
                self.data = json.load(file_input)
            return self.data
        except FileNotFoundError:
            self.data = deepcopy(DEFAULT_DATA)
            self.save()
            return self.data

        except json.JSONDecodeError:
            raise ValueError(
                f"Ошибка: Файл {self.file_name} "
                f"поврежден или содержит некорректные данные."
            )

        except Exception as error:
            raise RuntimeError(f"Произошла ошибка при чтении файла: {error}")

    def save(self):
        """
        Сохраняет файл и выдает ошибку, если сохранение не удалось
        """
        try:
            with open(self.file_name, "w", encoding="utf-8") as file_output:
                json.dump(self.data, file_output, ensure_ascii=False, indent=2)
            return True
        except Exception as error:
            raise RuntimeError(f"Ошибка при сохранении данных: {error}")

    def get_data(self):
        return self.data

    def get_sessions(self):
        return self.data.get("sessions", [])

    def get_settings(self):
        return self.data.get("settings", {})

    def new_session(self, minutes: int, session_type: int):
        """
        Создает новую сессию и выдает ошибку,
        если введенные данные не число или отрицательное число
        """
        if self.data is None:
            self.data = self.load()
        session = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "minutes": minutes,
            "type": session_type,
        }

        self.data["sessions"].append(session)
        self.data["stats"]["total_minutes"] += minutes
        self.save()

        return session
