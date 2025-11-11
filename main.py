import lexer
import rdp
import TACKY
import assembly_ast
import subprocess
import argparse


def main():
    arg_parser = argparse.ArgumentParser(description="C compiler written in Python")
    arg_parser.add_argument("input_file", type=str)
    arg_parser.add_argument("--lex", default=False, help="Only runs the lexer")
    arg_parser.add_argument("--parse", default=False, help="Only runs the parser")
    arg_parser.add_argument("--tacky", default=False, help="Only runs up to the IR generation")
    arg_parser.add_argument("--codegen", default=False, help="Only runs up to assembly generation")

    args = arg_parser.parse_args()
    
    subprocess.run(["gcc", "-E", "-P", args.input_file, "-o", "preprocessed.i"])
    code = open("preprocessed.i", 'r').read().strip()
    if args.lex:
        print(lexer.tokenize(code))
    elif args.parse:
        print(rdp.Parser(lexer.tokenize(code)).parse_program())
    elif args.tacky:
        print(TACKY.TACKYParser(rdp.Parser(lexer.tokenize(code)).parse_program()).parse_ast())
    elif args.codegen:
        print(assembly_ast.ASMParser(rdp.Parser(lexer.tokenize(code)).parse_program()).parse_ast())
    else:
        asm_name = args.input_file[:args.input_file.index('.')] + ".s"
        open(asm_name, 'w').write(assembly_ast.ASMParser(rdp.Parser(lexer.tokenize(code)).parse_program()).parse_ast().output())
        subprocess.run(["gcc", asm_name, "-o", asm_name[:asm_name.index('.')]])
        #subprocess.run(["rm", asm_name])
        subprocess.run(["rm", "preprocessed.i"])

main()