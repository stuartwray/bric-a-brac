#!/usr/bin/python3
# A python version of some code from Douglas Crockford's
# "Monads and Gonads" talk (15 Jan 2013)
# http://www.youtube.com/watch?v=b0EF0VTs9Dc
# (I wrote this so I could properly understand what his Javascript was doing.)

# video 15:00

# Define a little class so we can make vanilla objects. (We can't set
# attributes on instances of "object", but we can on instances of this class.)
class Obj:
    pass

def MONAD():
    def unit(value):
        monad = Obj()
        def bind(self, func):
            return func(value)
        # Can't just assign a function as a method of an object in python,
        # since it won't know what object it belongs to. Hence this trickery,
        # which makes a bound-method from a function.
        monad.bind = bind.__get__(monad, Obj)
        return monad

    return unit

# video 16:30

alert = print # print can stand in for alert

identity = MONAD()
monad = identity("Hello world.")
monad.bind(alert)

# A little slight-of-hand went on there, because the type of alert
# doesn't conform to the monad rules as explained after 12:00 in the video.
# Rather than being of type Value -> Monad, it's of type Value -> NotAMonad,
# so we couldn't chain binds in the obviously desirable way. But it makes
# a more straightforward example for now, and the next example does it right.

# video 22:20
# we need to use classes, not prototypes, but we can make it similar

def MONAD():
    # Prototype is actually a dynamically created class
    Prototype = type("NotReallyAPrototype", (), {})
    def unit(value):
        monad = Prototype()
        def bind(self, func, *args):
            return func(value, *args)
        monad.bind = bind.__get__(monad, Obj)
        return monad

    def method(name, func):
        setattr(Prototype, name, func)
        return unit
    unit.method = method

    def lift(name, func):
        def wrapper(self, *args):
            return unit(self.bind(func, *args))
        setattr(Prototype, name, wrapper)
        return unit
    unit.lift = lift

    return unit

# video 24:00

ajax = MONAD().lift("alert", alert)
monad = ajax("Hello world.")
monad.alert()

# video 27:00

def MONAD(modifier):
    # Prototype is actually a dynamically created class
    Prototype = type("NotReallyAPrototype", (), {})
    def unit(value):
        monad = Prototype()
        def bind(self, func, *args):
            return func(value, *args)
        monad.bind = bind.__get__(monad, Obj)
        if callable(modifier):
            modifier(monad, value)
        return monad

    return unit

# video 27:15

def MaybeModifier(monad, value):
    if value == None:
        monad.is_null = True
        def bind(self, *args):
            return monad
        monad.bind = bind.__get__(monad, Obj)
    else:
        # can't leave is_null to be undefined in this branch ...
        monad.is_null = False  

maybe = MONAD(MaybeModifier)
monad = maybe(None)

print("This should do nothing ...")
monad.bind(alert)
print("... did it?")

# There's more stuff in the talk about promises, but I'll leave that as
# an "exercise for the reader" ... (see douglascrockford/monad on GitHub)

