import rdp
import TACKY
from enum import Enum

Psudeos = {}

# May emit a tuple, so be sure to watch out for that
class ASMParser:
    def __init__(self, program):
        self.ast = program
    
    def emit_ASMTree(self, e):
         match type(e):
            case TACKY.TACKYConstant:
                return ASMOperand.Imm(e.value)
            case TACKY.TACKYVar:
                 Psudeos[e.name] = ASMOperand.Psudeo(e.name)
                 return Psudeos[e.name]
            case TACKY.TACKYUnary:
                src = self.emit_ASMTree(e.src)
                dst = self.emit_ASMTree(e.dst)
                op = e.operator
                return ASMInstruction.Mov(src, dst), ASMInstruction.ASMUnary(op, dst)

    def parse_ASMOperand(self, op):
        if type(op) == rdp.Constant:
            return ASMOperand.Imm(op.value)

    def parse_ASMExpressions(self, body):
        instrs = []
        for elm in body:
            next_instrs = self.emit_ASMTree(elm)
            if type(next_instrs) == tuple:
                for e in next_instrs:
                    instrs.append(e)
            else:
                instrs.append(next_instrs)

    def parse_ASMFunction(self):
        return ASMFunction(self.ast.function.name, self.parse_ASMExpressions(self.ast.function.body))

    def parse_ast(self):
        return ASMProgram(self.parse_ASMFunction())

class ASMProgram:
    def __init__(self, function_def):
        self.func_def = function_def
    
    def __str__(self) -> str:
        return f"ASMProgram(\n\t{self.func_def}\n)"
    
    def output(self):
        return f"\t.global main\n{self.func_def.output()}"

class ASMFunction:
    def __init__(self, name, instructions):
        self.label = name
        self.instrs = instructions
    
    def __str__(self) -> str:
        instructions = [str(elm) for elm in self.instrs]
        return f"ASMFunction(\n\t\tname={self.label},\n\t\tinstructions={instructions}\n\t)"
    
    def output(self):
        instr_text = ""
        for elm in self.instrs:
            instr_text += f"\t{elm.output()}\n"
        return self.label + ':\n' + instr_text

class Reg(Enum):
    AX = 0
    R10 = 1

class ASMInstruction:
    def __init__(self) -> None:
        pass

    @classmethod
    def Mov(cls, source, destination):
        cls.src = source
        cls.dst = destination
        return cls()
    
    @classmethod
    def ASMUnary(cls, unary_operator, operand):
        cls.operator = unary_operator
        cls.operand = operand
        return cls()
    
    @classmethod
    def AllocateStack(cls, val):
        cls.value = val
        return cls()
    
    @classmethod
    def Ret(cls):
        return cls()

class ASMOperand:
    def __init__(self):
        pass

    @classmethod
    def Imm(cls, int_num):
        cls.value = int_num
        return cls()
    
    @classmethod
    def Register(cls, register):
        cls.reg = register
        return cls()
    
    @classmethod
    def Psudeo(cls, identifier):
        cls.ident = identifier
        return cls()

    @classmethod
    def Stack(cls, integer):
        cls.value = integer
        return cls()
    
    def __str__(self) -> str:
        return str(self.data)