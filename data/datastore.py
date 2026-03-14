import os
import json
from datetime import datetime


class DataStore:

    def __init__(self, file_name="app_data.json"):
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
            raise ValueError(f"Ошибка: Файл {self.file_name} поврежден или содержит некорректные данные.")

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

    def new_session(self, data):
        """
        Создает новую сессию и выдает ошибку, если введенные данные не число или отрицательное число
        """
        try:
            minutes = int(input('Введите количество минут: '))
            if minutes <= 0:
                raise ValueError("Количество минут должно быть положительным числом!")

        except ValueError:
            raise ValueError('Введите число!')

        note = input('Заметки (Enter для пропуска): ')

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


