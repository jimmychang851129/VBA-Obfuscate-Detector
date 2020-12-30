from VBParser import SimpleTokenParser
from pygments.token import Token

def _getTokens(src: str):
    # remove underline '_'
    src = src.replace('_\n', '')
    src = src.strip().split('\n')
    token_list = []
    for s in src:
        if s != '':
            token_list.append(SimpleTokenParser(s))
    return token_list

def _doCountArray(tokens, idx):
    if idx >= len(tokens):
        return 0, 0
    arr_count, ascii_arr_count = 0, 0
    in_array = False
    is_ascii = True
    parent_stack = 0
    i = idx
    while i < len(tokens):
        if tokens[i] == (Token.Name.Builtin, 'Array'):
            if in_array:
                arr_c, ascii_c, new_idx = _doCountArray(tokens, i)
                arr_count += arr_c
                ascii_arr_count += ascii_c
                i = new_idx
                continue
            else:
                in_array = True
                arr_count += 1
        elif tokens[i] == (Token.Punctuation, '('):
            if in_array:
                parent_stack += 1
        elif tokens[i] == (Token.Punctuation, ')'):
            if in_array:
                parent_stack -= 1
                if parent_stack == 0:
                    if is_ascii:
                        ascii_arr_count += 1
                    in_array = False
        elif parent_stack > 0:
            if tokens[i][0] == Token.Literal.Number.Integer:
                val = int(tokens[i][1])
                if val < 0 and val > 255:
                    is_ascii = False
        i += 1
    return arr_count, ascii_arr_count, i
def CountArray(token_list: list):
    arr_count, ascii_arr_count = 0, 0
    for tokens in token_list:
        c1, c2, _ = _doCountArray(tokens, 0)
        arr_count += c1
        ascii_arr_count += c2
    print('Array Count: {}, ASCII Array Count: {}'.format(arr_count, ascii_arr_count))
def CheckChr(token_list: list):
    use_chr, use_chrB, use_chrW = False, False, False
    for tokens in token_list:
        for token in tokens:
            if token[0] == Token.Name.Builtin:
                t_name = token[1].lower()
                if  t_name == 'chr':
                    use_chr = True
                elif t_name == 'chrb':
                    use_chrB = True
                elif t_name == 'chrw':
                    use_chrW = True
    print('Using Chr: {}, Using ChrB: {}, Using ChrW: {}'.format(use_chr, use_chrB, use_chrW))
def CountConcatOperator(token_list: list, operator: str):
    op_count, str_op_count = 0, 0
    for tokens in token_list:
        for i, token in enumerate(tokens):
            if token[0] == Token.Operator:
                if token[1] == operator:
                    op_count += 1
                    if (i - 1 >= 0 and tokens[i-1][0] == Token.Literal.String.Double) or\
                        (i + 1 < len(tokens) and tokens[i+1][0] == Token.Literal.String.Double):
                        str_op_count += 1
    print('Operator \'{}\' Count: {}, String Concat Operator \'{}\' Count: {}'.format(operator, op_count, operator, str_op_count))
def StringConcatDetect(src: str):
    token_list = _getTokens(src)
    CountArray(token_list)
    CheckChr(token_list)
    CountConcatOperator(token_list, '+')
    CountConcatOperator(token_list, '&')
if __name__ == "__main__":
    with open('test_cases/test_array_detect.txt', 'r') as f:
        code = f.read()
    StringConcatDetect(code)
    print('==========================')
    with open('test_cases/test_string_operator.txt', 'r') as f:
        code = f.read()
    StringConcatDetect(code)