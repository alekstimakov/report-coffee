from pathlib import Path

from report_coffee.cli import main


def test_main_success(tmp_path: Path, capsys):
    # Создаём временный CSV для позитивного сценария.
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,100,7,5,ok,Math\n"
        "Alice,2024-06-02,300,6,6,ok,Math\n"
        "Bob,2024-06-01,500,5,7,ok,Math\n",
        encoding="utf-8",
    )

    # Вызываем CLI-функцию напрямую с аргументами.
    exit_code = main(["--files", str(csv_file), "--report", "median-coffee"])
    captured = capsys.readouterr()

    # Проверяем успешный код завершения и базовый вывод таблицы.
    assert exit_code == 0
    assert "student" in captured.out
    assert "median_coffee" in captured.out
    assert "Bob" in captured.out
    assert "Alice" in captured.out
    assert captured.err == ""


def test_main_unknown_report(tmp_path: Path, capsys):
    # CSV есть, но запрашиваем несуществующий отчёт.
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,100,7,5,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(["--files", str(csv_file), "--report", "unknown-report"])
    captured = capsys.readouterr()

    # Ожидаем ошибку и сообщение об неизвестном отчёте.
    assert exit_code == 1
    assert "Неизвестный отчёт" in captured.err


def test_main_missing_file(capsys):
    # Путь к файлу не существует.
    exit_code = main(["--files", "missing.csv", "--report", "median-coffee"])
    captured = capsys.readouterr()

    # Ожидаем ошибку и понятное сообщение.
    assert exit_code == 1
    assert "файл не найден" in captured.err


def test_main_invalid_csv_data(tmp_path: Path, capsys):
    # В колонке coffee_spent передано нечисловое значение.
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,not-a-number,7,5,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(["--files", str(csv_file), "--report", "median-coffee"])
    captured = capsys.readouterr()

    # Ожидаем понятную ошибку о невалидных данных.
    assert exit_code == 1
    assert "Невалидные данные в файле" in captured.err


def test_main_missing_required_column(tmp_path: Path, capsys):
    # В CSV отсутствует обязательная колонка coffee_spent.
    csv_file = tmp_path / "invalid_missing_column.csv"
    csv_file.write_text(
        "student,date,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,7,5,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(["--files", str(csv_file), "--report", "median-coffee"])
    captured = capsys.readouterr()

    # Ожидаем понятную ошибку о невалидной структуре файла.
    assert exit_code == 1
    assert "Невалидные данные в файле" in captured.err
    assert "отсутствуют колонки: coffee_spent" in captured.err


def test_main_empty_student_value(tmp_path: Path, capsys):
    # В обязательном поле student пустое значение.
    csv_file = tmp_path / "invalid_empty_student.csv"
    csv_file.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        ",2024-06-01,100,7,5,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(["--files", str(csv_file), "--report", "median-coffee"])
    captured = capsys.readouterr()

    # Ожидаем ошибку валидации с указанием проблемного поля.
    assert exit_code == 1
    assert "Невалидные данные в файле" in captured.err
    assert "пустое поле 'student'" in captured.err
