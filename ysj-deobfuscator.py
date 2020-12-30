import sys, os, argparse
import TokenRename.tokenrename as tkrename

def ParseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputdir",'-i', type=str, help='macros dir')
    args = parser.parse_args()
    return args

def main():
    print('''
   _______  __    __   ____  __    ____                      __          ____       __            __            
  / ___/\\ \\/ /   / /  / __ \\/ /_  / __/_  ________________ _/ /____     / __ \\___  / /____  _____/ /_____  _____
  \\__ \\  \\  /_  / /  / / / / __ \\/ /_/ / / / ___/ ___/ __ `/ __/ _ \\   / / / / _ \\/ __/ _ \\/ ___/ __/ __ \\/ ___/
 ___/ /  / / /_/ /  / /_/ / /_/ / __/ /_/ (__  ) /__/ /_/ / /_/  __/  / /_/ /  __/ /_/  __/ /__/ /_/ /_/ / /    
/____/  /_/\\____/   \\____/_.___/_/  \\__,_/____/\\___/\\__,_/\\__/\\___/  /_____/\\___/\\__/\\___/\\___/\\__/\\____/_/     
                                                                                                                 
    VBA Obfuscation Detection Tools
    By @Yvonne, @Shupo, @Jimmy
    ''')


if __name__ == '__main__':
    args = ParseArg()
    main(args)


