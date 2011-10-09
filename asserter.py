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
    
    def __call__(self, *args, **kwargs):
        return type(self)(self.obj(*args, **kwargs))

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

    def isinstance(self, cls):
        result = isinstance(self.obj, cls)
        if not result:
            raise AssertionError("{} is not an instance of {}".format(self.obj, cls))
        return result

from contextlib import contextmanager

@contextmanager
def assert_raises(exception=AssertionError):
    try:
        yield
    except exception:
        pass
    else:
        assert False, "{} not raise".format(exception)        
    
