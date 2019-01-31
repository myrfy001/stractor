# coding:utf-8


class IncCounter:

    def __init__(self, str_format: str = '{:020d}'):
        self.counter = 0
        self.str_format = str_format.format

    def get_next_int(self):
        self.counter += 1
        return self.counter

    def get_next_str(self):
        self.counter += 1
        return self.str_format(self.counter)
