import argparse


def parse_args(argv=None):
    # Настройка CLI-параметров скрипта.
    parser = argparse.ArgumentParser(
        description="Формирует отчёты по CSV-файлам со статистикой студентов."
    )
    # Список входных CSV-файлов (один или несколько).
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к одному или нескольким CSV-файлам.",
    )
    # Название отчёта, который нужно построить.
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчёта, например: median-coffee.",
    )
    # Если argv=None, argparse возьмёт аргументы из командной строки.
    return parser.parse_args(argv)
