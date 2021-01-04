#!/usr/bin/env python
import os
import argparse
from tqdm                     import tqdm
from PyInquirer               import prompt
# Self-defined modules
from ysj_io                   import printTitle, printError
from VBAParse.VBAObject       import VBAObject
from VBAParse.utils           import process, extract_src_codes, extract_rev_codes
from PcodeCompare.detector    import CodeDiffDetect
from TokenConcat.detector     import StringConcatDetect
from TokenRename.tokenrename  import CalculateSingleEntropy
from JumpControlFlow.detector import FunctionChainDetect

global QUESTIONS
QUESTIONS = [
    {
        "type": "list",
        "name": "action",
        "message": "What do you want to do?",
        "choices": ["Detect a file", "Exit"],
    },{
        "type": "input",
        "name": "file",
        "message": "Which file do you want to check?",
    }
]

def main():

    action = prompt(QUESTIONS[0])["action"]
    if action == "Exit":
        exit()

    file = prompt(QUESTIONS[1])["file"]
    if not os.path.isfile(file):
        printError("Please provide a valid Office Document file.")
        exit()

    # Process file content into VBAObject    
    src_codes_dic = extract_src_codes(file)
    raw_rev_codes = process(file)
    rev_codes_dic = extract_rev_codes(raw_rev_codes)
    vbaobj = VBAObject(
        ioc=file,
        rev_codes=rev_codes_dic,
        src_codes=src_codes_dic
    )
    
    # Compare two kind of source codes
    if vbaobj.src_codes is not None:
        for k in vbaobj.src_codes.keys():
            if k == "ThisDocument":
                continue
            printTitle(k)
            src = vbaobj.src_codes[k]
            rev = vbaobj.rev_codes[k] if k in vbaobj.rev_codes else src
            target = rev
            if len(src) != len(rev):
                target = src
            try: # Tag 1.
                CodeDiffDetect(src, rev)
            except:
                pass
            try: # Tag 2.
                StringConcatDetect(target)
            except:
                pass
            try: # Tag 3.
                CalculateSingleEntropy(target)
            except:
                pass
            try: # Tag 4.
                FunctionChainDetect(target)
            except:
                pass


if __name__ == '__main__':
    print('''
   _______  __    __   ____  __    ____                      __          ____       __            __            
  / ___/\\ \\/ /   / /  / __ \\/ /_  / __/_  ________________ _/ /____     / __ \\___  / /____  _____/ /_____  _____
  \\__ \\  \\  /_  / /  / / / / __ \\/ /_/ / / / ___/ ___/ __ `/ __/ _ \\   / / / / _ \\/ __/ _ \\/ ___/ __/ __ \\/ ___/
 ___/ /  / / /_/ /  / /_/ / /_/ / __/ /_/ (__  ) /__/ /_/ / /_/  __/  / /_/ /  __/ /_/  __/ /__/ /_/ /_/ / /    
/____/  /_/\\____/   \\____/_.___/_/  \\__,_/____/\\___/\\__,_/\\__/\\___/  /_____/\\___/\\__/\\___/\\___/\\__/\\____/_/     
                                                                                                                 
    VBA Obfuscation Detection Tools
    By @Yvonne, @Shupo, @Jimmy
    ''')

    # while True:
    main()
