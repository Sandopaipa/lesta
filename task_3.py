"""
ЗАДАЧА
На языке Python предложить алгоритм, который быстрее всего (по процессорным тикам)
отсортирует данный ей массив чисел. Массив может быть любого размера со случайным порядком чисел
(в том числе и отсортированным). Объяснить, почему вы считаете, что функция соответствует
заданным критериям.


Руководствуясь такой характеристикой, как временная сложность алгоритма - то в данном случае
оптимальным вариантом будет использование алгоритма timsort, так как он имеет худшую временную
сложность O(n log n) и лучшую O(n). Кроме того, timsort является встроенным алгоритм сортировки [https://docs.python.org/3/howto/sorting.html].

Так как timsort основан на сортировке вставкой и сортировке слиянием - то имеет смысл сравнить скорость
его работы и затраты памяти в сранвнеии с этими алгоритмами. Из-за того, что timsort уже используется в
Python функцией sorted(), то программная реализоация данного алгоритма здесь не приводится.

Если запустить работу программы - то можно увидеть, что минимальное время работы у алгоритма timsort,
однако затраты памяти у него самые большие. Сортировка слиянием в среднем оказывается медленнее, но по затратам
памяти это сильно меньше, чем timsort.

Наверное, если бы мне критически важно было время работы алгоритма - то я выбрал бы timsort.
Если бы мне было критически важно потребление памяти алгоритма - то я бы выбрал сортировку слиянием.
А еще у этого алгоритма тоакая же временная сложность, как и у timsort.
Хотя, стоит отметить, что если массив совсем небольшой, то можно использовать и сортировку вставкой.
По потреблению памяти будет как в случае использования сортировки слиянием, но по времени - несколько быстрее.
"""
import random
import time
import sys


def insertion_sort(_array: list) -> None:
    """
    Сортировка вставкой.
    """
    for i in range(len(_array)):
        current_item = _array[i]
        j = i - 1
        while j >= 0 and current_item < _array[j]:
            _array[j + 1] = _array[j]
            j = j - 1
        _array[j + 1] = current_item


def merge_sort(_array: list) -> None:
    """
    Сортировка слиянием.
    """
    if len(_array) > 1:
        mid = len(_array)//2
        lefthalf = _array[:mid]
        righthalf = _array[mid:]

        merge_sort(lefthalf)
        merge_sort(righthalf)

        i = j = k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                _array[k] = lefthalf[i]
                i = i + 1
            else:
                _array[k] = righthalf[j]
                j = j + 1
            k = k + 1

        while i < len(lefthalf):
            _array[k] = lefthalf[i]
            i = i + 1
            k = k + 1

        while j < len(righthalf):
            _array[k] = righthalf[j]
            j = j + 1
            k = k + 1


def sort_alg_time(sort_alg, array: list) -> dict:
    """
    Функция для вычисления времени работы алгоритма.
    Возвращает словарь следующего вида:
        {"Названием алгоритма сортировки": "Затраченное на выполненние время"}
    """
    start_time = time.perf_counter_ns()
    sort_alg(array)
    stop_time = time.perf_counter_ns()
    return {
        sort_alg.__name__: stop_time - start_time
    }


def sort_alg_mem(sort_alg, array: list) -> dict:
    """
    Функция для вычисления затрат памяти алгоритмом (Размер объекта).
    Возвращает словарь вида:
        {"Название алгоритма сортировки": "Объем алгоритма в байтах"}
    """
    return {
        sort_alg.__name__: sys.getsizeof(sort_alg(array))
    }


def dict_sort(_dict: dict) -> dict:
    """
    Функция для сортировки словаря по его значениям для наглядности.
    """
    sorted_tuple = sorted(_dict.items(), key=lambda x: x[1])
    return dict(sorted_tuple)


arr: list = []
for _ in range(10):
    arr.append(random.randint(-100000, 100000))

algs_arr: list = [
    insertion_sort,
    merge_sort,
    sorted,
]

alg_time_set: dict = {}
alg_mem_set: dict = {}



for _alg in algs_arr:
    alg_time_set.update(sort_alg_time(
        _alg, arr
    ))

alg_time_set = dict_sort(alg_time_set)
print(alg_time_set)

for _alg in algs_arr:
    alg_mem_set.update(sort_alg_mem(
        _alg, arr
    ))
alg_mem_set = dict_sort(alg_mem_set)
print(alg_mem_set)


