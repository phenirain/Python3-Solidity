import math


def factorial(number):
    if number == 0:
        return 1
    else:
        return number * factorial(number - 1)


def toDouble(countNumbers):
    numbers = list()
    b = 0
    while b != countNumbers:
        try:
            numbers.append(float(input(f"Введите {b + 1} число: ")))
            b += 1
        except Exception:
            print("Вы должны ввести именно число")
    return numbers


work = True
while (work):
    print('1: Сложение')
    print('2: Вычитание')
    print('3: Умножение')
    print('4: Деление')
    print('5: Вовзедение в степень')
    print('6: Квадратный корень')
    print('7: Факториал')
    print('8: Синус')
    print('9: Косинус')
    print('10: Тангенс')
    print('11: Выход')
    operation = input("Введите операцию: ")
    match (operation):
        case "1":
            numbers = toDouble(2)
            print(f"{numbers[0]} + {numbers[1]} = {numbers[0] + numbers[1]}")
        case "2":
            numbers = toDouble(2)
            print(f"{numbers[0]} - {numbers[1]} = {numbers[0] - numbers[1]}")
        case "3":
            numbers = toDouble(2)
            print(f"{numbers[0]} * {numbers[1]} = {numbers[0] * numbers[1]}")
        case "4":
            numbers = toDouble(2)
            if numbers[1] != 0:
                print(f"{numbers[0]} / {numbers[1]} = {numbers[0] / numbers[1]}")
            else:
                print("Делить на ноль нельзя")
        case "5":
            numbers = toDouble(2)
            print(f"{numbers[0]} в степени {numbers[1]} = {math.pow(numbers[0], numbers[1])}")
        case "6":
            numbers = toDouble(1)
            try:
                print(f"Корень из {numbers[0]} = {math.sqrt(numbers[0])}")
            except ValueError:
                print('нельзя найти корень из отрицательного числа')
        case "7":
            numbers = toDouble(1)
            if numbers[0] >= 0:
                print(factorial(int(numbers[0])))
            else: print("Нельзя вычислить факториал из отрицательного числа")
        case "8":
            numbers = toDouble(1)
            print(f"Синус {numbers[0]} = {math.sin(math.radians(numbers[0]))}")
        case "9":
            numbers = toDouble(1)
            print(f"Косинус {numbers[0]} = {math.cos(math.radians(numbers[0]))}")
        case "10":
            numbers = toDouble(1)
            print(f"Тангенс {numbers[0]} = {math.tan(math.radians(numbers[0]))}")
        case "11":
            work = False
            print("Конец вычислений")
        case _:
            print("Введите одну из команд")
    print()
# import math
#
# <<<<<<< HEAD
# def get_float_input(prompt):
#     while True:
#         try:
#             return float(input(prompt))
#         except ValueError:
#             print("Число введено неверно")
#
# def calculator():
#     while True:
#         try:
#             print("Выберите действие программы:\n"
#                   "1.Сложить\n"
#                   "2.Вычесть\n"
#                   "3.Умножить\n"
#                   "4.Разделить\n"
#                   "5.Возвести в степень\n"
#                   "6.Вычислить квадратный корень"
#                   "7.Факториал\n"
#                   "8.Синус\n"
#                   "9.Косинус\n"
#                   "10.Тангенс\n"
#                   "11.Выход\n")
#             command = float(input("Введите номер операции:"))
#             match command:
#                 case 1:
#                     number1 = get_float_input('Введите первое число:\n')
#                     number2 = get_float_input('Введите второе число:\n')
#                     print(f"Ответ: {number1 + number2}\n")
#                 case 2:
#                     number1 = get_float_input('Введите первое число:\n')
#                     number2 = get_float_input('Введите второе число:\n')
#                     print(f"Ответ: {number1 - number2}\n")
#                 case 3:
#                     number1 = get_float_input('Введите первое число:\n')
#                     number2 = get_float_input('Введите второе число:\n')
#                     print(f"Ответ: {number1 * number2}\n")
#                 case 4:
#                     number1 = get_float_input('Введите первое число:\n')
#                     number2 = get_float_input('Введите второе число:\n')
#                     if number2 != 0:
#                         print(f"Ответ: {number1 / number2}\n")
#                     else:
#                         print(f"На нуль делить нельзя\n")
#                 case 5:
#                     number1 = get_float_input('Введите первое число:\n')
#                     number2 = get_float_input('Введите второе число:\n')
#                     print(f"Ответ: {math.pow(number1, number2)}\n")
#                 case 6:
#                     number1 = get_float_input('Введите число:\n')
#                     print(f"Ответ: {math.sqrt(number1)}\n")
#                 case 7:
#                     number1 = get_float_input('Введите число:\n')
#                     if number1 < 0:
#                         print("Необходимо ввести целое положительное число")
#                     else:
#                         print(f"Ответ: {math.factorial(int(number1))}\n")
#                 case 8:
#                     number1 = get_float_input('Введите число:\n')
#                     print(f"Ответ: {math.sin(math.radians(number1))}\n")
#                 case 9:
#                     number1 = get_float_input('Введите число:\n')
#                     print(f"Ответ: {math.cos(math.radians(number1))}\n")
#                 case 10:
#                     number1 = get_float_input('Введите число:\n')
#                     print(f"Ответ: {math.tan(math.radians(number1))}\n")
#                 case 11:
#                     exit()
#         except ValueError:
#             print(f"\nНеизвестная команда")
#
# calculator()
#
#
#
#
# =======
#
# def factorial(number):
#     if number == 0:
#         return 1
#     else:
#         return number * factorial(number - 1)
#
#
# def toDouble(countNumbers):
#     numbers = list()
#     b = 0
#     while b != countNumbers:
#         try:
#             numbers.append(float(input(f"Введите {b + 1} число: ")))
#             b += 1
#         except Exception:
#             print("Вы должны ввести именно число")
#     return numbers
#
#
# work = True
# while (work):
#     print('1: Сложение')
#     print('2: Вычитание')
#     print('3: Умножение')
#     print('4: Деление')
#     print('5: Вовзедение в степень')
#     print('6: Квадратный корень')
#     print('7: Факториал')
#     print('8: Синус')
#     print('9: Косинус')
#     print('10: Тангенс')
#     print('11: Выход')
#     operation = input("Введите операцию: ")
#     match (operation):
#         case "1":
#             numbers = toDouble(2)
#             print(f"{numbers[0]} + {numbers[1]} = {numbers[0] + numbers[1]}")
#         case "2":
#             numbers = toDouble(2)
#             print(f"{numbers[0]} - {numbers[1]} = {numbers[0] - numbers[1]}")
#         case "3":
#             numbers = toDouble(2)
#             print(f"{numbers[0]} * {numbers[1]} = {numbers[0] * numbers[1]}")
#         case "4":
#             numbers = toDouble(2)
#             if numbers[1] != 0:
#                 print(f"{numbers[0]} / {numbers[1]} = {numbers[0] / numbers[1]}")
#             else:
#                 print("Делить на ноль нельзя")
#         case "5":
#             numbers = toDouble(2)
#             print(f"{numbers[0]} в степени {numbers[1]} = {math.pow(numbers[0], numbers[1])}")
#         case "6":
#             numbers = toDouble(1)
#             try:
#                 print(f"Корень из {numbers[0]} = {math.sqrt(numbers[0])}")
#             except ValueError:
#                 print('нельзя найти корень из отрицательного числа')
#         case "7":
#             numbers = toDouble(1)
#             if numbers[0] >= 0:
#                 print(factorial(int(numbers[0])))
#             else: print("Нельзя вычислить факториал из отрицательного числа")
#         case "8":
#             numbers = toDouble(1)
#             print(f"Синус {numbers[0]} = {math.sin(math.radians(numbers[0]))}")
#         case "9":
#             numbers = toDouble(1)
#             print(f"Косинус {numbers[0]} = {math.cos(math.radians(numbers[0]))}")
#         case "10":
#             numbers = toDouble(1)
#             print(f"Тангенс {numbers[0]} = {math.tan(math.radians(numbers[0]))}")
#         case "11":
#             work = False
#             print("Конец вычислений")
#         case _:
#             print("Введите одну из команд")
#     print()
# >>>>>>> 54782e6c62a72568573a2c9062e86d5816dcc997
