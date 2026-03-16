import csv


def read_information_from_csv(files: list[str]) -> list[dict]:
    # Общий список строк из всех переданных CSV-файлов.
    rows: list[dict] = []

    # Читаем файлы по очереди и объединяем данные в один список.
    for file_path in files:
        with open(file_path, mode="r", encoding="utf-8", newline="") as csv_file:
            # Каждая строка CSV будет словарём по заголовкам колонок.
            reader = csv.DictReader(csv_file)
            rows.extend(reader)

    return rows
