import re

# 0 = regex for identifier, 1 = regex for constant
TOKEN_REGEX = [r"[a-zA-Z_]\w*\b", r"[0-9]+\b", r"\--", r"\-", r"\+", r"\*", r"\/", r"\%", r"~", r"\(", r"\)",r"{", r"}", r";"]

def tokenize(program: str) -> list:
    program_remaining = program
    tokens = []
    while program_remaining != "":
        program_remaining = program_remaining.lstrip()

        for ex in TOKEN_REGEX:
            curr_token = re.match(ex, program_remaining)
            if curr_token:
                tokens.append(curr_token[0])
                program_remaining = program_remaining[len(curr_token[0])::]
                break
            elif ex == r";":
                raise SyntaxError(f"Unrecognized token: {program_remaining}")

    return tokens