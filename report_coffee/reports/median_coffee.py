import statistics
from typing import Any


def calculate_median(rows: list[dict[str, str]]) -> tuple[list[str], list[list[Any]]]:
    # Словарь вида: студент -> список его трат на кофе.
    student_coffee_spent: dict[str, list[int]] = {}

    # Проходим по всем строкам и собираем траты по каждому студенту.
    for row in rows:
        student = row["student"]
        coffee_spent = int(row["coffee_spent"])

        # Если студент встречается впервые, создаём для него пустой список.
        if student not in student_coffee_spent:
            student_coffee_spent[student] = []

        # Добавляем текущую трату в список студента.
        student_coffee_spent[student].append(coffee_spent)

    # Формируем строки итоговой таблицы.
    table_rows: list[list[Any]] = []
    for student, spends in student_coffee_spent.items():
        median_value = statistics.median(spends)
        table_rows.append([student, median_value])

    # Сортируем по убыванию медианы трат.
    table_rows.sort(key=lambda item: item[1], reverse=True)

    headers = ["student", "median_coffee"]
    return headers, table_rows


def build_median_coffee_report(
    rows: list[dict[str, str]],
) -> tuple[list[str], list[list[Any]]]:
    # Совместимое имя функции для вызова через реестр отчётов.
    return calculate_median(rows)
