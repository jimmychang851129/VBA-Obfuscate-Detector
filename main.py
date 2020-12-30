#!/usr/bin/env python
import os
import argparse
from tqdm                    import tqdm
from VBAParse.VBAObject      import VBAObject
from VBAParse.utils          import process, extract_src_codes, extract_rev_codes
from PcodeCompare.detector   import CodeDiffDetect
from TokenConcat.detector    import StringConcatDetect
from TokenRename.tokenrename import CalculateSingleEntropy
from JumpControlFlow.detector import FunctionChainDetect

def main():
    parser = argparse.ArgumentParser(description="Analyzing VBA.")
    parser.add_argument("-f", "--file", action="store", type=str,
                        help="specify a valid Office .doc file.")
    args = parser.parse_args()

    # Prepare the arguments
    file = args.file
    assert os.path.isfile(file)

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
        for k in tqdm(vbaobj.src_codes.keys()):
            if k == "ThisDocument":
                continue
            print(k)
            src = vbaobj.src_codes[k]
            rev = vbaobj.rev_codes[k] if k in vbaobj.rev_codes else src
            try: # Tag 1.
                CodeDiffDetect(src, rev)
            except:
                pass
            try: # Tag 2.
                StringConcatDetect(rev)
            except:
                pass
            try: # Tag 3.
                CalculateSingleEntropy(rev)
            except:
                pass
            try: # Tag 4.??
                FunctionChainDetect(rev)
            except:
                pass


if __name__ == '__main__':
    main()
