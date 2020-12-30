# VBA Deobfuscator

## Dataset

`macros`: macros extracted from VirusTotal Academic Malware Samples (a sample may contain multiple VBA modules, using the IoC to identify them).
```
Filename     : {filename}
OLE stream   : {olestream}
VBA filename : {vba_filename}
----------------------------------------
{VBA code}
```


## TokenRenaming

Test single File

```lang=python
$ python3 tokenrename.py -t -f <filepath to macro>
```

API

```lang=python
import tokenrename
ret = tokenrename.CalculateSingleEntropy(filepath)
tokenrename.PrintResult(ret)
```

Visualization result

[google sheet](https://docs.google.com/spreadsheets/d/13Yoe1ezfDdvCyhC-0342HzPq7k2BnGPYY69FxuB6mps/edit?usp=sharing)
