from asserter import Asserter, assert_raises

def test_int():
    num = Asserter(1)
    num < 2
    num > 0
    num == 1
    with assert_raises():
        num <= 0
    with assert_raises():
        num == 2
    with assert_raises():
        3 < num < 5
        
def test_dict():
    d = Asserter(dict(a=3))

    'a' in d 
    with assert_raises():
        'b' in d

    d['a'] == 3
    with assert_raises():
        d['a'] == 4

    d.keys() == ['a']
    with assert_raises():
        d.keys() == ['b']

def test_list():
    orig = range(10)
    l = Asserter(orig)
    l.is_(orig)

    l.length() == 10
    with assert_raises():
        l.length() == 9
        

class Animal(object):
    def __init__(self, age):
        self._age = age
    @property
    def age(self):
        return self._age
    def say(self):
        raise NotImplementedError()
    
class Dog(Animal):
    def say(self):
        return "woof"
    
def test_nested():
    orig = Dog(13)
    obj = Asserter(orig)

    obj.is_(orig)
    obj.isinstance(Dog)
    with assert_raises():
        obj.isinstance(int)
        
    obj.say() == "woof"
    
    with assert_raises():
        obj.say() == "quack"

    obj.age == 13
    with assert_raises():
        obj.age == 15
