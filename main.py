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
