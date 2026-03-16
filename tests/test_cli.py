from pathlib import Path

from report_coffee.cli import main


def test_main_success(tmp_path: Path, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,100,7,5,ok,Math\n"
        "Alice,2024-06-02,300,6,6,ok,Math\n"
        "Bob,2024-06-01,500,5,7,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(["--files", str(csv_file), "--report", "median-coffee"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "student" in captured.out
    assert "median_coffee" in captured.out
    assert "Bob" in captured.out
    assert "Alice" in captured.out
    assert captured.err == ""


def test_main_unknown_report(tmp_path: Path, capsys):
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,100,7,5,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(["--files", str(csv_file), "--report", "unknown-report"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Неизвестный отчёт" in captured.err


def test_main_missing_file(capsys):
    exit_code = main(["--files", "missing.csv", "--report", "median-coffee"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "файл не найден" in captured.err


def test_main_invalid_csv_data(tmp_path: Path, capsys):
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,not-a-number,7,5,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(["--files", str(csv_file), "--report", "median-coffee"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Невалидные данные в файле" in captured.err


def test_main_missing_required_column(tmp_path: Path, capsys):
    csv_file = tmp_path / "invalid_missing_column.csv"
    csv_file.write_text(
        "student,date,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,7,5,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(["--files", str(csv_file), "--report", "median-coffee"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Невалидные данные в файле" in captured.err
    assert "отсутствуют колонки: coffee_spent" in captured.err


def test_main_empty_student_value(tmp_path: Path, capsys):
    csv_file = tmp_path / "invalid_empty_student.csv"
    csv_file.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        ",2024-06-01,100,7,5,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(["--files", str(csv_file), "--report", "median-coffee"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Невалидные данные в файле" in captured.err
    assert "пустое поле 'student'" in captured.err


def test_main_merges_data_from_multiple_files(tmp_path: Path, capsys):
    first_csv = tmp_path / "part1.csv"
    second_csv = tmp_path / "part2.csv"

    first_csv.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-01,100,7,5,ok,Math\n"
        "Bob,2024-06-01,400,6,6,ok,Math\n",
        encoding="utf-8",
    )
    second_csv.write_text(
        "student,date,coffee_spent,sleep_hours,study_hours,mood,exam\n"
        "Alice,2024-06-02,300,7,5,ok,Math\n"
        "Bob,2024-06-02,600,6,6,ok,Math\n",
        encoding="utf-8",
    )

    exit_code = main(
        ["--files", str(first_csv), str(second_csv), "--report", "median-coffee"]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Alice" in captured.out
    assert "Bob" in captured.out
    assert "200" in captured.out
    assert "500" in captured.out
