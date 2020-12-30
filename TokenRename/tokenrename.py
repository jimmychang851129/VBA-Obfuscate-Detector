from pygments import highlight
from pygments.lexers import VBScriptLexer
from pygments.formatter import Formatter
from pygments.token import Token
import math, os, sys
import argparse
sys.path.append("../")
from VBParser import SimpleTokenParser

charlist = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

def countEntropy(chardict,cnt):
    entropy = 0
    for key in chardict.keys():
        if chardict[key] != 0:
            p = chardict[key] / cnt
            entropy -= p * math.log(p)
    return entropy

# [All, Token.Name,Token.Function,Token.Literal.String.Double]
def Entropy(l):
    cnt = 0
    EntroList = []
    chardict = dict()
    for c in charlist:
        chardict[c] = 0
    for s in l.keys():
        for ele in l[s]:
            for c in ele:
                if c not in chardict:
                    # print("[Entropy]: %c not in chardict"%(c))
                    continue
                chardict[c]+= 1
                cnt += 1
    EntroList.append(countEntropy(chardict,cnt))
    tokenlist = [Token.Name,Token.Name.Function,Token.Literal.String.Double]
    for token in tokenlist:
        cnt = 0
        chardict = dict()
        for c in charlist:
            chardict[c] = 0
        if token in l:
            for ele in l[token]:
                for c in ele:
                    if c not in chardict:
                        # print("[Entropy]: %c not in chardict"%(c))
                        continue
                    chardict[c]+= 1
                    cnt += 1
            EntroList.append(countEntropy(chardict,cnt))
        else:
            EntroList.append(0)   
    return EntroList

# Token.Name.Variable: Null
def getToken(code):
    whitelist = set({Token.Literal.String.Double,Token.Name,Token.Name.Function})
    tokenlist = SimpleTokenParser(code)
    l = dict()
    for token in tokenlist:
        if token[0] in whitelist:
            if token[0] not in l:
                l[token[0]] = []
            if token[0] == Token.Literal.String.Double and len(token[1]) <= 4:
                continue
            l[token[0]].append(token[1])
    return l

def getVar(tokenlist):
    varlist = []
    for ele in tokenlist[Token.Name]:
        if Token.Name.Function not in tokenlist or ele not in tokenlist[Token.Name.Function]:
            varlist.append(ele)
    tokenlist.pop(Token.Name,None)
    tokenlist[Token.Name] = varlist
    return tokenlist

# string.double beware length
# builtin may contains op such as strreverse...
def getEntropy(dirpath):
    EntropyList = []
    filelist = []
    for file in os.listdir(dirpath):
        inputfile = os.path.join(dirpath,file)
        code = open(inputfile,'r').read()
        tokenlist = getToken(code)
        tokenlist = getVar(tokenlist)
        EntropyList.append(Entropy(tokenlist))
        filelist.append(file)
    return EntropyList,filelist

def writeFile(filelist,EntropyList,outputdir):
    filepath = os.path.join(outputdir,"entropy.csv")
    with open(filepath,'w') as fw:
        fw.write("Filename,Overall Entropy,Variable Name Entropy,Function Name Entropy,Strings Entropy\n")
        for i in range(len(EntropyList)):
            out = ",".join([str(x) for x in EntropyList[i]])
            fw.write(filelist[i]+","+out+"\n")

def CalculateSingleEntropy(filepath):
    code = open(filepath,'r').read()
    tokenlist = getToken(code)
    tokenlist = getVar(tokenlist)
    return Entropy(tokenlist)

def ParseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir",'-i', type=str, help='macros dir')
    parser.add_argument("--outputdir",'-o', type=str, help='outputdir')
    parser.add_argument("--test",'-t', help="only calculate entropy of single file",action='store_true')
    parser.add_argument("--file",'-f', type=str, help="Single file path, only used when args.test specified")
    args = parser.parse_args()
    return args

def PrintResult(ret):
    entropyName = ["Overall Entropy","Variable Name Entropy","Function Name Entropy","Strings Entropy"]
    Threshold = [3.5,3.31,2.6,2.18]
    cnt = 0
    for i in range(len(ret)):
        print("%s ... %f / %f ... %s"%(entropyName[i],ret[i],Threshold[i]))
        if ret[i] > Threshold[i]:
            cnt += 1
    if cnt >= 2:
        print("Token Renaming Detection ... True")
    else:
        print("Token Renaming Detection ... False")

def main(args):
    if args.test == True:
        ret = CalculateSingleEntropy(args.file)
        PrintResult(ret)
    else:
        entrolist, filelist = getEntropy(args.inputdir)
        writeFile(filelist,entrolist,args.outputdir)

if __name__ == '__main__':
    args = ParseArg()
    main(args)
