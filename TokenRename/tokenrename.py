from pygments import highlight
from pygments.lexers import VBScriptLexer
from pygments.formatter import Formatter
from pygments.token import Token
import math, os, sys
import argparse
sys.path.append("../")

charlist = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

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


def Entropy(l):
    cnt = 0
    chardict = dict()
    for c in charlist:
        chardict[c] = 0
    for s in l:
        for c in s:
            if c not in chardict:
                print("[Entropy]: %c not in chardict"%(c))
                continue
            chardict[c]+= 1
            cnt += 1
    entropy = 0
    for key in chardict.keys():
        if chardict[key] != 0:
            p = chardict[key] / cnt
            entropy -= p * math.log(p)
    return entropy

def getToken(code):
    whitelist = set({Token.Literal.String.Double,Token.Name,Token.Name.Variable,Token.Name.Function})
    tokenlist = SimpleTokenParser(code)
    l = []
    for token in tokenlist:
        if token[0] in whitelist:
            if token[0] == Token.Literal.String.Double and len(token[1]) <= 4:
                continue
            l.append(token[1])
    return l

# string.double beware length
# builtin may contains op such as strreverse...
def getEntropy(dirpath):
    EntropyList = []
    filelist = []
    for file in os.listdir(dirpath):
        inputfile = os.path.join(dirpath,file)
        code = open(inputfile,'r').read()
        tokenlist = getToken(code)
        EntropyList.append(Entropy(tokenlist))
        filelist.append(file)
    return EntropyList,filelist

def writeFile(filelist,EntropyList):
    with open("entropy.csv",'w') as fw:
        for i in range(len(EntropyList)):
            fw.write(filelist[i]+","+str(EntropyList[i])+"\n")

def CalculateSingleEntropy(filepath):
    code = open(filepath,'r').read()
    tokenlist = getToken(code)
    return Entropy(tokenlist)

def ParseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir",'-i', type=str, help='macros dir')
    parser.add_argument("--outputdir",'-o', type=str, help='outputdir')
    parser.add_argument("--test",'-t', help="only calculate entropy of single file",action='store_true')
    parser.add_argument("--file",'-f', type=str, help="Single file path, only used when args.test specified")
    args = parser.parse_args()
    return args

def main(args):
    if args.test == True:
        ret = CalculateSingleEntropy(args.file)
        print("entropy = ",ret)
    else:
        entrolist, filelist = getEntropy(args.inputdir)
        writeFile(filelist,entrolist,args.outputdir)

if __name__ == '__main__':
    args = ParseArg()
    main(args)
