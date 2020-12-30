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

def StringConcatDetect(src: str):
    token_list = _getTokens(src)
    CountArray(token_list)
    #TODO: Chr, ChrW, ChrB
    #TODO: +, &, XOR
    #TODO: case sensitive?
    pass
if __name__ == "__main__":
    with open('test_cases/test_array_detect.txt', 'r') as f:
        code = f.read()
    StringConcatDetect(code)
    '''
    with open('test_cases/test_array_detect_2.txt', 'r') as f:
        code = f.read()
    StringConcatDetect(code)
    '''