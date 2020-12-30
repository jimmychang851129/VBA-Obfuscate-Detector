from pygments import highlight
from pygments.lexers import VBScriptLexer
from pygments.formatter import Formatter
from pygments.token import Token

class MyFormatter(Formatter):
    def __init__(self, **options):
        super().__init__(**options)
        self.token_list = list()
    def format(self, tokensource, outfile):
        for type, value in tokensource:
            if type != Token.Text.Whitespace:
                if type == Token.Name and (value.lower() =='chrw' or value.lower() =='chrb'):
                    type = Token.Name.Builtin
                self.token_list.append((type, value))

def SimpleTokenParser(source_code: str) -> list:
    """Tokenize the source code to pygments.token.Token.Return a list of (type, value) tuples.
    """
    myFormatter = MyFormatter()
    highlight(source_code, VBScriptLexer(), myFormatter)
    return myFormatter.token_list

if __name__ == "__main__":
    code = '''
    Sub AAA():
        A = Array(1,2,3,4,5, Chr(123), ChrB(234), ChrW(3453))
        cHr(123)
        ChR(234)
    End Sub
    '''
    code = code.strip().split('\n')
    print(code)
    for c in code:
        print(SimpleTokenParser(c))