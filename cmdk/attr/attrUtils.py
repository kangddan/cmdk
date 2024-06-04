from functools import wraps

# check type ----------------------------------------------
def checkNumberType(func):
    def wrapper(*args, **kwargs):
        if not isinstance(args[1], (int, float, complex)): # (self, value) -> args[1]
            raise TypeError('The {} attribute must be a number'.format(func.__name__))
        return func(*args, **kwargs)
    return wrapper
    
def checkVectorType(func):
    def wrapper(*args, **kwargs):
        if not all(isinstance(n, (int, float, complex)) for n in args[1]):
            raise TypeError('Please ensure all parameters are numeric :{}'.format(args[1]))
        return func(*args, **kwargs)
    return wrapper
    

def checkClass(func):
    @wraps(func)
    def wrapper(self, other, *args, **kwargs):
        if not isinstance(other, self.__class__):
            raise TypeError('Expected object of type {}, got {}'.format(self.__class__.__name__, type(other).__name__))
        return func(self, other, *args, **kwargs)
    return wrapper
    

