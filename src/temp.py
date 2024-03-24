class CircularIterator:
    def __init__(self, lst):
        self.lst = lst
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        result = self.lst[self.index]
        self.index = (self.index + 1) % len(self.lst)
        return result

class MyClass:
    def __init__(self):
        self.gps_iter = CircularIterator([1,2,3,4,5])

    def main(self):
        for i in range(30):
            print(next(self.gps_iter))


a = MyClass()
a.main()