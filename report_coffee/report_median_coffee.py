from report_coffee.reports.median_coffee import build_median_coffee_report


# Реестр доступных отчётов: имя из --report -> функция построения отчёта.
REPORTS = {
    "median-coffee": build_median_coffee_report,
}


def get_report(report_name: str):
    # Возвращаем функцию отчёта по имени.
    report_builder = REPORTS.get(report_name)

    # Если отчёт неизвестен, явно сообщаем об ошибке.
    if report_builder is None:
        available_reports = ", ".join(sorted(REPORTS))
        raise ValueError(
            f"Неизвестный отчёт: '{report_name}'. "
            f"Доступные отчёты: {available_reports}"
        )

    return report_builder
