import os
import shutil
# copy file
# srcfile: file to be copied  
# dstpath: output directory
def copyfile(srcfile, dstpath, copyfilename=""):  
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  
        if copyfilename != "":
            fname = copyfilename
        shutil.copy(srcfile, dstpath + fname)  
        print("copy %s -> %s"%(srcfile, dstpath + fname))
    return

# import os
# delete all files under path
def delpathfiles(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        print(root) # absolute path of root
        print(dirs) # folder list below root, presented as ['dir1', 'dir2']
        print(files)  # file list below root, presented as ['file1', 'file2']
        # delete file
        for name in files:
            os.remove(os.path.join(root, name))
        # delete directories
        for name in dirs:
            os.rmdir(os.path.join(root, name))

import json
import math
def readjson(filename):
    with open(filename, "r", encoding="utf-8") as f:
        ConfigInfo = json.load(f)
    MultWidth = ConfigInfo["width"]
    for i in range(2):
        MultWidth[i] = 2 * math.ceil(MultWidth[i]/2)
    if MultWidth[0] > MultWidth[1]:
        MultWidth[0], MultWidth[1] = MultWidth[1], MultWidth[0]
    signed = ConfigInfo["signed"][0]
    useapp = ConfigInfo["app"][0]
    AppBits = ConfigInfo["appbits"][0]
    AppBits = min(AppBits, MultWidth[0] + MultWidth[1] - 4)
    AppType = ConfigInfo["apptype"]
    if useapp == 1 and signed == 0:
        AppType = ConfigInfo["apptype"][:1]
    else:
        AppType = ConfigInfo["apptype"][:2]
    type = ConfigInfo["type"]
    combinatory = ConfigInfo["combinatory"][0]
    return MultWidth, signed, useapp, AppBits, AppType, type, combinatory


import re
def gen_CC4_inst(CC4_inst_initialinfo, MultWidth_f):
    CC4_instantiation = ""
    c_tmp_definition = ""
    S_D_assignment = ""
    for i in range(0, MultWidth_f + 2, 4):
        CC4_inst_info = re.sub("(<#width1>)", str(int(i/4)), CC4_inst_initialinfo)
        CC4_inst_info = re.sub("(<#width2>)", str(i), CC4_inst_info)
        CC4_inst_info = re.sub("(<#width3>)", str(i+1), CC4_inst_info)
        CC4_inst_info = re.sub("(<#width4>)", str(i+2), CC4_inst_info)
        CC4_inst_info = re.sub("(<#width5>)", str(i+3), CC4_inst_info)
        if i+3 > MultWidth_f + 1:
            CC4_inst_info = re.sub("(<#width6>)", str(MultWidth_f + 1), CC4_inst_info)
        else:
            CC4_inst_info = re.sub("(<#width6>)", str(i+3), CC4_inst_info)
        CC4_inst_info = re.sub("(<#width7>)", str(i+4), CC4_inst_info)
        CC4_instantiation += CC4_inst_info    
        c_tmp_definition += f"wire c_tmp_{i};\n\t"
    for i in range(MultWidth_f + 1, int(4*math.ceil((MultWidth_f+1)/4))):
        S_D_assignment += f"assign S[{i}] = 1'b0;\n\t"
        S_D_assignment += f"assign D[{i}] = 1'b0;\n\t"
    c_tmp_definition += f"wire c_tmp_{ int(4 * math.ceil((MultWidth_f+2)/4)) };\n\t"
    return CC4_instantiation, c_tmp_definition, S_D_assignment





