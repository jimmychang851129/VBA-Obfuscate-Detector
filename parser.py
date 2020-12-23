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
                self.token_list.append((type, value))

def SimpleTokenParser(source_code: str) -> list:
    """Tokenize the source code to pygments.token.Token.Return a list of (type, value) tuples.
    """
    myFormatter = MyFormatter()
    highlight(source_code, VBScriptLexer(), myFormatter)
    return myFormatter.token_list

if __name__ == "__main__":
    code = 'Sub AAA()\nMsgbox("Fake + Sub")\nDim GG\nGG = 2+2\nEnd Sub'
    print(SimpleTokenParser(code))