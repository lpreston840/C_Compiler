from enum import Enum

# Todo:
# [] Convert unops to enums
# [] Make parse_binop function
# [] Find other uses for enums and incorporate

class Parser:
    def __init__(self, toks) -> None:
        self.tokens = toks
    
    def _precedence(self, op):
        if op == "/" or op == "*" or op == "%":
            return 50
        elif op == "+" or op == "-":
            return 45
        
        # one-liner of the above code
        #return 50 if op in ["/", "*", "%"] else 45 #if op in ["+", "-"] else ...

    def expect(self, expected):
        actual = self.tokens.pop(0)
        if actual != expected:
            raise SyntaxError(f"Unexpected Token: {actual}")
    
    def parse_factor(self):
        next_token = self.tokens[0]
        
        if next_token.isdigit():
            return Constant(int(self.tokens.pop(0)))
        elif next_token == "-" or next_token == "~":
            operator = self.parse_unop()
            inner_exp = self.parse_factor()
            return Unary(operator, inner_exp)
        elif next_token == "(":
            self.tokens.pop(0)
            inner_exp = self.parse_exp(0)
            self.expect(")")
            return inner_exp
        else:
            raise SyntaxError("Malformed Expression")

    def parse_exp(self, min_prec):
        left = self.parse_factor()
        next_token = self.tokens[0]

        while next_token in ["/", "*", "%", "+", "-"] and self._precedence(next_token) >= min_prec:
            operator = self.parse_binop()
            right = self.parse_exp(self._precedence(next_token) + 1)
            left = Binary(left, operator, right)
            next_token = self.tokens[0]
    
        return left
    
    def parse_binop(self):
        operator = self.tokens.pop(0)

        match operator:
            case "+":
                return Binop.ADD
            case "-":
                return Binop.SUBTRACT
            case "*":
                return Binop.MULTIPLY
            case "/":
                return Binop.DIVIDE
            case "%":
                return Binop.MODULO

    def parse_unop(self):
        operator = self.tokens.pop(0)

        if operator == "-":
            return Negate()
        else:
            return Complement()

    def parse_identifier(self):
        return Identifier(self.tokens.pop(0))

    def parse_statement(self):
        self.expect("return")
        return_val = self.parse_exp(0)
        self.expect(";")
        return Return(return_val)
    
    def parse_function(self):
        self.expect("int")
        name = self.parse_identifier().name
        self.expect("(")
        self.expect("void")
        self.expect(")")
        self.expect("{")
        statement = self.parse_statement()
        self.expect("}")
        return Function(name, [statement])
    
    def parse_program(self):
        return Program(self.parse_function())



class Program:
    def __init__(self, func) -> None:
        self.function = func
    
    def __str__(self) -> str:
        return f"Program(\n\t{self.function}\n)"

class Function:
    def __init__(self, name, body) -> None:
        self.name = name
        self.body = body
    
    def __str__(self) -> str:
        body_str = ""

        for elm in self.body:
            body_str += str(elm)

        return f"Function(\n\t\tname = {self.name},\n\t\tbody = " + body_str + "\n\t)"

class Return:
    def __init__(self, value):
        self.return_value = value
    
    def __str__(self) -> str:
        return f"Return({self.return_value})"

class Identifier:
    def __init__(self, name) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return f"Identifier({self.name})"

class Constant:
    def __init__(self, val):
        self.value = val
    
    def __str__(self) -> str:
        return f"Constant({self.value})"

class Complement:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Complement"

class Negate:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Negate"

class Unary:
    def __init__(self, unop, expression) -> None:
        self.unary_operator = unop
        self.exp = expression
    
    def __str__(self) -> str:
        return f"Unary({self.unary_operator}, {self.exp})"

class Binop(Enum):
    ADD = 0
    SUBTRACT = 1
    MULTIPLY = 2
    DIVIDE = 3
    MODULO = 4

    def __str__(self) -> str:
        return super().__str__()

# exp1 should be the left hand expression and exp2 shuold be the right hand expression
class Binary:
    def __init__(self, ex1, op, ex2) -> None:
        self.exp1 = ex1
        self.operator = op
        self.exp2 = ex2
    
    def __str__(self) -> str:
        return f"Binary({self.operator}, {self.exp1}, {self.exp2})"