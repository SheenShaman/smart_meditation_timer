import pytest
import os
import json
from datetime import datetime
from data.datastore import DataStore


class TestsDataStore:
    """
    Тестирует класс DataStore
    """

    def test_init(self):
        """
        При создании без параметров используется файл по умолчанию
        """
        store = DataStore()
        assert store.file_name == 'app_data.json'

    def test_load(self, tmp_path):
        """
        Проверяем, что прочитали те же данные, что и ввели
        """
        test_file = tmp_path / 'app_data.json'
        test_data = {
            "sessions": [{"date": "2024-01-01", "minutes": 30, "notes": "тест"}],
            "settings": {"sound": False, "theme": "light", "weekly_goal": 300},
            "stats": {"total_minutes": 30}
        }
        with open(test_file, 'w', encoding='UTF-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        store = DataStore(test_file)
        res = store.load()

        assert res == test_data

    def test_load_nonexistent_file(self, tmp_path, capsys):
        """
        Проверяем, что при отсутствии файла данные возвращаются по умолчанию
        """
        nonexistent_file = tmp_path / 'no_file.json'

        store = DataStore(nonexistent_file)

        with pytest.raises(FileNotFoundError) as exc_info:
            store.load()

        assert str(nonexistent_file) in str(exc_info.value)
        assert 'не найден' in str(exc_info.value)

    def test_save(self, tmp_path):
        """
        Проверяем, что сох роняемое содержимое сов подает с тем, что хотим сохранить
        """
        test_file = tmp_path / 'save_test.json'
        test_data = {
            "sessions": [{"date": "2024-01-01", "minutes": 30}],
            "settings": {"sound": True},
            "stats": {"total_minutes": 30}
        }

        store = DataStore(test_file)
        res = store.save(test_data)

        assert res is True

        with open(test_file, 'r', encoding='UTF - 8') as f:
            save_data = json.load(f)
        assert save_data == test_data

    def test_save_error(self, mocker):
        """
        Тестируем, что выдаст ошибку при ошибке сохранения
        """
        store = DataStore("/nonexistent/folder/file.json")

        with pytest.raises(RuntimeError) as exc_info:
            store.save({'test': 'data'})

        assert "Ошибка при сохранении данных" in str(exc_info)

    def test_new_session_success_with_note(self, tmp_path, monkeypatch):
        """
        Проверяет успешно ли, добавляется сессия с заметкой
        """
        test_file = tmp_path/'test.json'
        initial_data = {
            "sessions": [],
            "settings": {"sound": True, "theme": "dark", "weekly_goal": 200},
            "stats": {"total_minutes": 0}
        }
        store = DataStore(test_file)
        store.save(initial_data)

        inputs = iter(["30", "тестовая заметка"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        res = store.new_session(initial_data.copy())

        assert len(res["sessions"]) == 1

        session = res["sessions"][0]
        assert session["minutes"] == 30
        assert session["notes"] == "тестовая заметка"
        assert "date" in session

        assert res["stats"]["total_minutes"] == 30
