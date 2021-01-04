import os, subprocess
from ysj_io import printResult

def _clean_data(data):
    lines = [l.strip() for l in data.split("\n")]
    i, result = 0, []
    while i < len(lines):
        if lines[i][-2: ] == " _":
            temp = ""
            while lines[i][-2: ] == " _":
                temp, i = temp + lines[i][:-1], i + 1
            temp, i = temp + lines[i], i + 1
            result.append( temp )
        elif "Attribute" == lines[i][:9]:
            i += 1
        else:
            result.append( lines[i] )
            i += 1

    return "\n".join(result)

def CodeDiffDetect(src, rev):
    diff = 0
    total = len(rev.strip().split("\n")) + len(src.strip().split("\n"))
    with open("rev", "w") as outfile:
        outfile.write(_clean_data(rev))
    with open("src", "w") as outfile:
        outfile.write(_clean_data(src))
        # outfile.write(src)
    try:
        cmd = "diff -wbiBE rev src | wc -l"
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = ps.communicate()[0].decode("utf-8")
        output = int(output.strip())
        diff = output / total
    except:
        print("Fail to compare source code and reversed code in ", k)
    # os.remove("rev")
    # os.remove("src")

    result = {"Difference Rate between Source and Pcode": (diff, 0.5)}
    printResult("P-Code Stomping", result)
