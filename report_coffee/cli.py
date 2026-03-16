import argparse
import sys

from tabulate import tabulate

from report_coffee.csv_reader import read_information_from_csv
from report_coffee.report_registry import get_report


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Формирует отчеты по CSV-файлам со статистикой студентов."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к одному или нескольким CSV-файлам.",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчета, например: median-coffee.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    # Разбираем аргументы командной строки.
    args = parse_args(argv)

    try:
        # Читаем и объединяем строки из всех переданных CSV-файлов.
        rows = read_information_from_csv(args.files)
        # Находим функцию построения отчёта по имени из --report.
        report_builder = get_report(args.report)
        # Строим структуру таблицы: заголовки и строки.
        headers, table_rows = report_builder(rows)
    except FileNotFoundError as error:
        # Пользователь указал путь к несуществующему файлу.
        print(f"Ошибка: файл не найден: {error.filename}", file=sys.stderr)
        return 1
    except ValueError as error:
        # Пользователь указал неизвестное имя отчёта.
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1

    # Печатаем таблицу в консоль.
    print(tabulate(table_rows, headers=headers, tablefmt="grid"))
    return 0
