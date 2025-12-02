class bar:
    def __init__(self) -> None:
        pass

    @classmethod
    def foo(cls, a, b):
        cls.a = a
        cls.b = b
        return cls()
    
    def __str__(self) -> str:
        if self == bar.foo:
            return "foo"
        else:
            return str(type(self))
    
inst = bar.foo(1, 2)
print(inst)
