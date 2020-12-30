#!/usr/bin/env python
import os
import re
import argparse
import subprocess
import pcode2code
from oletools.olevba import VBA_Parser


class VBAObject():
    def __init__(self, ioc, dir=""):
        self.ioc = ioc
        self.rev_codes = None # Should be a dic {stream: []}
        self.src_codes = None # Should be a dic {stream: []}

    def set_rev_codes(self, obj):
        self.rev_codes = obj

    def set_src_codes(self, obj):
        self.src_codes = obj

    def print_rev_codes(self):
        for k, v in self.rev_codes.items():
            print(f"Stream: {k}\n{v}\n{'-' * 20}")

    def print_src_codes(self):
        for k, v in self.src_codes.items():
            print(f"Stream: {k}\n{v}\n{'-' * 20}")

def get_code_diff(src, rev):
    code_diff = {}

    if rev is None or src is None:
        return code_diff

    for k in rev.keys():
        if k == "ThisDocument":
            continue

        code_diff[k] = 0
        if k not in src:
            continue
        else:
            total = len(rev[k].strip().split("\n")) + len(src[k].strip().split("\n"))
            with open("rev", "w") as outfile:
                outfile.write(rev[k])
            with open("src", "w") as outfile:
                outfile.write(src[k])
            try:
                cmd = "diff -biB rev src | wc -l"
                ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                output = ps.communicate()[0].decode("utf-8")
                output = int(output.strip())
                code_diff[k] = (output / total)
            except:
                print("Fail to compare source code and reversed code in ", k)
            os.remove("rev")
            os.remove("src")
    return code_diff


def extract_src_codes(file):
    dic = {}
    parser = VBA_Parser(file)
    for (_, sname, _, code) in parser.extract_macros():
        sname = sname.split("/")[-1]
        if sname not in dic:
            lines = code.split("\n")[1: ]
            dic[sname] = "\n".join(lines) # remove the first line
        else:
            print(f"Error in src_codes: repeat {sname}")
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
                    print(f"Error in rev_codes: repeat {stream_name}")
            elif i > 1: # b/c i == 1 is "=" * 40
                l = re.sub(r"[0-9]*: ", "", l)
                dic[stream_name].append(l)

        dic[stream_name] = "\n".join(dic[stream_name])
    return dic


def process(file):
    # Extract pcodes and Reverse into source codes
    temp_file = "temp_for_pcode"
    temp_code = "temp_for_reverse_VBA"
    try:
        subprocess.run(["python3", "pcodedmp.py", "-d", file, "-o", temp_file])
    except:
        print("Fail to execute the pcodedump library.")
    try:
        pcode2code.process(temp_file, temp_code, ispcodedump=True)
    except:
        print("Fail to process pcode to source code.")
    raw = open(temp_code, "r").read()

    # Remove the temporary file used to store the cache pcodes
    if os.path.isfile(temp_file):
        os.remove(temp_file)
    if os.path.isfile(temp_code):
        os.remove(temp_code)
    return raw


def main():

    parser = argparse.ArgumentParser(description="Analyzing VBA.")
    parser.add_argument("-f", "--file", action="store", type=str,
                        help="specify a valid Office .doc file.")
    parser.add_argument("-d", "--dir", action="store", type=str, default=os.getcwd(),
                        help="specify a existing folder to store output (optional).")
    args = parser.parse_args()

    # Prepare the arguments
    file, folder = args.file, args.dir
    assert os.path.isfile(file)
    assert os.path.isdir(folder)

    # Process file content into VBAObject
    vbaobj = VBAObject(ioc=file, dir=folder) # ioc is used to name the output file
    src_codes_dic = extract_src_codes(file)
    vbaobj.set_src_codes(src_codes_dic)
    
    # Process raw reverse source codes into one or more code sections 
    raw_rev_codes = process(file)
    rev_codes_dic = extract_rev_codes(raw_rev_codes)
    vbaobj.set_rev_codes(rev_codes_dic)
    
    # Compare two kind of source codes
    diff = get_code_diff(vbaobj.src_codes, vbaobj.rev_codes)


if __name__ == '__main__':
    main()
