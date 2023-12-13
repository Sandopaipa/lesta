"""
ЗАДАЧА
На языке Python написать минимум по 2 класса реализовывающих циклический буфер FIFO.
Объяснить плюсы и минусы каждой реализации.


В данном случае - был проведен эксперимент по работе буфера с данными разного объема для
того, чтобы качественно установить зависиость производительности буфера от его размера и количества
данных, с которым ему необходимо работать.

Результат получился следующий: буфер ListFIFO на базе списка (массива) оказался эффективнее при работе со
сравнительно небольшим количеством данных при небольшом объеме буфера. ОДнако при увеличении объема как
самих данных - так и размера буфера - преимущество по скорости работы начинает переходимть к буферу LinkedListFIFO
на базе связанного списка.

Вы можете перепроверить данное утверждение, если запустите данный скрипт.
"""


import time


class ZeroSize(Exception):
    """
    Исключение, которое вызвывается при задании нулевого размера буфера.
    """
    def __init__(self):
        self.message = 'Максимальная длина буфера не может быть равно 0'
        super().__init__(self.message)


class BelowZeroSize(Exception):
    """
    Исключение, которое вызывается при задании отрицательного размера буфера
    """
    def __init__(self):
        self.message = 'Размер буфера не может быть отрицательным'
        super().__init__(self.message)


class InvalidBufSizeVal(Exception):
    """
    Исключение, которое вызывается, если размер буфера не int.
    """
    def __init__(self):
        self.message = 'Недействительный размер буфера'
        super().__init__(self.message)


class EmptyBuf(Exception):
    """
    Исключение, которое вызывается при попытке достать значение из пустого буфера.
    """
    def __init__(self):
        self.message = 'Вы пытаетесь взять значение из пустого буфера'


class ListFIFO:
    """
    Циклический буфер на базе списка (массива).

    Плюсы:  1. Читаемость кода
            2. Алгоритм быстрее работает с небольшим размером буфера.
    Минусы: 1. При увеличении размера буфера - скорость работы снижается.
    """
    def __init__(self, buf_size: int):
        self.buf_size: int = self._size_check(buf_size)
        self.buffer: list = []

    def add_item(self, item) -> None:
        """
        Добавляет item в конец массива. При заполнении массива удаляет первый его элемент.
        """
        if len(self.buffer) == self.buf_size:
            self.buffer.pop(0)
        self.buffer.append(item)

    def get_item(self):
        """
        Забирает элемент из начала массива и удаляет его из буфера.
        """
        if len(self.buffer) == 0:
            raise EmptyBuf
        return self.buffer.pop(0)

    def _size_check(self, buf_size: int) -> int | Exception:
        """
        Валидация размера буфера.
        """
        if isinstance(buf_size, int):   # Проверка целочисленности размера буфера.
            if buf_size == 0:           # Валидация размера буфера.
                raise ZeroSize
            elif buf_size < 0:          # Валидация размера буфера.
                raise BelowZeroSize
            else:
                return buf_size
        else:
            raise InvalidBufSizeVal

    def __len__(self):
        return len(self.buffer)

    def __iter__(self):
        for _item in self.buffer:
            yield _item


class LinkedListFIFO:
    """
    Класс, имлпементирующий связанный список.
    Плюсы:  1. Быстрее работает при большом размере буфера.
    Минусы: 1. Немного сложнее в реализации.
            2. Ниже скорость при работе с небольшим размером буфера.
    """
    class Node:
        """
        Класс, имплементирующий узел списка.
        """
        def __init__(self, data: any):
            self.next = None
            self.data = data

    def __init__(self, buf_size: int):
        self.buf_size = self._size_check(buf_size)
        self.head = None
        self.tail = None
        self.length = 0

    def add_item(self, data: any) -> None:
        """
        Добавление элемента в список.
        data: может быть любым типом.
        """
        item = self.Node(data)
        #  Если список пустой
        if self._is_empty() is True:
            self._add_first_item(item)
            return
        else:
            #  Если список полный - убираем головной элемент.
            if self._is_full() is True:
                self._pop()
                #  Проверяем, если список пустой: полезно, когда буфер из одного элемента.
                if self._is_empty() is not True:
                    self._add(item)
                else:
                    self._add_first_item(item)
            else:
                self._add(item)
                return

    def _is_empty(self) -> bool:
        """
        Проверка, пустой ли буфер.
        """
        if self.length == 0:
            return True
        else:
            return False

    def _is_full(self) -> bool:
        """
        Проверка, заполнен ли буфер полность.
        """
        if self.length == self.buf_size:
            return True
        else:
            return False

    def _pop(self) -> None:
        """
        Удаление элемента. Удаляется головной элемент буфера.
        """
        if self.head == self.tail:
            self.head = None
            self.tail = None
            self.length -= 1
            return
        else:
            self.head = self.head.next
            self.length -= 1
            return

    def _add(self, item: Node) -> None:
        """
        Добавление элемента в буфер.
        """
        self.tail.next = item
        self.tail = self.tail.next
        self.length += 1
        return

    def _add_first_item(self, item: Node) -> None:
        """
        Добавление первогоо элемента в буфер.
        """
        self.head = item
        self.tail = self.head
        self.length = 1
        return

    def _size_check(self, buf_size: int) -> int | Exception:
        """
        Валидация размера буфера.
        """
        if isinstance(buf_size, int):   # Проверка целочисленности размера буфера.
            if buf_size == 0:           # Валидация размера буфера.
                raise ZeroSize
            elif buf_size < 0:          # Валидация размера буфера.
                raise BelowZeroSize
            else:
                return buf_size
        else:
            raise InvalidBufSizeVal

    def __iter__(self):
        current_node = self.head
        while current_node is not None:
            data = current_node.data
            current_node = current_node.next
            yield data


def build_array(array_size: int) -> list:
    arr: list = []
    for _item in range(array_size):
        arr.append(_item)
    return arr


def perf_test(buf_size: int, array_size: int) -> None:
    """
    Функция для тестирования времени обработки массива двумя циклическими буферами.
    """
    arr = build_array(array_size)

    buf1 = ListFIFO(buf_size)
    buf2 = LinkedListFIFO(buf_size)

    start_time = time.perf_counter_ns()
    for _item in arr:
        buf2.add_item(_item)
    end_time = time.perf_counter_ns()

    buf2_exec_time = end_time - start_time

    start_time = time.perf_counter_ns()
    for _item in arr:
        buf1.add_item(_item)
    end_time = time.perf_counter_ns()

    buf1_exec_time = end_time - start_time

    print(
        f'buf_size {buf_size}     array_size {array_size}'
    )

    if buf2_exec_time > buf1_exec_time:
        print(
            f'Буфер на базе ListFIFO быстрее LinkedListFIFO на {buf2_exec_time - buf1_exec_time}'
        )
    elif buf1_exec_time == buf2_exec_time:
        print(
            'Оба справились за одинаковое время'
        )
    else:
        print(
            f'Буфер на базе LinkedListFIFO быстрее ListFIFO на {buf1_exec_time - buf2_exec_time}'
        )


arr_test_1 = 100
buf_size1 = 1
buf_size2 = 50
buf_size3 = 90
buf_size4 = 100
for i in [buf_size1, buf_size2, buf_size3, buf_size4]:
    perf_test(buf_size=i, array_size=arr_test_1)

arr_test_1 = 10000000
buf_size1 = 1
buf_size2 = 500
buf_size3 = 9000
buf_size4 = 100000
for i in [buf_size1, buf_size2, buf_size3, buf_size4]:
    perf_test(buf_size=i, array_size=arr_test_1)
