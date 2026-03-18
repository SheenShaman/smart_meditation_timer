import pytest
import os
import json
from datetime import datetime
from data.datastore import DataStore, DATA_FILE
from pathlib import Path


class TestsDataStore:
    """
    Тестирует класс DataStore
    """

    def test_init(self):
        """
        При создании без параметров используется файл по умолчанию
        """
        store = DataStore()
        assert store.file_name == DATA_FILE

    def test_load(self, tmp_path):
        """
        Проверяем, что прочитали те же данные, что и ввели
        """
        test_file = tmp_path / "app_data.json"
        test_data = {
            "sessions": [
                {"date": "2024-01-01", "minutes": 30, "notes": "тест"}
            ],
            "settings": {"sound": False, "theme": "light", "weekly_goal": 300},
            "stats": {"total_minutes": 30},
        }
        with open(test_file, "w", encoding="UTF-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)

        store = DataStore(test_file)
        res = store.load()

        assert res == test_data

    def test_load_nonexistent_file(self, tmp_path, capsys):
        """
        Проверяем, что при отсутствии файла данные возвращаются по умолчанию
        """
        nonexistent_file = tmp_path / "no_file.json"

        store = DataStore(nonexistent_file)

        data = store.load()

        assert data["sessions"] == []
        assert data["stats"]["total_minutes"] == 0
        assert "settings" in data

    def test_save(self, tmp_path):
        """
        Проверяем, что сох роняемое содержимое сов подает с тем, что хотим сохранить
        """
        test_file = tmp_path / "save_test.json"
        store = DataStore(test_file)
        store.data = {
            "sessions": [{"date": "2024-01-01", "minutes": 30}],
            "settings": {"sound": True},
            "stats": {"total_minutes": 30},
        }
        store.save()
        assert test_file.exists()
        with open(test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data == store.data

    def test_save_error(self, mocker):
        """
        Тестируем, что выдаст ошибку при ошибке сохранения
        """
        store = DataStore("test.json")
        store.data = {}

        mocker.patch("builtins.open", side_effect=Exception("fail"))

        with pytest.raises(RuntimeError):
            store.save()

    def test_new_session_success(self, tmp_path, monkeypatch):
        """
        Проверяет успешно ли, добавляется сессия с заметкой
        """
        test_file = tmp_path / "test.json"
        store = DataStore(test_file)

        session = store.new_session(minutes=1, session_type=1)

        assert session["minutes"] == 1
        assert session["type"] == 1
        assert "date" in session

        data = store.load()

        assert len(data["sessions"]) == 1
        assert data["stats"]["total_minutes"] == 1
