from report_coffee.reports.median_coffee import calculate_median


def test_calculate_median_and_sort_desc():
    # Подготовка входных данных (строки в формате DictReader).
    rows = [
        {"student": "Alice", "coffee_spent": "100"},
        {"student": "Alice", "coffee_spent": "300"},
        {"student": "Bob", "coffee_spent": "500"},
        {"student": "Bob", "coffee_spent": "700"},
        {"student": "Charlie", "coffee_spent": "200"},
    ]

    # Запускаем расчёт отчёта.
    headers, table_rows = calculate_median(rows)

    # Проверяем заголовок и сортировку по убыванию медианы.
    assert headers == ["student", "median_coffee"]
    assert table_rows == [
        ["Bob", 600.0],
        ["Alice", 200.0],
        ["Charlie", 200],
    ]
