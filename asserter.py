import operator

make_special_func = "__{}__".format
predicates = map(make_special_func, ('eq', 'ne', 'lt', 'gt', 'le', 'ge', 'contains'))

def create_forwarding_pred(pred_name):
    def pred(self, other):
        pred = getattr(operator, pred_name)
        result = pred(self.obj, other)
        if not result:
            raise AssertionError("{} {} {} -> False".format(self.obj, pred_name.strip('_'), other))
        return result
    pred.__name__ = pred_name
    return pred

def meta(name, bases, dict_):
    for pred_name in predicates:
        dict_[pred_name] = create_forwarding_pred(pred_name)
    return type(name, bases, dict_)

class Asserter(object):

    __metaclass__ = meta
    
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return "wrapped({})".format(repr(self.obj))
    
    def __call__(self):
        return type(self)(self.obj())

    def __getitem__(self, item):
        return type(self)(self.obj[item])

    def __getattr__(self, attr):
        return type(self)(getattr(self.obj, attr))

    def __len__(self):
        raise NotImplementedError("Python's builtin len() lacks support for a return value different from int, use .length() instead")

    def length(self):
        return type(self)(len(self.obj))
    
    def is_(self, other):
        result = self.obj is other
        if not result:
            raise AssertionError("{} is {} -> False".format(self.obj, other))
        return result

    def __instancecheck__(self, cls):
        return isinstance(self.obj, cls)

    def __subclasscheck__(self, cls):
        return issubclass(type(self.obj), cls)

from contextlib import contextmanager

@contextmanager
def assert_raises(exception=AssertionError):
    try:
        yield
    except exception:
        pass
    else:
        assert False, "{} not raise".format(exception)

def test():
    num = Asserter(1)
    num < 2
    num > 0
    num == 1
    num.is_(1)
    with assert_raises():
        num <= 0
    with assert_raises():
        num == 2

    d = Asserter(dict(a=3))
    'a' in d 
    d['a'] == 3
    with assert_raises():
        'b' in d
    with assert_raises():
        d['a'] == 4
    
    l = Asserter(range(10))
    
    l.length() == 10
    with assert_raises():
        l.length() == 9
    

if __name__ == '__main__':
    test()
        
    
