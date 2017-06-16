class Vector:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
 
    def __mul__(self, other):
        if not isinstance(other, int):
            raise ValueError("Second multiplication object must be an int")
        return Vector(self.X * other, self.Y * other)
 
    def __rmul__(self, other):
        return self * other 

    def __add__(self, other):
        return Vector(self.X + other.X, self.Y + other.Y)

    def __str__(self):
        return "Position ({0},{1})".format(self.X, self.Y)

    def __iter__(self):
        yield self.X
        yield self.Y

    @property
    def X(self):
        return self.__x

    @property
    def Y(self):
        return self.__y


class Stack:
    def __init__(self):
        self.items = []

    def empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    @property
    def size(self):
        return len(self.items)
