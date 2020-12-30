import os, subprocess
from ysj_io import printResult

def CodeDiffDetect(src, rev):
    diff = 0
    total = len(rev.strip().split("\n")) + len(src.strip().split("\n"))
    with open("rev", "w") as outfile:
        outfile.write(rev)
    with open("src", "w") as outfile:
        outfile.write(src)
    try:
        cmd = "diff -biB rev src | wc -l"
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ps.communicate()[0].decode("utf-8")
        output = int(output.strip())
        diff = output / total
    except:
        print("Fail to compare source code and reversed code in ", k)
    os.remove("rev")
    os.remove("src")

    result = {"Difference Rate between Source and Pcode": (diff, 0.5)}
    printResult("P-Code Stomping", result)
