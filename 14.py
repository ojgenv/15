
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--log', default = 'logs', help = 'название файла для сохранения лога')
args = parser.parse_args()

logging.basicConfig(filename = args.log + '.log', filemode = 'w', encoding = 'utf-8', level = logging.INFO, format = '%(levelname)s %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def log_func(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Ошибка {e} в функции {func.__name__} с аргументами {args}, {kwargs}')
            return None

    return wrapper

class Rectangle:
    @log_func
    def __init__(self, width, height=None):
        logger.info('создаём объект класса Rectangle %s, %s', width, height)
        self.width = width
        if height:
            self.height = height
        else:
            self.height = width
        
        if self.width < 0 or self.height < 0:
            #logger.error('неверные параметры сторон прямоугольника')
            raise ValueError('NegativeValueError')

    def perimeter(self):
        return 2 * (self.width + self.height)

    def area(self):
        return self.width * self.height

    def __add__(self, other: "Rectangle"):
        width = self.width + other.width
        perimeter = self.perimeter() + other.perimeter()
        height = perimeter // 2 - width
        return Rectangle(width, height)

    def __sub__(self, other: "Rectangle"):
        if self.perimeter() < other.perimeter():
            self, other = other, self
        width = abs(self.width - other.width)
        perimeter = self.perimeter() - other.perimeter()
        height = perimeter // 2 - width
        return Rectangle(width, height)

    def __lt__(self, other: "Rectangle") -> bool:
        return self.area() < other.area()

    def __eq__(self, other) -> bool:
        return self.area() == other.area()

    def __le__(self, other) -> bool:
        return self.area() <= other.area()

    def __str__(self) -> bool:
        return f"Прямоугольник со сторонами {self.width} и {self.height}"
        
    def __repr__(self) -> str:
        return f"Rect({self.width}, {self.height})"

def test_width(width, height):
    '''
    >>> test_width(5,4)
    5
    >>> test_width(-2,3)
    Traceback (most recent call last):
    ...
    ValueError: NegativeValueError
    '''
    r = Rectangle(width, height)
    print(r.width)
    
def test_height(width, height):
    '''
    >>> test_height(3,4)
    3
    4
    '''
    r = Rectangle(width, height)
    print(r.width)
    print(r.height)
    
def test_perimeter(width, height=None):
    '''
    >>> test_perimeter(5)
    20
    >>> test_perimeter(3,4)
    14
    '''
    r = Rectangle(width, height)
    print(r.perimeter())

def test_area(width, height=None):
    '''
    >>> test_area(5)
    25
    >>> test_area(3,4)
    12
    '''
    r = Rectangle(width, height)
    print(r.area())

def test_addition(r1: "Rectangle", r2: "Rectangle"):
    '''
    >>> test_addition(Rectangle(5), Rectangle(3,4))
    8
    6.0
    '''
    r3 = r1 + r2
    print(r3.width)
    print(r3.height)

def test_subtraction(r1: "Rectangle", r2: "Rectangle"):
    '''
    >>> test_subtraction(Rectangle(5), Rectangle(3,4))
    2
    2.0
    '''
    r3 = r1 - r2
    print(r3.width)
    print(r3.height)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()