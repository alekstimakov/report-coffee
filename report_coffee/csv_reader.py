import csv

REQUIRED_COLUMNS = {"student", "coffee_spent"}


def read_information_from_csv(files: list[str]) -> list[dict[str, str]]:
    # Общий список строк из всех переданных CSV-файлов.
    rows: list[dict[str, str]] = []

    # Читаем файлы по очереди и объединяем данные в один список.
    for file_path in files:
        with open(file_path, mode="r", encoding="utf-8", newline="") as csv_file:
            # Каждая строка CSV будет словарём по заголовкам колонок.
            reader = csv.DictReader(csv_file)
            missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing_columns:
                columns = ", ".join(sorted(missing_columns))
                raise ValueError(
                    f"Невалидные данные в файле '{file_path}': "
                    f"отсутствуют колонки: {columns}"
                )

            for row_number, row in enumerate(reader, start=2):
                student = row.get("student")
                coffee_spent_raw = row.get("coffee_spent")

                if not student:
                    raise ValueError(
                        f"Невалидные данные в файле '{file_path}', "
                        f"строка {row_number}: пустое поле 'student'"
                    )

                try:
                    int(str(coffee_spent_raw))
                except (TypeError, ValueError) as error:
                    raise ValueError(
                        f"Невалидные данные в файле '{file_path}', "
                        f"строка {row_number}: "
                        f"'coffee_spent' должно быть целым числом"
                    ) from error

                rows.append(row)

    return rows
