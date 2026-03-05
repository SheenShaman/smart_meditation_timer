import os
import json
from datetime import datetime


class DataStore:
    def __init__(self, file_name="app_data.json"):
        self.file_name = file_name

    def load(self):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file_input:
                data = json.load(file_input)
                return data
        except FileNotFoundError:
            print(f"Файл {self.file_name} не найден. Будет создан новый файл при сохранении.")
            return {
                "sessions": [],
                "settings": {
                    "sound": True,
                    "theme": "dark",
                    "weekly_goal": 200
                },
                "stats": {
                    "total_minutes": 0
                }
            }
        except json.JSONDecodeError:
            print(f"Ошибка: Файл {self.file_name} поврежден или содержит некорректные данные.")
            return {
                "sessions": [],
                "settings": {
                    "sound": True,
                    "theme": "dark",
                    "weekly_goal": 200
                },
                "stats": {
                    "total_minutes": 0
                }
            }
        except Exception as error:
            print(f"Произошла ошибка при чтении файла: {error}")
            return {
                "sessions": [],
                "settings": {
                    "sound": True,
                    "theme": "dark",
                    "weekly_goal": 200
                },
                "stats": {
                    "total_minutes": 0
                }
            }

    def save(self, data):
        try:
            with open(self.file_name, 'w', encoding='utf-8') as file_output:
                json.dump(data, file_output, ensure_ascii=False, indent=2)
            print(f"Данные успешно сохранены в файл {self.file_name}")
            return True

        except Exception as error:
            print(f"Ошибка при сохранении данных: {error}")
            return False

    def new_session(self, data):
        try:
            minutes = int(input('Введите количество минут: '))
            if minutes <= 0:
                print("Количество минут должно быть положительным числом!")
                return data
        except ValueError:
            print('Введите число!')
            return data

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


store = DataStore("test.json")
data = store.load()
data = store.new_session(data)

print(f"Всего сессий: {len(data['sessions'])}")
print(f"Всего минут: {data['stats']['total_minutes']}")

with open("test.json", 'r', encoding='utf-8') as f:
    print(json.dumps(json.load(f), indent=2, ensure_ascii=False))
