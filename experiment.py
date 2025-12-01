class bar:
    def __init__(self) -> None:
        pass

    @classmethod
    def foo(cls, a, b):
        cls.a = a
        cls.b = b
        return cls()
    
    def __str__(self) -> str:
        if type(self) == bar.foo:
            return "foo1"
        else:
            return "bar"
    
inst = bar.foo(1, 2)
print(inst)
