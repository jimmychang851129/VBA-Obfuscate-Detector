# VBA obfuscation Dectector

![](https://github.com/jimmychang851129/VBA-Deobfuscator/blob/main/image/logo.png?raw=true)

SYJDetector is the final project in the Malware Malware Reverse Engineering and Analysis, National Taiwan University.

SYJ Detector aims to detect the vba obfuscation techniques used in microsoft CFB files.

Slides for further details: [link](https://www.csie.ntu.edu.tw/~r08922004/webpage/syjobfuscator.pdf)

This project is developed by [tpainting](https://github.com/tpainting), [yuyuanhey](https://github.com/yuyuanhey), and [jimmy](https://github.com/jimmychang851129)

## Installation

```
$ pip3 install -r requirements.txt
$ python3 main.py
```

## Dataset

The Dataset is a credit to VirusTotal.
:warning: PLEASE BE CAREFUL AS THEY ARE MALWARE SAMPLES.

[Dataset (Dropbox) ](https://www.dropbox.com/s/papk5xt0shalsv0/macros.tar.gz?dl=0)

`macros`: macros extracted from VirusTotal Academic Malware Samples (a sample may contain multiple VBA modules, using the IoC to identify them).
```
Filename     : {filename}
OLE stream   : {olestream}
VBA filename : {vba_filename}
----------------------------------------
{VBA code}
```

## Methodology

### Common VBA obfuscation Methods

| Methodology | Description |  Tools |
| -------- | -------- | -------- |
| vba stomping  | Replace performance cache with malicious p-code  | [EvilClippy](https://github.com/outflanknl/EvilClippy)| 
| Token renaming | function/variable name renaming |[VBad](https://github.com/Pepitoh/VBad/blob/master/VBad.py), [MacroPack](https://github.com/sevagas/macro_pack), [VBA Obfuscator](https://github.com/bonnetn/vba-obfuscator) |
|String Concat|concat command or strings to avoid detection| [VBad](https://github.com/Pepitoh/VBad/blob/master/VBad.py), [MacroPack](https://github.com/sevagas/macro_pack), [VBA Obfuscator](https://github.com/bonnetn/vba-obfuscator) |
|Control Flow Obfuscation| various of function calls and condition jump|
|identation removal | remove all the identation| [VBad](https://github.com/Pepitoh/VBad/blob/master/VBad.py), [MacroPack](https://github.com/sevagas/macro_pack), [VBA Obfuscator](https://github.com/bonnetn/vba-obfuscator) |


### Detection

#### Token-renaming obfuscation

As obfuscated function or variable names often have higher entropy than the normal function names. We calculate the entropy of the token name and identify if it the name is obfuscated or not.

#### vba stomping

We decompile the p-code and compare the Line of Difference(LoD) with the origin p-code attached in the CFB file. We will identify this obfuscation technique is used if the LoD is over a pre-determined threshold.

#### String concat obfuscation

We calculate the number of append operations and identify obfuscation if it passes the threshold

#### Control flow obfuscation

We build a directed graph for the function relation and identify the obfuscation if the maximum path passes the threshold

## Demo

![](https://github.com/jimmychang851129/VBA-Deobfuscator/blob/main/image/demo.png?raw=true)
