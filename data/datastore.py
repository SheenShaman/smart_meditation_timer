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

    def load(self):
        """
        Читает данные из файла и поверяет, что он есть
        """
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file_input:
                data = json.load(file_input)
                return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.file_name} не найден. Будет создан новый файл при сохранении.")

        except json.JSONDecodeError:
            raise ValueError(
                f"Ошибка: Файл {self.file_name} "
                f"поврежден или содержит некорректные данные."
            )

        except Exception as error:
            raise RuntimeError(f"Произошла ошибка при чтении файла: {error}")

    def save(self, data):
        """
        Сохраняет файл и выдает ошибку, если сохранение не удалось
        """
        try:
            with open(self.file_name, 'w', encoding='utf-8') as file_output:
                json.dump(data, file_output, ensure_ascii=False, indent=2)
            print(f"Данные успешно сохранены в файл {self.file_name}")
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
            "minutes": minutes
        }
        if note.strip():
            session["notes"] = note.strip()

        data["sessions"].append(session)

        data["stats"]["total_minutes"] += minutes

        self.save(data)

        print(f"Сессия добавлена! (+{minutes} минут)")
        print(f"Всего минут: {data['stats']['total_minutes']}")

        return data


