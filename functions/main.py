import math


def rectangle_area(width, height):
    return width * height


def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False


def sum_digits(number):
    sum = 0
    while number > 0:
        sum += number % 10
        number //= 10
    return sum







def sumNumbers(numbers):
    count = 0
    for num in numbers:
        count += num
    return count


def findMax(numbers):
    max = 0
    for num in numbers:
        if max < num:
            max = num
    return max


def deleteDupl(numbers):
    newList = list()
    for num in numbers:
        if num not in newList:
            newList.append(num)
    return newList


def uniteLists(list1, list2):
    newList = list()
    for value in list1:
        newList.append(value)
    for value in list2:
        newList.append(value)
    return newList


def findEl(tupl, f):
    newList = list(tupl)
    result = "Не найдено"
    for id, value in enumerate(newList):
        if f == value:
            result = id
    return result


if __name__ == "__main__":
    findMax([1,2,3,4,5])