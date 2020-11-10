import os
from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML

save_folder = "macros_parsed/"

# CFB file (e.g., xls, doc, etc.)
filename = "./2020/MS_Excel_Spreadsheet/eae500b4e0e912f2668350952da3f2a5717a3ec2b5ee01376ada29613d1bd1d5"
filedata = open(filename, "rb").read()
vbaparser = VBA_Parser(filename, data=filedata)

for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
    basename = os.path.basename(filename)
    target = os.path.join(save_folder, f"{basename}_{vba_filename}.txt")
    with open(target, "w") as outfile:
        outfile.write(f"Filename     : {filename}\n")
        outfile.write(f"OLE stream   : {stream_path}\n")
        outfile.write(f"VBA filename : {vba_filename}\n")
        outfile.write(f"{'-' * 40}\n")
        outfile.write(vba_code)

