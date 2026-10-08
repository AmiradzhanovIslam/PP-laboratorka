# Лабораторная работа №1
# Индивидуальный вариант №6: сумма чисел от 10 до 50

# 1. Императивный стиль
numbers = list(range(10, 51))
total = 0
iterations = 0

for number in numbers:
    total += number
    iterations += 1

print("Числа:", numbers)
print("Количество итераций:", iterations)
print("Сумма чисел от 10 до 50:", total)


# 2. Процедурный стиль
from typing import Iterable

def get_numbers(start: int, end: int) -> list[int]:
    return list(range(start, end + 1))

def sum_numbers(values: Iterable[int]) -> int:
    total = 0
    for value in values:
        total += value
    return total

numbers = get_numbers(10, 50)
print("Количество чисел:", len(numbers))
print("Сумма чисел от 10 до 50:", sum_numbers(numbers))


# 3. Объектно-ориентированный стиль
class NumberRange:
    """Представляет диапазон целых чисел и операции над ним."""

    def __init__(self, start: int, end: int):
        self._start = start
        self._end = end

    def get_numbers(self) -> list[int]:
        return list(range(self._start, self._end + 1))

    def calculate_sum(self) -> int:
        return sum(self.get_numbers())

    def count(self) -> int:
        return len(self.get_numbers())

numbers = NumberRange(10, 50)
print("Количество чисел:", numbers.count())
print("Сумма чисел от 10 до 50:", numbers.calculate_sum())


# 4. Функциональный стиль
numbers = range(10, 51)

squares_example = [number ** 2 for number in numbers]
result = sum(numbers)

print("Первое число:", numbers.start)
print("Последнее число:", numbers.stop - 1)
print("Сумма чисел от 10 до 50:", result)

