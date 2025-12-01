import rdp
from enum import Enum

Vars = {}

def make_temporary():
    return f"tmp.{len(Vars)}" 

class TACKYParser:
    def __init__(self, program):
        self.ast = program
        self.instructions = []
    
    def emit_tacky(self, e):
        #print(e)
        match type(e):
            case rdp.Constant:
                return TACKYConstant(e.value)
            case rdp.Unary:
                src = self.emit_tacky(e.exp)
                dst_name = make_temporary()
                Vars[dst_name] = TACKYVar(dst_name)
                dst = Vars[dst_name]
                op = e.unary_operator
                self.instructions.append(TACKYUnary(op, src, dst))
                for elm in self.instructions:
                    print(elm)
                return dst
            case rdp.Binary:
                v1 = self.emit_tacky(e.exp1)
                v2 = self.emit_tacky(e.exp2)
                op = e.operator
                dst_name = make_temporary()
                Vars[dst_name] = TACKYVar(dst_name)
                dst = Vars[dst_name]
                self.instructions.append(TACKYBinary(op, v1, v2, dst))
                return dst


    def parse_TACKYExpressions(self, body):
        for elm in body:
            if type(elm) == rdp.Return:
                self.instructions.append(TACKYReturn(self.emit_tacky(elm.return_value)))

    def parse_TACKYFunction(self):
        self.parse_TACKYExpressions(self.ast.function.body)
        return TACKYFunction(self.ast.function.name, self.instructions)

    def parse_ast(self):
        return TACKYProgram(self.parse_TACKYFunction())

class TACKYProgram:
    def __init__(self, function_def):
        self.func_def = function_def
    
    def __str__(self) -> str:
        return f"TACKYProgram(\n\t{self.func_def}\n)"

class TACKYFunction:
    def __init__(self, name, instructions):
        self.label = name
        self.instrs = instructions
    
    def __str__(self) -> str:
        instructions = ""
        for elm in self.instrs:
            instructions += str(elm) + ",\n\t\t\t     "
        return f"TACKYFunction(\n\t\tname={self.label},\n\t\tinstructions={instructions}\n\t)"

class TACKYReturn:
    def __init__(self, expression) -> None:
        self.exp = expression

    def __str__(self) -> str:
        return f"Return({self.exp})"

class TACKYConstant:
    def __init__(self, data) -> None:
        self.data = data
    
    def __str__(self) -> str:
        return f"Constant({self.data})"

class TACKYUnary:
    def __init__(self, tacky_op, source, destination) -> None:
        self.operator = tacky_op
        self.src = source
        self.dst = destination
    
    def __str__(self) -> str:
        return f"Unary({self.op}, {self.src}, {self.dst})"

class TACKYBinary:
    def __init__(self, tacky_op, source1, source2, destination) -> None:
        self.operator = tacky_op
        self.src1 = source1
        self.src2 = source2
        self.dst = destination
    
    def __str__(self) -> str:
        return f"Binary({self.op}, {self.src1}, {self.src2}, {self.dst})"

class TACKYVar:
    def __init__(self, name) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return f"Var({self.name})"