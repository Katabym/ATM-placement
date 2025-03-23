import argparse
import subprocess
import sys
from functions import *

def main():
    atms = argparse.ArgumentParser(description='Расчет новых расстояний между банкоматами')
    atms.add_argument('--tests', action='store_true', help='Запускает тестовые варианты')
    atms.add_argument('--v1_3', action='store_true', help='Запускает тест для функции 1.3 версии')
    atms.add_argument('--v2_2_1', action='store_true', help='Запускает тест для функции 2.2.1 версии')
    atms.add_argument('--v2_2_0', action='store_true', help='Запускает тест для функции 2.2.0 версии')
    atms.add_argument('--n', type=int, default=3, help='Количество расстояний между банкоматами')
    atms.add_argument('--k', type=int, default=3, help='Количество новых банкоматов')
    atms.add_argument('--L', type=int, nargs='+', default=[10, 5, 8], help='Список расстояний')


    args = atms.parse_args()

    try:
        if args.n == len(args.L):
            if args.tests:
                # Запускаем tests.py
                subprocess.run([sys.executable, 'tests.py'])
            elif args.v1_3:
                # Запускаем функцию 1ю3 версии
                print(f"Parametrs: {args.n, args.k, args.L}")
                result = optimize_atm_locations_ver_1_3(args.n, args.k, args.L)
                # Вывод не отсортированный по убыванию
                print("Version 1.3 result - ", [round(x, 1) for x in result])
                # Вывод отсортированный по убыванию
                print("Version 1.3 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
            elif args.v2_2_1:
                # Запускаем функцию 2.2.1 версии
                print(f"Parametrs: {args.n, args.k, args.L}")
                result = optimize_atm_locations_2_2_1(args.n, args.k, args.L)
                # Вывод не отсортированный по убыванию
                print("Version 2.2.1 result - ", [round(x, 1) for x in result])
                # Вывод отсортированный по убыванию
                print("Version 2.2.1 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
            elif args.v2_2_0:
                # Запускаем функцию 2.2.0 версии
                print(f"Parametrs: {args.n, args.k, args.L}")
                result = optimize_atm_locations_2_2_0(args.n, args.k, args.L)
                # Вывод не отсортированный по убыванию
                print("Version 2.2.0 result - ", [round(x, 1) for x in result])
                # Вывод отсортированный по убыванию
                print("Version 2.2.0 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
            else:
                print("Аргумент отсутствует.")
        else:
            # На случай если поменяли n или L по одиночке
            print("Количество промежутков n не соответствует списку длинн этих промежутков L")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()