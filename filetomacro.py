import os

def CombineMacrosToFile(inputdir,outputdir):
    fileList = dict()
    for vba in os.listdir(inputdir):
        try:
            with open(os.path.join(inputdir,vba),'r') as f:
                line = f.readline().split(":")[-1].strip()
                tmp = f.readlines()
                tmp = [x.strip() for x in tmp[3:]]
                if line not in fileList:
                    fileList[line] = []
                    fileList[line].append(tmp)
                else:
                    fileList[line].append(tmp)
        except Exception as e:
            print(str(e))
            print("vba = ",vba)
    for key in fileList.keys():
        filename = key.split('/')[-1]
        with open(os.path.join(outputdir,filename),'w') as fw:
            for ele in fileList[key]:
                for d in ele:
                    fw.write(d+"\n")
                fw.write("\n\n")

def ParseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir",'-i', type=str, help='macros dir ex: VBA_Deobfuscator/macros/')
    parser.add_argument("--outputdir",'-o', type=str, help='outputdir')
    args = parser.parse_args()
    return args

def main(args):
    CombineMacrosToFile(args.inputdir,args.outputdir)

if __name__ == '__main__':
    args = ParseArg()
    main(args)
