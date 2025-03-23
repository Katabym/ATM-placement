
from functions import optimize_atm_locations_ver_1_3 as ver1_3
from functions import optimize_atm_locations_2_2_1 as ver2_2_1
from functions import optimize_atm_locations_2_2_0 as ver2_2_0


def Test_versions(n, k, L, test_number=1):
    print(f"Test number {test_number}")
    print(f"Test parametrs: {n, k, L}")
    print('>>>>>>')
    try:
        result = ver1_3(n, k, L)
        # Вывод не отсортированный по убыванию
        print("Version 1.3 result - ", [round(x, 1) for x in result])
        # Вывод отсортированный по убыванию
        print("Version 1.3 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
        print('>>>>>>')
    except:
        print("Я споткнулся")

    try:
        result = ver2_2_1(n, k, L)
        # Вывод не отсортированный по убыванию
        print("Version 2.2.1 result - ", [round(x, 1) for x in result])
        # Вывод отсортированный по убыванию
        print("Version 2.2.1 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
        print('>>>>>>')
    except:
        print("Я споткнулся")

    try:
        result = ver2_2_0(n, k, L)
        # Вывод не отсортированный по убыванию
        print("Version 2.2.0 result - ", [round(x, 1) for x in result])
        # Вывод отсортированный по убыванию
        print("Version 2.2.0 sort result - ", sorted([round(x, 1) for x in result], reverse=True))
        print('>>>>>>')
    except:
        print("Я споткнулся")

    print("~" * 50)

# Test 1
# 4 bankomat
n = 3
# 3 new bankomat
k = 3
L = [10, 5, 8]

Test_versions(n, k, L)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test 2
# 6 bankomat
n = 5
# 8 new bankomat
k = 8
L = [10, 5, 8, 13, 2]

Test_versions(n, k, L, 2)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test 3
# 6 bankomat
n = 5
# 4 new bankomat
k = 4
L = [15, 7, 12, 9, 6]

Test_versions(n, k, L, 3)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test 4
# 3 bankomat
n = 2
# 5 new bankomat
k = 5
L = [20, 10]

Test_versions(n, k, L, 4)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Test 5
# 8 bankomat
n = 7
# 6 new bankomat
k = 6
L = [8, 12, 5, 9, 11, 7, 15]

Test_versions(n, k, L, 5)