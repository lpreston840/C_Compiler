import rdp

Var = {}

def make_temporary():
    return f"tmp.{len(Var)}" 

def convert_unop(op):
    match op:
        case rdp.Negate:
            return "negate"
        case rdp.Complement:
            return "Complement"

def emit_tacky(e, instructions):
    match e:
        case rdp.Constant:
            return TACKYConstant(e.data)
        case rdp.Unary:
            src = emit_tacky(e.exp, instructions)
            dst_name = make_temporary()
            dst = Var[dst_name]
            tacky_op = convert_unop(e.unary_operator)
            instructions.append(TACKYUnary(tacky_op, src, dst))
            return dst


class TACKYParser:
    def __init__(self, program):
        self.ast = program
    
    def parse_TACKYOperand(self, op):
        if type(op) == rdp.Constant:
            return TACKYOperand.Imm(op.value)

    def parse_TACKYExpressions(self, body):
        for elm in body:
            if type(elm) == rdp.Return:
                return [Mov(self.parse_TACKYOperand(elm.return_value), TACKYOperand.Register()), Ret()]

    def parse_TACKYFunction(self):
        return TACKYFunction(self.ast.function.name, self.parse_TACKYExpressions(self.ast.function.body))

    def parse_ast(self):
        return TACKYProgram(self.parse_TACKYFunction())

class TACKYProgram:
    def __init__(self, function_def):
        self.func_def = function_def
    
    def __str__(self) -> str:
        return f"TACKYProgram(\n\t{self.func_def}\n)"
    
    def output(self):
        return f"\t.global main\n{self.func_def.output()}"

class TACKYFunction:
    def __init__(self, name, instructions):
        self.label = name
        self.instrs = instructions
    
    def __str__(self) -> str:
        instructions = [str(elm) for elm in self.instrs]
        return f"TACKYFunction(\n\t\tname={self.label},\n\t\tinstructions={instructions}\n\t)"
    
    def output(self):
        instr_text = ""
        for elm in self.instrs:
            instr_text += f"\t{elm.output()}\n"
        return self.label + ':\n' + instr_text

class Mov:
    def __init__(self, source, destination) -> None:
        self.src = source
        self.dst = destination

    def __str__(self) -> str:
        return f"Mov(src={self.src}, dst={self.dst})"
    
    def output(self):
        src_sym = '$' if type(self.src.data) == int else '%'
        dst_sym = '$' if type(self.dst.data) == int else '%'
        return f"movl\t{src_sym}{self.src.data}, {dst_sym}{self.dst.data}"

class Ret:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Ret"
    
    def output(self):
        return "ret"

class TACKYConstant:
    def __init__(self, data) -> None:
        self.data = data

class TACKYUnary:
    def __init__(self, tacky_op, source, destination) -> None:
        self.op = tacky_op
        self.src = source
        self.dst = destination

class TACKYOperand:
    def __init__(self, data):
        self.data = data

    @classmethod
    def Imm(cls, int_num):
        return cls(int_num)
    
    @classmethod
    def Register(cls):
        return cls("eax")
    
    def __str__(self) -> str:
        return str(self.data)