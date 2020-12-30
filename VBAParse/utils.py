#!/usr/bin/env python
import os, re
import subprocess
from ysj_io          import printError
from VBAParse        import pcode2code
from oletools.olevba import VBA_Parser

def extract_src_codes(file):
    dic = {}
    parser = VBA_Parser(file)
    for (_, sname, _, code) in parser.extract_macros():
        sname = sname.split("/")[-1]
        if sname not in dic:
            lines = code.split("\n")[1: ]
            dic[sname] = "\n".join(lines) # remove the first line
        else:
            printError(f"Error in src_codes: repeat {sname}")
    return dic


def extract_rev_codes(raw):
    dic = {}
    for rev in raw.split("stream : "):
        lines = [l for l in rev.split("\n") if l != ""]
        if len(lines) == 0:
            continue
        stream_name = None
        for i, l in enumerate(lines):
            # Extract Stream Name
            if i == 0:
                stream_name = l.split(" ")[0].split("/")[-1]
                if stream_name not in dic:
                    dic[stream_name] = []
                else:
                    printError(f"Error in rev_codes: repeat {stream_name}")
            elif i > 1: # b/c i == 1 is "=" * 40
                l = re.sub(r"[0-9]*: ", "", l)
                dic[stream_name].append(l)

        dic[stream_name] = "\n".join(dic[stream_name])
    return dic


def process(file):
    # Extract pcodes and Reverse into source codes
    folder = os.path.dirname(__file__)
    temp_file = os.path.join(folder, "temp_for_pcode")
    temp_code = os.path.join(folder, "temp_for_reverse_VBA")
    try:
        subprocess.run(["python3", "./VBAParse/pcodedmp.py", "-d", file, "-o", temp_file])
    except:
        printError("Fail to execute the pcodedump library.")
    try:
        pcode2code.process(f"{temp_file}", temp_code, ispcodedump=True)
    except:
        printError("Fail to process pcode to source code.")
    raw = open(temp_code, "r").read()

    # Remove the temporary file used to store the cache pcodes
    if os.path.isfile(temp_file):
        os.remove(temp_file)
    if os.path.isfile(temp_code):
        os.remove(temp_code)
    return raw
