import os
import numpy as np
import random

from utils import *
from appLayer import *
from dadda import *


# ########################## Optional approximation multiplier underlying modules and instantiation contents ##############################
appLut_path_dict = {
    "LUT_a": [
        "../lut_src/LUT_a_app1.v",
        "../lut_src/LUT_a_app2.v",
        "../lut_src/LUT_a_app3.v"
    ],
    "LUT_b": [
        "../lut_src/LUT_b_app1.v",
        "../lut_src/LUT_b_app2.v"
    ],
    "LUT_c": [
        "../lut_src/LUT_c_app1.v",
        "../lut_src/LUT_c_app2.v",
        "../lut_src/LUT_c_app3.v"
    ],
    "LUT_d": [
        "../lut_src/LUT_d_app1.v",
        "../lut_src/LUT_d_app2.v"
    ],
    "LUT_e": []
}

appLut_inst_path_dict = {
    "LUT_a": [
        "../inst_src/lut/LUT_a_app1_inst.v",
        "../inst_src/lut/LUT_a_app2_inst.v",
        "../inst_src/lut/LUT_a_app3_inst.v"
    ],
    "LUT_b": [
        "../inst_src/lut/LUT_b_app1_inst.v",
        "../inst_src/lut/LUT_b_app2_inst.v"
    ],
    "LUT_c": [
        "../inst_src/lut/LUT_c_app1_inst.v",
        "../inst_src/lut/LUT_c_app2_inst.v",
        "../inst_src/lut/LUT_c_app3_inst.v"
    ],
    "LUT_c_type2": [
        "../inst_src/lut/LUT_c_app1_inst.v",
        "../inst_src/lut/LUT_c_app2_inst.v",
        "../inst_src/lut/LUT_c_app3_inst.v"
    ],
    "LUT_d": [
        "../inst_src/lut/LUT_d_app1_inst.v",
        "../inst_src/lut/LUT_d_app2_inst.v"
    ],
    "LUT_e": []
}

# ######################################################## end #######################################################


class Multiplier:
    def __init__(self, MultWidth, signed, useapp, AppBits, AppType, type, combinatory):
        # basic info
        self.MultWidth_f = MultWidth[0]
        self.MultWidth_b = MultWidth[1]
        self.signed = signed
        self.useapp = useapp
        self.AppBits = AppBits
        self.AppType = AppType
        self.type = type
        self.combinatory = combinatory
        # config info for approximation: app layers, allapp layers, otherapp layers, noapp layers; config info of each app layer
        # app layers include allapp, otherapp and noapp 3 types
        # allapp layers refer to such layers that all modules inside have been introduced with approximate logic
        # otherapp layers refer to such layers that not all modules inside have been introduced with approximate logic
        # noapp layers refer to such layers that no modules inside have been introduced with approximate logic
        self.AppAttributes = gen_appAttributes(self.MultWidth_f, self.MultWidth_b, self.useapp, self.AppBits)
        self.appLayer_configInfo_list = []
        # Dadda Tree config info
        self.Dadda_configInfo_list = []
        self.Dadda_max_rownums = 0  # the max row number among all column of Dadda Tree
        # basic modules
        self.accLut_path_list = []
        self.appLut_path_list = []
        self.adderFile_path = ""
        # layer modules
        self.layer_mod_path_list = []  # template files for layer modules
        self.accLut_inst_path_list = ""  # accurate modules' instantiation content files for layer modules
        self.appLut_inst_path_list = ""  # approximate modules' instantiation content files for layer modules
        self.layer_num = 0
        # top modules
        self.mult_mod_path = ""  # template files for top modules
        self.layer_inst_path_list = ""  # layer modules' instantiation content files for layer modules
        # output directory and output files
        self.output_directory = "../output/src/"
        self.layer_output_filename_list = []
        self.mult_output_path = ""
        # adder width
        self.CLAadderWidth = 72  # default adder width is 72
        # tb file
        self.tb_path  = ""





    # ################################################# copy_underlyingFiles #################################################
    # copy needed basic module files to output path
    def copy_underlyingFiles(self):
        if (self.useapp == 0) and (self.signed == 0):
            self.accLut_path_list = [
                "../lut_src/LUT_a.v",
                "../lut_src/LUT_b.v"
                # CC4\FA\HA are included in adder_src
            ]
        elif (self.useapp == 0) and (self.signed == 1):
            self.accLut_path_list = [
                "../lut_src/LUT_a.v",
                "../lut_src/LUT_b.v",
                "../lut_src/LUT_c.v",
                "../lut_src/LUT_d.v",
                "../lut_src/LUT_e.v"
            ]
        elif (self.useapp == 1) and (self.signed == 0):
            self.accLut_path_list = [
                "../lut_src/LUT_a.v",
                "../lut_src/LUT_b.v"
            ]
            # ############################## self-selection ##################################
            self.appLut_path_list.append(appLut_path_dict["LUT_a"][self.AppType[0]])
            self.appLut_path_list.append(appLut_path_dict["LUT_b"][0])
            # self.appLut_path_list.append(appLut_path_dict["LUT_b"][1])
            # #################################### end #######################################
        elif (self.useapp == 1) and (self.signed == 1):
            self.accLut_path_list = [
                "../lut_src/LUT_a.v",
                "../lut_src/LUT_b.v",
                "../lut_src/LUT_c.v",
                "../lut_src/LUT_d.v",
                "../lut_src/LUT_e.v"
            ]
            # ############################### self-selection ###################################
            self.appLut_path_list.append(appLut_path_dict["LUT_a"][self.AppType[0]])
            self.appLut_path_list.append(appLut_path_dict["LUT_c"][self.AppType[1]])
            self.appLut_path_list.append(appLut_path_dict["LUT_d"][0])
            # self.appLut_path_list.append(appLut_path_dict["LUT_d"][1])
            # ##################################### end ########################################
        if not os.path.exists(self.output_directory):
            os.mkdir(self.output_directory)
        delpathfiles(self.output_directory)
        for lut_path in self.accLut_path_list:
            copyfile(lut_path, self.output_directory)
        for lut_path in self.appLut_path_list:
            copyfile(lut_path, self.output_directory)
        return
    # ###################################################### end #######################################################








    # ################################################# gen_layerFiles #################################################
    # write codes into layer module files
    '''
    steps:
    1. get approximation config info
    2. get instantiation contents of basic modules
    3. generate all layer module files
    4. write codes into layer module files
        4-1 <unsigned accurate multipliers>
            4-1-1 get instantiation contents of LUT modules
            4-1-2 get instantiation contents of CC modules
            4-1-3 get template of layer modules, and substitute identifiers for LUT & CC instantion contents
        4-2 <signed accurate multipliers> {common layers, last layer}
            4-2-1 for common layers, get instantiation contents of LUT modules
            4-2-2 for common layers, get instantiation contents of CC modules
            4-2-3 get template of common layer modules, and substitute identifiers for LUT & CC instantion contents
            4-2-4 for last layer, get instantiation contents of LUT modules
            4-2-5 for last layer, get instantiation contents of CC modules
            4-2-6 get template of last layer module, and substitute identifiers for LUT & CC instantion contents                
        4-3 <unsigned approximate multipliers> {allapp layers, otherapp layers, noapp layers}
            first get template of layer modules
            4-3-1 for allapp layers, get instantiation contents of LUT modules
            4-3-2 for allapp layers, get instantiation contents of CC modules
            4-3-3 substitute identifiers in template contents for LUT & CC instantion contents
            4-3-4 for noapp layers, get instantiation contents of LUT modules
            4-3-5 for noapp layers, get instantiation contents of CC modules
            4-3-6 substitute identifiers in template contents for LUT & CC instantion contents
            4-3-7 for otherapp layers, get instantiation contents of LUT modules within for-loops
            4-3-8 for otherapp layers, get instantiation contents of CC modules within for-loops
            4-3-9 substitute identifiers in template contents for LUT & CC instantion contents within for-loops
        4-4 <signed approximate multipliers> {allapp layers, otherapp layers, noapp layers} {common layers, last layer}
            first get template of common layer modules
            4-4-1 for allapp layers, get instantiation contents of LUT modules
            4-4-2 for allapp layers, get instantiation contents of CC modules
            4-4-3 substitute identifiers in template contents for LUT & CC instantion contents
            4-4-4 for noapp layers, get instantiation contents of LUT modules
            4-4-5 for noapp layers, get instantiation contents of CC modules
            4-4-6 substitute identifiers in template contents for LUT & CC instantion contents
            then get template of last layer modules
            4-4-7 for last layer, get instantiation contents of LUT modules
            4-4-8 for last layers, get instantiation contents of CC modules
            4-4-9 substitute identifiers in template contents for LUT & CC instantion contents
            4-4-10 for otherapp layers, get instantiation contents of LUT modules within for-loops
            4-4-11 for otherapp layers, get instantiation contents of CC modules within for-loops
            4-4-12 substitute identifiers in template contents for LUT & CC instantion contents within for-loops
    '''
    def gen_layerFiles(self):
        if (self.useapp == 0) and (self.signed == 0):

            # 1. get approximation config info
            # 2. get instantiation contents of basic modules
            self.accLut_inst_path_list = [
                "../inst_src/lut/LUT_a_inst.v",
                "../inst_src/lut/LUT_b_inst.v",
                "../inst_src/lut/CC4_inst.v"          
            ]
            f_input_list = []
            for lut_inst_path in self.accLut_inst_path_list:
                f_input_list.append( open(lut_inst_path, "r", encoding="utf-8") )
            LUT_a_inst_initialinfo = f_input_list[0].read()
            LUT_b_inst_initialinfo = f_input_list[1].read()
            CC4_inst_initialinfo = f_input_list[2].read()

            # 3. generate all layer module files
            self.layer_mod_path_list = [
                "../mod_src/layer/00/acc_layer_unsigned_mod.v"
            ]
            self.layer_output_filename_list = ["acc_layer_unsigned" + str(self.MultWidth_f) + "x2.v"]
            for filename in self.layer_output_filename_list:
                copyfile(self.layer_mod_path_list[0], self.output_directory, filename)

            # 4. write codes into layer module files
            # 4-1-1 get instantiation contents of LUT modules
            LUT_instantiation = ""
            for i in range(self.MultWidth_f - 1):
                LUT_a_inst_info = re.sub("(<#width1>)", str(i), LUT_a_inst_initialinfo)
                LUT_a_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_a_inst_info)
                LUT_instantiation += LUT_a_inst_info
            LUT_b_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_b_inst_initialinfo)
            LUT_b_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_b_inst_info)
            LUT_instantiation += LUT_b_inst_info

            # 4-1-2 get instantiation contents of CC modules
            CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

            # 4-1-3 get template of layer modules, and substitute identifiers for LUT & CC instantion contents
            self.layer_mod_path_list.append("../mod_src/layer/00/acc_layer_unsigned_mod.v")
            mod_initialinfo = ""
            with open(self.layer_mod_path_list[0], "r", encoding="utf-8") as f:
                mod_initialinfo = f.read()
            mod_initialinfo = re.sub("(<#width1>)", str(self.MultWidth_f), mod_initialinfo)
            mod_initialinfo = re.sub("(<#width2>)", str(self.MultWidth_f + 1), mod_initialinfo)
            mod_initialinfo = re.sub("(<#width4>)", str( int(4*math.ceil((self.MultWidth_f+1)/4))-1 ), mod_initialinfo)
            mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_initialinfo)
            mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
            mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
            mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
            with open(self.output_directory + self.layer_output_filename_list[0], "w", encoding="utf-8") as f:
                f.write(mod_info)
            for i in range( len(f_input_list) ):
                f_input_list[i].close()
            



        elif (self.useapp == 0) and (self.signed == 1):

            # 1. get approximation config info
            # 2. get instantiation contents of basic modules
            self.accLut_inst_path_list = [
                "../inst_src/lut/LUT_a_inst.v",
                "../inst_src/lut/LUT_b_inst.v",
                "../inst_src/lut/LUT_c_inst.v",
                "../inst_src/lut/LUT_c_inst_type2.v",
                "../inst_src/lut/LUT_d_inst.v",
                "../inst_src/lut/LUT_e_inst.v",
                "../inst_src/lut/CC4_inst.v"
            ]
            f_input_list = []
            for lut_inst_path in self.accLut_inst_path_list:
                f_input_list.append( open(lut_inst_path, "r", encoding="utf-8") )
            LUT_a_inst_initialinfo = f_input_list[0].read()
            LUT_b_inst_initialinfo = f_input_list[1].read()
            LUT_c_inst_initialinfo = f_input_list[2].read()
            LUT_c_inst_initialinfo_type2 = f_input_list[3].read()  # attention: LUT_c usages in common layers and last layer are different
            LUT_d_inst_initialinfo = f_input_list[4].read()
            LUT_e_inst_initialinfo = f_input_list[5].read()
            CC4_inst_initialinfo = f_input_list[6].read()

            # 3. generate all layer module files
            self.layer_mod_path_list = [
                "../mod_src/layer/01/acc_layer_signed_common_mod.v",
                "../mod_src/layer/01/acc_layer_signed_last_mod.v"
            ]
            self.layer_output_filename_list = [
                "acc_layer_signed" + str(self.MultWidth_f) + "x2_common.v",
                "acc_layer_signed" + str(self.MultWidth_f) + "x2_last.v"
            ]
            for i in range( len(self.layer_output_filename_list) ):
                filename = self.layer_output_filename_list[i]
                copyfile(self.layer_mod_path_list[i], self.output_directory, filename)

            # 4. write codes into layer module files
            # 4-2-1 for common layers, get instantiation contents of LUT modules
            LUT_instantiation = ""
            for i in range(self.MultWidth_f - 2):
                LUT_a_inst_info = re.sub("(<#width1>)", str(i), LUT_a_inst_initialinfo)
                LUT_a_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_a_inst_info)
                LUT_instantiation += LUT_a_inst_info
            LUT_c_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_c_inst_initialinfo_type2)
            LUT_c_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_c_inst_info)
            LUT_instantiation += LUT_c_inst_info
            LUT_d_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_d_inst_initialinfo)
            LUT_d_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_d_inst_info)
            LUT_instantiation += LUT_d_inst_info
            
            # 4-2-2 for common layers, get instantiation contents of CC modules
            CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

            # 4-2-3 get template of common layer modules, and substitute identifiers for LUT & CC instantion contents
            mod_initialinfo = ""
            with open(self.layer_mod_path_list[0], "r", encoding="utf-8") as f:
                mod_initialinfo = f.read()
            mod_initialinfo = re.sub("(<#width1>)", str(self.MultWidth_f), mod_initialinfo)
            mod_initialinfo = re.sub("(<#width2>)", str(self.MultWidth_f + 1), mod_initialinfo)
            mod_initialinfo = re.sub("(<#width4>)", str( int(4*math.ceil((self.MultWidth_f+1)/4))-1 ), mod_initialinfo)
            mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_initialinfo)
            mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
            mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
            mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
            with open(self.output_directory + self.layer_output_filename_list[0], "w", encoding="utf-8") as f:
                f.write(mod_info)

            # 4-2-4 for last layer, get instantiation contents of LUT modules
            LUT_instantiation = ""
            for i in range(self.MultWidth_f - 2):
                LUT_c_inst_info = re.sub("(<#width1>)", str(i), LUT_c_inst_initialinfo)
                LUT_c_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_c_inst_info)
                LUT_instantiation += LUT_c_inst_info
            LUT_e_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_e_inst_initialinfo)
            LUT_e_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_e_inst_info)
            LUT_instantiation += LUT_e_inst_info
            LUT_b_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_b_inst_initialinfo)
            LUT_b_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_b_inst_info)
            LUT_instantiation += LUT_b_inst_info

            # 4-2-5 for last layer, get instantiation contents of CC modules
            CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

            # 4-2-6 get template of last layer module, and substitute identifiers for LUT & CC instantion contents  
            mod_initialinfo = ""
            with open(self.layer_mod_path_list[1], "r", encoding="utf-8") as f:
                mod_initialinfo = f.read()
            mod_initialinfo = re.sub("(<#width1>)", str(self.MultWidth_f), mod_initialinfo)
            mod_initialinfo = re.sub("(<#width2>)", str(self.MultWidth_f + 1), mod_initialinfo)
            mod_initialinfo = re.sub("(<#width4>)", str( int(4*math.ceil((self.MultWidth_f+1)/4))-1 ), mod_initialinfo)
            mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_initialinfo)
            mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
            mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
            mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
            with open(self.output_directory + self.layer_output_filename_list[1], "w", encoding="utf-8") as f:
                f.write(mod_info)





        elif (self.useapp == 1) and (self.signed == 0):

            # 1. get approximation config info
            self.appLayer_configInfo_list = gen_appunsignedLayer_configInfo(self.MultWidth_f, self.AppBits, self.AppAttributes)            

            # 2. get instantiation contents of basic modules
            self.accLut_inst_path_list = [
                "../inst_src/lut/LUT_a_inst.v",
                "../inst_src/lut/LUT_b_inst.v",
                "../inst_src/lut/CC4_inst.v"             
            ]
            # ################################## self-selection #####################################
            self.appLut_inst_path_list = []
            self.appLut_inst_path_list.append(appLut_inst_path_dict["LUT_a"][self.AppType[0]])
            self.appLut_inst_path_list.append(appLut_inst_path_dict["LUT_b"][0])
            # self.appLut_inst_path_list.append(appLut_inst_path_dict["LUT_b"][1])
            # ######################################## end ###############################################
            f_input_list = []
            for lut_inst_path in self.accLut_inst_path_list + self.appLut_inst_path_list:
                f_input_list.append( open(lut_inst_path, "r", encoding="utf-8") )
            LUT_a_inst_initialinfo = f_input_list[0].read()
            LUT_b_inst_initialinfo = f_input_list[1].read()
            CC4_inst_initialinfo = f_input_list[2].read()
            LUT_a_app_inst_initialinfo = f_input_list[-2].read()
            LUT_b_app_inst_initialinfo = f_input_list[-1].read()

            # 3. generate all layer module files
            self.layer_mod_path_list = [
                "../mod_src/layer/10/app_layer_unsigned_mod.v"
            ]
            self.layer_output_filename_list = []
            if self.AppAttributes[1] != 0:  # num_allapp
                self.layer_output_filename_list.append( "app_layer_unsigned" + str(self.MultWidth_f) + "x2_0.v" )
                for i in range(self.AppAttributes[2]):  # num_otherapp
                    self.layer_output_filename_list.append( "app_layer_unsigned" + str(self.MultWidth_f) + "x2_" + str(i+1) + ".v" )
            else:
                for i in range(self.AppAttributes[2]):  # num_otherapp
                    self.layer_output_filename_list.append( "app_layer_unsigned" + str(self.MultWidth_f) + "x2_" + str(i) + ".v" )
            if self.AppAttributes[3] != 0:  # num_noapp
                self.layer_output_filename_list.append( "app_layer_unsigned" + str(self.MultWidth_f) + "x2_" + str(len(self.layer_output_filename_list)) + ".v" )
            for filename in self.layer_output_filename_list:
                copyfile(self.layer_mod_path_list[0], self.output_directory, filename)    
            self.layer_num = len(self.layer_output_filename_list)       
            
            # 4. write codes into layer module files
            # first get template of layer modules
            mod_initialinfo = ""
            with open(self.layer_mod_path_list[0], "r", encoding="utf-8") as f:
                mod_initialinfo = f.read()
            mod_initialinfo = re.sub("(<#width1>)", str(self.MultWidth_f), mod_initialinfo)
            mod_initialinfo = re.sub("(<#width2>)", str(self.MultWidth_f + 1), mod_initialinfo)
            mod_initialinfo = re.sub("(<#width4>)", str( int(4*math.ceil((self.MultWidth_f+1)/4))-1 ), mod_initialinfo)
            if self.AppAttributes[1] != 0:
                # 4-3-1 for allapp layers, get instantiation contents of LUT modules
                LUT_instantiation = ""
                for i in range(self.MultWidth_f - 1):
                    LUT_a_app_inst_info = re.sub("(<#width1>)", str(i), LUT_a_app_inst_initialinfo)
                    LUT_a_app_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_a_app_inst_info)
                    LUT_instantiation += LUT_a_app_inst_info
                LUT_b_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_b_app_inst_initialinfo)
                LUT_b_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_b_app_inst_info)
                LUT_instantiation += LUT_b_app_inst_info
            
                # 4-3-2 for allapp layers, get instantiation contents of CC modules
                CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)
            
                # 4-3-3 substitute identifiers in template contents for LUT & CC instantion contents
                mod_info = re.sub("(<#width3>)", str(0), mod_initialinfo)
                mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_info)
                mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
                mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
                mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
                with open(self.output_directory + self.layer_output_filename_list[0], "w", encoding="utf-8") as f:
                    f.write(mod_info)

            if self.AppAttributes[3] != 0:
                # 4-3-4 for noapp layers, get instantiation contents of LUT modules
                LUT_instantiation = ""
                for i in range(self.MultWidth_f - 1):
                    LUT_a_inst_info = re.sub("(<#width1>)", str(i), LUT_a_inst_initialinfo)
                    LUT_a_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_a_inst_info)
                    LUT_instantiation += LUT_a_inst_info
                LUT_b_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_b_inst_initialinfo)
                LUT_b_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_b_inst_info)
                LUT_instantiation += LUT_b_inst_info
            
                # 4-3-5 for noapp layers, get instantiation contents of CC modules
                CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

                # 4-3-6 substitute identifiers in template contents for LUT & CC instantion contents
                if self.AppAttributes[1] != 0:
                    mod_info = re.sub("(<#width3>)", str(self.AppAttributes[2]+1), mod_initialinfo)
                else:
                    mod_info = re.sub("(<#width3>)", str(self.AppAttributes[2]), mod_initialinfo)
                mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_info)
                mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
                mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
                mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
                with open(self.output_directory + self.layer_output_filename_list[-1], "w", encoding="utf-8") as f:
                    f.write(mod_info)                

            # if-elif-else judgments in for-loops can be optimized
            for num in range(self.AppAttributes[2]):
                # 4-3-7 for otherapp layers, get instantiation contents of LUT modules within for-loops
                LUT_instantiation = ""
                num_LUT_a_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_a_app"]
                num_LUT_a = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_a"]
                num_LUT_b_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["ifLUT_b_app"]

                for i in range(num_LUT_a_app):
                    LUT_a_app_inst_info = re.sub("(<#width1>)", str(i), LUT_a_app_inst_initialinfo)
                    LUT_a_app_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_a_app_inst_info)
                    LUT_instantiation += LUT_a_app_inst_info
                for i in range(num_LUT_a):
                    LUT_a_inst_info = re.sub("(<#width1>)", str(num_LUT_a_app + i), LUT_a_inst_initialinfo)
                    LUT_a_inst_info = re.sub("(<#width2>)", str(num_LUT_a_app + i + 1), LUT_a_inst_info)
                    LUT_instantiation += LUT_a_inst_info
                if num_LUT_b_app == 1:
                    LUT_b_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_b_app_inst_initialinfo)
                    LUT_b_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_b_app_inst_info)
                    LUT_instantiation += LUT_b_app_inst_info
                else:
                    LUT_b_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_b_inst_initialinfo)
                    LUT_b_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_b_inst_info)
                    LUT_instantiation += LUT_b_inst_info
            
                # 4-3-8 for otherapp layers, get instantiation contents of CC modules within for-loops
                CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

                # 4-3-9 substitute identifiers in template contents for LUT & CC instantion contents within for-loops
                if self.AppAttributes[1] != 0:
                    mod_info = re.sub("(<#width3>)", str(num+1), mod_initialinfo)
                else:
                    mod_info = re.sub("(<#width3>)", str(num), mod_initialinfo)
                mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_info)
                mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
                mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
                mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)

                if self.AppAttributes[1] != 0:
                    with open(self.output_directory + self.layer_output_filename_list[num+1], "w", encoding="utf-8") as f:
                        f.write(mod_info)
                else:
                    with open(self.output_directory + self.layer_output_filename_list[num], "w", encoding="utf-8") as f:
                        f.write(mod_info)
            
            
            



        elif (self.useapp == 1) and (self.signed == 1):
            # 1. get approximation config info
            self.appLayer_configInfo_list = gen_appsignedLayer_configInfo(self.MultWidth_f, self.AppBits, self.AppAttributes)
            # 2. get instantiation contents of basic modules
            self.accLut_inst_path_list = [
                "../inst_src/lut/LUT_a_inst.v",
                "../inst_src/lut/LUT_b_inst.v",
                "../inst_src/lut/LUT_c_inst.v",
                "../inst_src/lut/LUT_c_inst_type2.v",
                "../inst_src/lut/LUT_d_inst.v",
                "../inst_src/lut/LUT_e_inst.v",
                "../inst_src/lut/CC4_inst.v"
            ]
            # ################################## self-selection #####################################
            self.appLut_inst_path_list = []
            self.appLut_inst_path_list.append(appLut_inst_path_dict["LUT_a"][self.AppType[0]])
            self.appLut_inst_path_list.append(appLut_inst_path_dict["LUT_c"][self.AppType[1]])
            self.appLut_inst_path_list.append(appLut_inst_path_dict["LUT_c_type2"][self.AppType[1]])
            self.appLut_inst_path_list.append(appLut_inst_path_dict["LUT_d"][0])
            # self.appLut_inst_path_list.append(appLut_inst_path_dict["LUT_d"][1])
            # ######################################## end ###############################################
            f_input_list = []
            for lut_inst_path in self.accLut_inst_path_list:
                f_input_list.append( open(lut_inst_path, "r", encoding="utf-8") )
            for lut_inst_path in self.appLut_inst_path_list:
                f_input_list.append( open(lut_inst_path, "r", encoding="utf-8") )
            LUT_a_inst_initialinfo = f_input_list[0].read()
            LUT_b_inst_initialinfo = f_input_list[1].read()
            LUT_c_inst_initialinfo = f_input_list[2].read()
            LUT_c_inst_initialinfo_type2 = f_input_list[3].read()  # attention: LUT_c usages in common layers and last layer are different
            LUT_d_inst_initialinfo = f_input_list[4].read()
            LUT_e_inst_initialinfo = f_input_list[5].read()
            CC4_inst_initialinfo = f_input_list[6].read()
            LUT_a_app_inst_initialinfo = f_input_list[-4].read()
            LUT_c_app_inst_initialinfo = f_input_list[-3].read()
            LUT_c_app_inst_initialinfo_type2 = f_input_list[-2].read()
            LUT_d_app_inst_initialinfo = f_input_list[-1].read()

            # 3. generate all layer module files
            self.layer_mod_path_list = [
                "../mod_src/layer/11/app_layer_signed_common_mod.v",
                "../mod_src/layer/11/app_layer_signed_last_mod.v"
            ]
            self.layer_output_filename_list = []
            if self.AppAttributes[1] != 0:
                self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_common_0.v" )
                if self.AppAttributes[0] == int( self.MultWidth_b/2 ):  # indicate that last layer is also an approximate modules and here is no noapp modules
                    for i in range(self.AppAttributes[2]-1):
                        self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_common_" + str(i+1) + ".v" )
                    self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_last.v" )
                else:
                    for i in range(self.AppAttributes[2]):
                        self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_common_" + str(i+1) + ".v" )
                    if self.AppAttributes[3] > 1:
                        self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_common_" + str(self.AppAttributes[2]+1) + ".v" )
                    self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_last.v" )
            else:
                if self.AppAttributes[0] == int( self.MultWidth_b/2 ):  # indicate that last layer is also an approximate modules and here is no noapp modules
                    for i in range(self.AppAttributes[2]-1):
                        self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_common_" + str(i) + ".v" )
                    self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_last.v" )
                else:
                    for i in range(self.AppAttributes[2]):
                        self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_common_" + str(i) + ".v" )
                    if self.AppAttributes[3] > 1:
                        self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_common_" + str(self.AppAttributes[2]) + ".v" )
                    self.layer_output_filename_list.append( "app_layer_signed" + str(self.MultWidth_f) + "x2_last.v" )
            for filename in self.layer_output_filename_list[:-1]:
                copyfile(self.layer_mod_path_list[0], self.output_directory, filename)      
            copyfile(self.layer_mod_path_list[1], self.output_directory, self.layer_output_filename_list[-1])
            
            # 4. write codes into layer module files
            # first get template of common layer modules
            mod_initialinfo_common = ""
            with open(self.layer_mod_path_list[0], "r", encoding="utf-8") as f:
                mod_initialinfo_common = f.read()
            mod_initialinfo_common = re.sub("(<#width1>)", str(self.MultWidth_f), mod_initialinfo_common)
            mod_initialinfo_common = re.sub("(<#width2>)", str(self.MultWidth_f + 1), mod_initialinfo_common)
            mod_initialinfo_common = re.sub("(<#width4>)", str( int(4*math.ceil((self.MultWidth_f+1)/4))-1 ), mod_initialinfo_common)


            if self.AppAttributes[1] != 0:
                # 4-4-1 for allapp layers, get instantiation contents of LUT modules
                LUT_instantiation = ""
                for i in range(self.MultWidth_f - 2):
                    LUT_a_app_inst_info = re.sub("(<#width1>)", str(i), LUT_a_app_inst_initialinfo)
                    LUT_a_app_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_a_app_inst_info)
                    LUT_instantiation += LUT_a_app_inst_info
                LUT_c_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_c_app_inst_initialinfo_type2)
                LUT_c_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_c_app_inst_info)
                LUT_instantiation += LUT_c_app_inst_info
                LUT_d_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_d_app_inst_initialinfo)
                LUT_d_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_d_app_inst_info)
                LUT_instantiation += LUT_d_app_inst_info

                # 4-4-2 for allapp layers, get instantiation contents of CC modules
                CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

                # 4-4-3 substitute identifiers in template contents for LUT & CC instantion contents
                mod_info = re.sub("(<#width3>)", str(0), mod_initialinfo_common)
                mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_info)
                mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
                mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
                mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
                with open(self.output_directory + self.layer_output_filename_list[0], "w", encoding="utf-8") as f:
                    f.write(mod_info)

            if self.AppAttributes[3] != 0:
                # 4-4-4 for noapp layers, get instantiation contents of LUT modules
                LUT_instantiation = ""
                for i in range(self.MultWidth_f - 2):
                    LUT_a_inst_info = re.sub("(<#width1>)", str(i), LUT_a_inst_initialinfo)
                    LUT_a_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_a_inst_info)
                    LUT_instantiation += LUT_a_inst_info
                LUT_c_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_c_inst_initialinfo_type2)
                LUT_c_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_c_inst_info)
                LUT_instantiation += LUT_c_inst_info
                LUT_d_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_d_inst_initialinfo)
                LUT_d_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_d_inst_info)
                LUT_instantiation += LUT_d_inst_info

                # 4-4-5 for noapp layers, get instantiation contents of CC modules
                CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

                # 4-4-6 substitute identifiers in template contents for LUT & CC instantion contents
                if self.AppAttributes[1] != 0:
                    mod_info = re.sub("(<#width3>)", str(self.AppAttributes[2]+1), mod_initialinfo_common)
                else:
                    mod_info = re.sub("(<#width3>)", str(self.AppAttributes[2]), mod_initialinfo_common)
                mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_info)
                mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
                mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
                mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
                with open(self.output_directory + self.layer_output_filename_list[-2], "w", encoding="utf-8") as f:  # 索引为-1的是layer_last层
                    f.write(mod_info)

            # then get template of last layer modules
            if self.AppAttributes[0] != int( self.MultWidth_b/2 ):
                # 4-4-7 for last layer, get instantiation contents of LUT modules
                LUT_instantiation = ""
                for i in range(self.MultWidth_f - 2):
                    LUT_c_inst_info = re.sub("(<#width1>)", str(i), LUT_c_inst_initialinfo)
                    LUT_c_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_c_inst_info)
                    LUT_instantiation += LUT_c_inst_info
                LUT_e_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_e_inst_initialinfo)
                LUT_e_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_e_inst_info)
                LUT_instantiation += LUT_e_inst_info
                LUT_b_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_b_inst_initialinfo)
                LUT_b_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_b_inst_info)
                LUT_instantiation += LUT_b_inst_info

                # 4-4-8 for last layers, get instantiation contents of CC modules
                CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

            else:
                # 4-4-7 for last layer, get instantiation contents of LUT modules
                LUT_instantiation = ""
                num_LUT_c_app = self.appLayer_configInfo_list[-1]["LUT_c_app"]
                num_LUT_c = self.appLayer_configInfo_list[-1]["LUT_c"]
                num_LUT_e_app = self.appLayer_configInfo_list[-1]["ifLUT_e_app"]
                num_LUT_b_app = self.appLayer_configInfo_list[-1]["ifLUT_b_app"]
                for i in range(num_LUT_c_app):
                    LUT_c_app_inst_info = re.sub("(<#width1>)", str(i), LUT_c_app_inst_initialinfo)
                    LUT_c_app_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_c_app_inst_info)
                    LUT_instantiation += LUT_c_app_inst_info
                for i in range(num_LUT_c):
                    LUT_c_inst_info = re.sub("(<#width1>)", str(num_LUT_c_app + i), LUT_c_inst_initialinfo)
                    LUT_c_inst_info = re.sub("(<#width2>)", str(num_LUT_c_app + i + 1), LUT_c_inst_info)
                    LUT_instantiation += LUT_c_inst_info
                # if num_LUT_e_app == 1:
                #     LUT_e_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_e_app_inst_initialinfo)
                #     LUT_e_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_e_app_inst_info)
                #     LUT_instantiation += LUT_c_app_inst_info
                # else:
                LUT_e_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_e_inst_initialinfo)
                LUT_e_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_e_inst_info)
                LUT_instantiation += LUT_e_inst_info
                if num_LUT_b_app == 1:
                    LUT_b_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_b_app_inst_initialinfo)
                    LUT_b_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_b_app_inst_info)
                    LUT_instantiation += LUT_b_app_inst_info
                else:
                    LUT_b_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_b_inst_initialinfo)
                    LUT_b_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_b_inst_info)
                    LUT_instantiation += LUT_b_inst_info

                # 4-4-8 for last layers, get instantiation contents of CC modules
                CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)


            # 4-4-9 substitute identifiers in template contents for LUT & CC instantion contents
            mod_initialinfo_last = ""
            with open(self.layer_mod_path_list[1], "r", encoding="utf-8") as f:
                mod_initialinfo_last = f.read()
            mod_info = re.sub("(<#width1>)", str(self.MultWidth_f), mod_initialinfo_last)
            mod_info = re.sub("(<#width2>)", str(self.MultWidth_f + 1), mod_info)
            mod_info = re.sub("(<#width4>)", str( int(4*math.ceil((self.MultWidth_f+1)/4))-1 ), mod_info)
            mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_info)
            mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
            mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
            mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
            with open(self.output_directory + self.layer_output_filename_list[-1], "w", encoding="utf-8") as f:  # file whose index valued -1 corresponds tp last layer
                f.write(mod_info)


            if self.AppAttributes[0] != int(self.MultWidth_b/2):
                for num in range(self.AppAttributes[2]):
                    # 4-4-10 for otherapp layers, get instantiation contents of LUT modules within for-loops
                    LUT_instantiation = ""
                    if self.AppAttributes[0] == int(self.MultWidth_b/2) and num == self.AppAttributes[2] - 1:
                        num_LUT_a_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_c_app"]
                        num_LUT_a = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_c"]
                        num_LUT_c_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["ifLUT_e_app"]
                        num_LUT_d_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["ifLUT_b_app"]
                    else:
                        num_LUT_a_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_a_app"]
                        num_LUT_a = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_a"]
                        num_LUT_c_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["ifLUT_c_app"]
                        num_LUT_d_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["ifLUT_d_app"]

                    for i in range(num_LUT_a_app):
                        LUT_a_app_inst_info = re.sub("(<#width1>)", str(i), LUT_a_app_inst_initialinfo)
                        LUT_a_app_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_a_app_inst_info)
                        LUT_instantiation += LUT_a_app_inst_info
                    for i in range(num_LUT_a):
                        LUT_a_inst_info = re.sub("(<#width1>)", str(num_LUT_a_app + i), LUT_a_inst_initialinfo)
                        LUT_a_inst_info = re.sub("(<#width2>)", str(num_LUT_a_app + i + 1), LUT_a_inst_info)
                        LUT_instantiation += LUT_a_inst_info
                    if num_LUT_c_app == 1:
                        LUT_c_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_c_app_inst_initialinfo_type2)
                        LUT_c_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_c_app_inst_info)
                        LUT_instantiation += LUT_c_app_inst_info
                    else:
                        LUT_c_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_c_inst_initialinfo_type2)
                        LUT_c_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_c_inst_info)
                        LUT_instantiation += LUT_c_inst_info
                    if num_LUT_d_app == 1:
                        LUT_d_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_d_app_inst_initialinfo)
                        LUT_d_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_d_app_inst_info)
                        LUT_instantiation += LUT_d_app_inst_info
                    else:
                        LUT_d_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_d_inst_initialinfo)
                        LUT_d_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_d_inst_info)
                        LUT_instantiation += LUT_d_inst_info

                    # 4-4-11 for otherapp layers, get instantiation contents of CC modules within for-loops
                    CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

                    # 4-4-12 substitute identifiers in template contents for LUT & CC instantion contents within for-loops
                    if self.AppAttributes[1] != 0:
                        mod_info = re.sub("(<#width3>)", str(num+1), mod_initialinfo_common)
                    else:
                        mod_info = re.sub("(<#width3>)", str(num), mod_initialinfo_common)  
                    mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_info)
                    mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
                    mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
                    mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
                    if self.AppAttributes[1] != 0:
                        with open(self.output_directory + self.layer_output_filename_list[num+1], "w", encoding="utf-8") as f:
                            f.write(mod_info)
                    else:
                        with open(self.output_directory + self.layer_output_filename_list[num], "w", encoding="utf-8") as f:
                            f.write(mod_info)
            else:
                for num in range(self.AppAttributes[2]-1):
                    # 4-4-10 for otherapp layers, get instantiation contents of LUT modules within for-loops
                    LUT_instantiation = ""
                    if self.AppAttributes[0] == int(self.MultWidth_b/2) and num == self.AppAttributes[2] - 1:
                        num_LUT_a_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_c_app"]
                        num_LUT_a = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_c"]
                        num_LUT_c_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["ifLUT_e_app"]
                        num_LUT_d_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["ifLUT_b_app"]
                    else:
                        num_LUT_a_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_a_app"]
                        num_LUT_a = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["LUT_a"]
                        num_LUT_c_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["ifLUT_c_app"]
                        num_LUT_d_app = self.appLayer_configInfo_list[num + self.AppAttributes[1]]["ifLUT_d_app"]

                    for i in range(num_LUT_a_app):
                        LUT_a_app_inst_info = re.sub("(<#width1>)", str(i), LUT_a_app_inst_initialinfo)
                        LUT_a_app_inst_info = re.sub("(<#width2>)", str(i + 1), LUT_a_app_inst_info)
                        LUT_instantiation += LUT_a_app_inst_info
                    for i in range(num_LUT_a):
                        LUT_a_inst_info = re.sub("(<#width1>)", str(num_LUT_a_app + i), LUT_a_inst_initialinfo)
                        LUT_a_inst_info = re.sub("(<#width2>)", str(num_LUT_a_app + i + 1), LUT_a_inst_info)
                        LUT_instantiation += LUT_a_inst_info
                    if num_LUT_c_app == 1:
                        LUT_c_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_c_app_inst_initialinfo_type2)
                        LUT_c_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_c_app_inst_info)
                        LUT_instantiation += LUT_c_app_inst_info
                    else:
                        LUT_c_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 2), LUT_c_inst_initialinfo_type2)
                        LUT_c_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f - 1), LUT_c_inst_info)
                        LUT_instantiation += LUT_c_inst_info
                    if num_LUT_d_app == 1:
                        LUT_d_app_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_d_app_inst_initialinfo)
                        LUT_d_app_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_d_app_inst_info)
                        LUT_instantiation += LUT_d_app_inst_info
                    else:
                        LUT_d_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f - 1), LUT_d_inst_initialinfo)
                        LUT_d_inst_info = re.sub("(<#width2>)", str(self.MultWidth_f), LUT_d_inst_info)
                        LUT_instantiation += LUT_d_inst_info

                    # 4-4-11 for otherapp layers, get instantiation contents of CC modules within for-loops
                    CC4_instantiation, c_tmp_definition, S_D_assignment = gen_CC4_inst(CC4_inst_initialinfo, self.MultWidth_f)

                    # 4-4-12 substitute identifiers in template contents for LUT & CC instantion contents within for-loops
                    if self.AppAttributes[1] != 0:
                        mod_info = re.sub("(<#width3>)", str(num+1), mod_initialinfo_common)
                    else:
                        mod_info = re.sub("(<#width3>)", str(num), mod_initialinfo_common)  
                    mod_info = re.sub("(<LUT instantiation>)", LUT_instantiation, mod_info)
                    mod_info = re.sub("(<CC4 instantiation>)", CC4_instantiation, mod_info)
                    mod_info = re.sub("(<c_tmp definition>)", c_tmp_definition, mod_info)
                    mod_info = re.sub("(<S_D assignment>)", S_D_assignment, mod_info)
                    if self.AppAttributes[1] != 0:
                        with open(self.output_directory + self.layer_output_filename_list[num+1], "w", encoding="utf-8") as f:
                            f.write(mod_info)
                    else:
                        with open(self.output_directory + self.layer_output_filename_list[num], "w", encoding="utf-8") as f:
                            f.write(mod_info)


        return
    # ##################################################### end #####################################################
    



    # ################################################ gen_addertree #############################################
    def gen_adderTree(self):
        count_list = gen_dadda_countlist(self.MultWidth_f, self.MultWidth_b, self.signed, self.type)
        count_list_initial = count_list[:]
        dadda_config_list, count_list_maxindex, count_list_remaining = gen_dadda_config(count_list)
        dadda_mod_path = "../mod_src/tree/dadda.v"
        dadda_output_path = self.output_directory + "dadda.v"
        copyfile(dadda_mod_path, self.output_directory, "dadda.v")            
        gen_dadda_output(dadda_output_path, dadda_config_list, count_list_initial, count_list_maxindex, count_list_remaining, self.MultWidth_f, self.MultWidth_b, self.signed, self.type)
        return

    # ##################################################### end #####################################################





    # ################################################# gen_topFile #################################################
    # write codes into top module files
    '''
    steps:
    1. get template of top modules
    2. substitute width identifiers in template of top modules, and generate initial contents for top modules
    3. write codes into top module files
        3-1 get layer instantiation contents of LUT modules, and write them into top modules
        3-2 generate layer modules' output signals' definition
        3-3 generate dadda tree's input ports
        3-4 generate adder signal assignment
        3-5 substitute identifiers  for adder's width config info
        3-6 write codes into top module file
    '''
    def gen_topFile(self):
        if (self.useapp == 0) and (self.signed == 0):
            # 1. get template of top modules
            if self.combinatory == 1:
                self.mult_mod_path = "../mod_src/mult_combinatory/00/acc_mult_unsigned_mod.v"
            elif self.combinatory == 0:
                self.mult_mod_path = "../mod_src/mult_CPDtest/00/acc_mult_unsigned_mod.v"
            self.mult_output_path = self.output_directory + "acc_mult_unsigned" + str(self.MultWidth_f) + "x" + str(self.MultWidth_b) + ".v"
            copyfile(self.mult_mod_path, self.output_directory, "acc_mult_unsigned" + str(self.MultWidth_f) + "x" + str(self.MultWidth_b) + ".v")
            
            # 2. substitute width identifiers in template of top modules, and generate initial contents for top modules
            mod_info = ""
            with open(self.mult_output_path, "r", encoding="utf-8") as f:
                mod_info = f.read()
            mod_info = re.sub("(<#width1>)", str(self.MultWidth_f), mod_info)
            mod_info = re.sub("(<#width2>)", str(self.MultWidth_b), mod_info)
            log2_MultWidth0 = int(np.log2(self.MultWidth_f))
            log2_MultWidth1 = int(np.log2(self.MultWidth_b))
            mod_info = re.sub("(<#width3>)", str(log2_MultWidth0), mod_info)  # this part can be optimized from view of hdl, but space for  optimization is  small

            # 3. write codes into top module files
            # 3-1 get layer instantiation contents of LUT modules, and write them into top modules
            layer_inst_path = "../inst_src/layer/00/acc_layer_unsigned_inst.v"
            f_input = open(layer_inst_path, "r", encoding="utf-8")
            layer_inst_instantiation = ""
            layer_inst_initialinfo = f_input.read()
            for i in range( int(self.MultWidth_b/2) ):
                layer_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f), layer_inst_initialinfo)
                layer_inst_info = re.sub("(<#width2>)", str(i), layer_inst_info)
                layer_inst_info = re.sub("(<#width3>)", str(i*2), layer_inst_info)
                layer_inst_info = re.sub("(<#width4>)", str(i*2 + 1), layer_inst_info)
                if i == 0:
                    layer_inst_info = re.sub("(1'b0)", "cin ", layer_inst_info)
                layer_inst_instantiation += layer_inst_info
            if self.combinatory == 0:
                layer_inst_instantiation = re.sub("([(]A)", "(A_reg", layer_inst_instantiation)
                layer_inst_instantiation = re.sub("([(]B)", "(B_reg", layer_inst_instantiation)
            mod_info = re.sub("(<layer instantiation>)", layer_inst_instantiation, mod_info)

            # 3-2 generate layer modules' output signals' definition
            wire_sum = ""
            # reg_sum = ""
            # reg_sum_assignment_0 = ""
            # reg_sum_assignment_1 = ""
            for i in range( int(self.MultWidth_b/2) ):  # all widths are even number s in default
                wire_sum += f"wire [width1+1 : 0] sum{i};\n\t"
                # reg_sum += f"reg [width1+1 : 0] sum{i}_reg;\n\t"
                # reg_sum_assignment_0 += f"sum{i}_reg <= 'd0;\n\t\t\t"
                # reg_sum_assignment_1 += f"sum{i}_reg <= sum{i};\n\t\t\t"
            mod_info = re.sub("(<wire sum>)", wire_sum, mod_info)
            # mod_info = re.sub("(<reg sum>)", reg_sum, mod_info)
            # mod_info = re.sub("(<reg sum assignment 0>)", reg_sum_assignment_0, mod_info)
            # mod_info = re.sub("(<reg sum assignment 1>)", reg_sum_assignment_1, mod_info)

            # 3-3 generate dadda tree's input ports
            input_port = ""
            for i in range( int(self.MultWidth_b/2) ):  # all widths are even number s in default
                input_port += f".sum{i}\t\t\t\t(sum{i}\t\t)\t\t\t\t,\n\t\t"
            input_port += "\n"
            mod_info = re.sub("(<sum ports>)", input_port, mod_info)

            # 3-4 generate adder signal assignment
            CLAadderNumberAssignment = ""
            CLAadderNumberAssignment += "wire\t[" + str(self.MultWidth_f+self.MultWidth_b) + ":0]\t\t\t\tnumber_1\t\t\t\t;\n"
            CLAadderNumberAssignment += "\twire\t[" + str(self.MultWidth_f+self.MultWidth_b) + ":0]\t\t\t\tnumber_2\t\t\t\t;\n"
            CLAadderNumberAssignment += "\tassign number_1 = {\n\t\t"
            for i in range(self.MultWidth_f+self.MultWidth_b+3, 2, -1):
                if i != 3:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[0]\t\t\t,\n\t\t"
                else:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[0]\n\t};\n\t"
            CLAadderNumberAssignment += "assign number_2 = {\n\t\t"
            for i in range(self.MultWidth_f+self.MultWidth_b+3, 2, -1):
                if i != 3:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[1]\t\t\t,\n\t\t"
                else:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[1]\n\t};\n\t"
            mod_info = re.sub("(<CLA adder number assignment>)", CLAadderNumberAssignment, mod_info)

            # 3-5 substitute identifiers  for adder's width config info
            mod_info = re.sub("(<#width4>)", str(self.MultWidth_f + self.MultWidth_b), mod_info)
            mod_info = re.sub("(<#width5>)", str(self.CLAadderWidth-1), mod_info)
            mod_info = re.sub("(<#width6>)", str(self.CLAadderWidth), mod_info)
            if self.CLAadderWidth > self.MultWidth_f + self.MultWidth_b + 1:
                tmp_num = self.CLAadderWidth - self.MultWidth_f - self.MultWidth_b - 1
                mod_info = re.sub("(<#adderAreg>)", "{" + str(tmp_num) + "'b0, adder_A_reg}", mod_info)
                mod_info = re.sub("(<#adderBreg>)", "{" + str(tmp_num) + "'b0, adder_B_reg}", mod_info)
            else:
                mod_info = re.sub("(<#adderAreg>)", "adder_A_reg", mod_info)
                mod_info = re.sub("(<#adderBreg>)", "adder_B_reg", mod_info)

            # 3-6 write codes into top module file
            with open(self.mult_output_path, "w", encoding="utf-8") as f:
                f.write(mod_info)
            f_input.close()






        elif (self.useapp == 0) and (self.signed == 1):
            # 1. get template of top modules
            if self.combinatory == 1:
                self.mult_mod_path = "../mod_src/mult_combinatory/01/acc_mult_signed_mod.v"
            else:
                self.mult_mod_path = "../mod_src/mult_CPDtest/01/acc_mult_signed_mod.v"
            self.mult_output_path = self.output_directory + "acc_mult_signed" + str(self.MultWidth_f) + "x" + str(self.MultWidth_b) + ".v"
            copyfile(self.mult_mod_path, self.output_directory, "acc_mult_signed" + str(self.MultWidth_f) + "x" + str(self.MultWidth_b) + ".v")

            # 2. substitute width identifiers in template of top modules, and generate initial contents for top modules
            mod_info = ""
            with open(self.mult_output_path, "r", encoding="utf-8") as f:
                mod_info = f.read()
            mod_info = re.sub("(<#width1>)", str(self.MultWidth_f), mod_info)
            mod_info = re.sub("(<#width2>)", str(self.MultWidth_b), mod_info)
            log2_MultWidth0 = math.ceil(np.log2(self.MultWidth_f))
            log2_MultWidth1 = math.ceil(np.log2(self.MultWidth_b))
            mod_info = re.sub("(<#width3>)", str(log2_MultWidth0), mod_info)

            # 3. write codes into top module files
            # 3-1 get layer instantiation contents of LUT modules, and write them into top modules
            layer_inst_path_list = [
                "../inst_src/layer/01/acc_layer_signed_common_inst.v",
                "../inst_src/layer/01/acc_layer_signed_last_inst.v"
            ]
            f_input_list = [
                open(layer_inst_path_list[0], "r", encoding="utf-8"),
                open(layer_inst_path_list[1], "r", encoding="utf-8")
            ]
            layer_inst_instantiation = ""
            layer_common_inst_initialinfo = f_input_list[0].read()
            for i in range( int(self.MultWidth_b/2)-1 ):
                layer_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f), layer_common_inst_initialinfo)
                layer_inst_info = re.sub("(<#width2>)", str(i), layer_inst_info)
                layer_inst_info = re.sub("(<#width3>)", str(i*2), layer_inst_info)
                layer_inst_info = re.sub("(<#width4>)", str(i*2 + 1), layer_inst_info)
                if i == 0:
                    layer_inst_info = re.sub("(1'b0)", "cin ", layer_inst_info)
                layer_inst_instantiation += layer_inst_info
            layer_last_inst_info = f_input_list[1].read()
            layer_last_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f), layer_last_inst_info)
            layer_last_inst_info = re.sub("(<#width2>)", str(int(self.MultWidth_b/2) - 1), layer_last_inst_info)
            layer_last_inst_info = re.sub("(<#width3>)", str(self.MultWidth_b - 2), layer_last_inst_info)
            layer_last_inst_info = re.sub("(<#width4>)", str(self.MultWidth_b - 1), layer_last_inst_info)
            layer_inst_instantiation += layer_last_inst_info
            if self.combinatory == 0:
                layer_inst_instantiation = re.sub("([(]A)", "(A_reg", layer_inst_instantiation)
                layer_inst_instantiation = re.sub("([(]B)", "(B_reg", layer_inst_instantiation)
            mod_info = re.sub("(<layer instantiation>)", layer_inst_instantiation, mod_info)

            # 3-2 generate layer modules' output signals' definition
            wire_sum = ""
            # reg_sum = ""
            # reg_sum_assignment_0 = ""
            # reg_sum_assignment_1 = ""
            for i in range( int(self.MultWidth_b/2) ):  # all widths are even number s in default
                wire_sum += f"wire [width1+1 : 0] sum{i};\n\t"
                # reg_sum += f"reg [width1+1 : 0] sum{i}_reg;\n\t"
                # reg_sum_assignment_0 += f"sum{i}_reg <= 'd0;\n\t\t\t"
                # reg_sum_assignment_1 += f"sum{i}_reg <= sum{i};\n\t\t\t"
            mod_info = re.sub("(<wire sum>)", wire_sum, mod_info)
            # mod_info = re.sub("(<reg sum>)", reg_sum, mod_info)
            # mod_info = re.sub("(<reg sum assignment 0>)", reg_sum_assignment_0, mod_info)
            # mod_info = re.sub("(<reg sum assignment 1>)", reg_sum_assignment_1, mod_info)

            # 3-3 generate dadda tree's input ports
            input_port = ""
            for i in range( int(self.MultWidth_b/2) ):  # all widths are even number s in default
                input_port += f".sum{i}\t\t\t\t(sum{i}\t\t)\t\t\t\t,\n\t\t"
            input_port += "\n"
            mod_info = re.sub("(<sum ports>)", input_port, mod_info)

            # 3-4 generate  adder signal assignment
            CLAadderNumberAssignment = ""
            CLAadderNumberAssignment += "wire\t[" + str(self.MultWidth_f+self.MultWidth_b) + ":0]\t\t\t\tnumber_1\t\t\t\t;\n"
            CLAadderNumberAssignment += "\twire\t[" + str(self.MultWidth_f+self.MultWidth_b) + ":0]\t\t\t\tnumber_2\t\t\t\t;\n"
            CLAadderNumberAssignment += "\tassign number_1 = {\n\t\t"
            for i in range(self.MultWidth_f+self.MultWidth_b+3, 2, -1):
                if i != 3:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[0]\t\t\t,\n\t\t"
                else:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[0]\n\t};\n\t"
            CLAadderNumberAssignment += "assign number_2 = {\n\t\t"
            for i in range(self.MultWidth_f+self.MultWidth_b+3, 2, -1):
                if i != 3:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[1]\t\t\t,\n\t\t"
                else:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[1]\n\t};\n\t"
            mod_info = re.sub("(<CLA adder number assignment>)", CLAadderNumberAssignment, mod_info)

            # 3-5 substitute identifiers  for adder's width config info
            mod_info = re.sub("(<#width4>)", str(self.MultWidth_f + self.MultWidth_b), mod_info)
            mod_info = re.sub("(<#width5>)", str(self.CLAadderWidth-1), mod_info)
            mod_info = re.sub("(<#width6>)", str(self.CLAadderWidth), mod_info)
            if self.CLAadderWidth > self.MultWidth_f + self.MultWidth_b + 1:
                tmp_num = self.CLAadderWidth - self.MultWidth_f - self.MultWidth_b - 1
                mod_info = re.sub("(<#adderAreg>)", "{" + str(tmp_num) + "'b0, adder_A_reg}", mod_info)
                mod_info = re.sub("(<#adderBreg>)", "{" + str(tmp_num) + "'b0, adder_B_reg}", mod_info)
            else:
                mod_info = re.sub("(<#adderAreg>)", "adder_A_reg", mod_info)
                mod_info = re.sub("(<#adderBreg>)", "adder_B_reg", mod_info)

            # 3-6 write codes into top module file
            with open(self.mult_output_path, "w", encoding="utf-8") as f:
                f.write(mod_info)
            for i in range(2):
                f_input_list[i].close()






        elif (self.useapp == 1) and (self.signed == 0):

            # 1. get template of top modules
            if self.combinatory == 1:
                self.mult_mod_path = "../mod_src/mult_combinatory/10/app_mult_unsigned_mod.v"
            else:
                self.mult_mod_path = "../mod_src/mult_CPDtest/10/app_mult_unsigned_mod.v"
            self.mult_output_path = self.output_directory + "app_mult_unsigned" + str(self.MultWidth_f) + "x" + str(self.MultWidth_b) + ".v"
            copyfile(self.mult_mod_path, self.output_directory, "app_mult_unsigned" + str(self.MultWidth_f) + "x" + str(self.MultWidth_b) + ".v")
            
            # 2. substitute width identifiers in template of top modules, and generate initial contents for top modules
            mod_info = ""
            with open(self.mult_output_path, "r", encoding="utf-8") as f:
                mod_info = f.read()
            mod_info = re.sub("(<#width1>)", str(self.MultWidth_f), mod_info)
            mod_info = re.sub("(<#width2>)", str(self.MultWidth_b), mod_info)
            log2_MultWidth0 = int(np.log2(self.MultWidth_f))
            log2_MultWidth1 = int(np.log2(self.MultWidth_b))
            mod_info = re.sub("(<#width3>)", str(log2_MultWidth0), mod_info)  # this part can be optimized from view of hdl, but space for  optimization is  small

            # 3. write codes into top module files
            # 3-1 get layer instantiation contents of LUT modules, and write them into top modules
            layer_inst_path = "../inst_src/layer/10/app_layer_unsigned_inst.v"
            f_input = open(layer_inst_path, "r", encoding="utf-8")
            layer_inst_instantiation = ""
            layer_inst_initialinfo = f_input.read()
            for i in range( self.AppAttributes[0] ):
                if i == 0:
                    layer_inst_info = re.sub("(1'b0)", "cin ", layer_inst_initialinfo)
                layer_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f), layer_inst_initialinfo)
                layer_inst_info = re.sub("(<#width2>)", str(i), layer_inst_info)
                layer_inst_info = re.sub("(<#width3>)", str(i*2), layer_inst_info)
                layer_inst_info = re.sub("(<#width4>)", str(i*2 + 1), layer_inst_info)
                if i < self.AppAttributes[1]:
                    layer_inst_info = re.sub("(<#width5>)", str(0), layer_inst_info)
                elif i < self.AppAttributes[1] + self.AppAttributes[2]:
                    if self.AppAttributes[1] != 0:
                        layer_inst_info = re.sub("(<#width5>)", str(i - self.AppAttributes[1] + 1), layer_inst_info)
                    else:
                        layer_inst_info = re.sub("(<#width5>)", str(i - self.AppAttributes[1]), layer_inst_info)
                else:
                    if self.AppAttributes[1] != 0:
                        layer_inst_info = re.sub("(<#width5>)", str(1 + self.AppAttributes[2]), layer_inst_info)
                    else:
                        layer_inst_info = re.sub("(<#width5>)", str(self.AppAttributes[2]), layer_inst_info)
                layer_inst_instantiation += layer_inst_info
            for i in range( int(self.MultWidth_b/2) - self.AppAttributes[0] ):
                layer_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f), layer_inst_initialinfo)
                layer_inst_info = re.sub("(<#width2>)", str(self.AppAttributes[0] + i), layer_inst_info)
                layer_inst_info = re.sub("(<#width3>)", str((self.AppAttributes[0] + i)*2), layer_inst_info)
                layer_inst_info = re.sub("(<#width4>)", str((self.AppAttributes[0] + i)*2 + 1), layer_inst_info)
                layer_inst_info = re.sub("(<#width5>)", str(len(self.layer_output_filename_list)-1), layer_inst_info) 
                layer_inst_instantiation += layer_inst_info
            if self.combinatory == 0:
                layer_inst_instantiation = re.sub("([(]A)", "(A_reg", layer_inst_instantiation)
                layer_inst_instantiation = re.sub("([(]B)", "(B_reg", layer_inst_instantiation)
            mod_info = re.sub("(<layer instantiation>)", layer_inst_instantiation, mod_info)

            # 3-2 generate layer modules' output signals' definition
            wire_sum = ""
            # reg_sum = ""
            # reg_sum_assignment_0 = ""
            # reg_sum_assignment_1 = ""
            for i in range( int(self.MultWidth_b/2) ):  # all widths are even number s in default
                wire_sum += f"wire [width1+1 : 0] sum{i};\n\t"
                # reg_sum += f"reg [width1+1 : 0] sum{i}_reg;\n\t"
                # reg_sum_assignment_0 += f"sum{i}_reg <= 'd0;\n\t\t\t"
                # reg_sum_assignment_1 += f"sum{i}_reg <= sum{i};\n\t\t\t"
            mod_info = re.sub("(<wire sum>)", wire_sum, mod_info)
            # mod_info = re.sub("(<reg sum>)", reg_sum, mod_info)
            # mod_info = re.sub("(<reg sum assignment 0>)", reg_sum_assignment_0, mod_info)
            # mod_info = re.sub("(<reg sum assignment 1>)", reg_sum_assignment_1, mod_info)

            # 3-3 generate dadda tree's input ports
            input_port = ""
            for i in range( int(self.MultWidth_b/2) ):  # all widths are even number s in default
                input_port += f".sum{i}\t\t\t\t(sum{i}\t\t)\t\t\t\t,\n\t\t"
            input_port += "\n"
            mod_info = re.sub("(<sum ports>)", input_port, mod_info)

            # 3-4 generate  adder signal assignment
            # CLA adder signals' definitions
            CLAadderNumberAssignment = ""
            CLAadderNumberAssignment += "wire\t[" + str(self.MultWidth_f+self.MultWidth_b) + ":0]\t\t\t\tnumber_1\t\t\t\t;\n"
            CLAadderNumberAssignment += "\twire\t[" + str(self.MultWidth_f+self.MultWidth_b) + ":0]\t\t\t\tnumber_2\t\t\t\t;\n"
            CLAadderNumberAssignment += "\tassign number_1 = {\n\t\t"
            for i in range(self.MultWidth_f+self.MultWidth_b+3, 2, -1):
                if i != 3:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[0]\t\t\t,\n\t\t"
                else:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[0]\n\t};\n\t"
            CLAadderNumberAssignment += "assign number_2 = {\n\t\t"
            for i in range(self.MultWidth_f+self.MultWidth_b+3, 2, -1):
                if i != 3:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[1]\t\t\t,\n\t\t"
                else:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[1]\n\t};\n\t"
            mod_info = re.sub("(<CLA adder number assignment>)", CLAadderNumberAssignment, mod_info)

            # 3-5 substitute identifiers  for adder's width config info
            mod_info = re.sub("(<#width4>)", str(self.MultWidth_f + self.MultWidth_b), mod_info)
            mod_info = re.sub("(<#width5>)", str(self.CLAadderWidth-1), mod_info)
            mod_info = re.sub("(<#width6>)", str(self.CLAadderWidth), mod_info)
            if self.CLAadderWidth > self.MultWidth_f + self.MultWidth_b + 1:
                tmp_num = self.CLAadderWidth - self.MultWidth_f - self.MultWidth_b - 1
                mod_info = re.sub("(<#adderAreg>)", "{" + str(tmp_num) + "'b0, adder_A_reg}", mod_info)
                mod_info = re.sub("(<#adderBreg>)", "{" + str(tmp_num) + "'b0, adder_B_reg}", mod_info)
            else:
                mod_info = re.sub("(<#adderAreg>)", "adder_A_reg", mod_info)
                mod_info = re.sub("(<#adderBreg>)", "adder_B_reg", mod_info)

            # 3-6 write codes into top module file
            with open(self.mult_output_path, "w", encoding="utf-8") as f:
                f.write(mod_info)
            f_input.close()






        elif (self.useapp == 1) and (self.signed == 1):

            # 1. get template of top modules
            if self.combinatory == 1:
                self.mult_mod_path = "../mod_src/mult_combinatory/11/app_mult_signed_mod.v"
            else:
                self.mult_mod_path = "../mod_src/mult_CPDtest/11/app_mult_signed_mod.v"
            self.mult_output_path = self.output_directory + "app_mult_signed" + str(self.MultWidth_f) + "x" + str(self.MultWidth_b) + ".v"
            copyfile(self.mult_mod_path, self.output_directory, "app_mult_signed" + str(self.MultWidth_f) + "x" + str(self.MultWidth_b) + ".v")
            
            # 2. substitute width identifiers in template of top modules, and generate initial contents for top modules
            mod_info = ""
            with open(self.mult_output_path, "r", encoding="utf-8") as f:
                mod_info = f.read()
            mod_info = re.sub("(<#width1>)", str(self.MultWidth_f), mod_info)
            mod_info = re.sub("(<#width2>)", str(self.MultWidth_b), mod_info)
            log2_MultWidth0 = int(np.log2(self.MultWidth_f))
            log2_MultWidth1 = int(np.log2(self.MultWidth_b))
            mod_info = re.sub("(<#width3>)", str(log2_MultWidth0), mod_info)  # this part can be optimized from view of hdl, but space for  optimization is  small

            # 3. write codes into top module files
            # 3-1 get layer instantiation contents of LUT modules, and write them into top modules
            layer_inst_path_list = [
                "../inst_src/layer/11/app_layer_signed_common_inst.v",
                "../inst_src/layer/11/app_layer_signed_last_inst.v"
            ]
            f_input_list = [
                open(layer_inst_path_list[0], "r", encoding="utf-8"),
                open(layer_inst_path_list[1], "r", encoding="utf-8")
            ]
            layer_inst_instantiation = ""
            layer_common_inst_initialinfo = f_input_list[0].read()
            for i in range( int(self.MultWidth_b/2)-1 ): 
                layer_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f), layer_common_inst_initialinfo)
                layer_inst_info = re.sub("(<#width2>)", str(i), layer_inst_info)
                layer_inst_info = re.sub("(<#width3>)", str(i*2), layer_inst_info)
                layer_inst_info = re.sub("(<#width4>)", str(i*2 + 1), layer_inst_info)
                if i < self.AppAttributes[1]:
                    layer_inst_info = re.sub("(<#width5>)", str(0), layer_inst_info)  # approximation introduced info
                elif i < self.AppAttributes[0]:
                    if self.AppBits >= self.MultWidth_f:
                        layer_inst_info = re.sub("(<#width5>)", str(i - self.AppAttributes[1] + 1), layer_inst_info)  # approximation introduced info
                    else:
                        layer_inst_info = re.sub("(<#width5>)", str(i - self.AppAttributes[1]), layer_inst_info)  # approximation introduced info
                else:
                    if self.AppBits >= self.MultWidth_f:
                        layer_inst_info = re.sub("(<#width5>)", str(self.AppAttributes[2] + 1), layer_inst_info)  # approximation introduced info
                    else:
                        layer_inst_info = re.sub("(<#width5>)", str(self.AppAttributes[2]), layer_inst_info)  # approximation introduced info

                if i == 0:
                    layer_inst_info = re.sub("(1'b0)", "cin ", layer_inst_info)
                layer_inst_instantiation += layer_inst_info
            layer_last_inst_info = f_input_list[1].read()
            layer_last_inst_info = re.sub("(<#width1>)", str(self.MultWidth_f), layer_last_inst_info)
            layer_last_inst_info = re.sub("(<#width2>)", str(int(self.MultWidth_b/2) - 1), layer_last_inst_info)
            layer_last_inst_info = re.sub("(<#width3>)", str(self.MultWidth_b - 2), layer_last_inst_info)
            layer_last_inst_info = re.sub("(<#width4>)", str(self.MultWidth_b - 1), layer_last_inst_info)
            layer_inst_instantiation += layer_last_inst_info
            if self.combinatory == 0:
                layer_inst_instantiation = re.sub("([(]A)", "(A_reg", layer_inst_instantiation)
                layer_inst_instantiation = re.sub("([(]B)", "(B_reg", layer_inst_instantiation)
            mod_info = re.sub("(<layer instantiation>)", layer_inst_instantiation, mod_info)

            # 3-2 generate layer modules' output signals' definition
            wire_sum = ""
            # reg_sum = ""
            # reg_sum_assignment_0 = ""
            # reg_sum_assignment_1 = ""
            for i in range( int(self.MultWidth_b/2) ):  # all widths are even number s in default
                wire_sum += f"wire [width1+1 : 0] sum{i};\n\t"
                # reg_sum += f"reg [width1+1 : 0] sum{i}_reg;\n\t"
                # reg_sum_assignment_0 += f"sum{i}_reg <= 'd0;\n\t\t\t"
                # reg_sum_assignment_1 += f"sum{i}_reg <= sum{i};\n\t\t\t"
            mod_info = re.sub("(<wire sum>)", wire_sum, mod_info)
            # mod_info = re.sub("(<reg sum>)", reg_sum, mod_info)
            # mod_info = re.sub("(<reg sum assignment 0>)", reg_sum_assignment_0, mod_info)
            # mod_info = re.sub("(<reg sum assignment 1>)", reg_sum_assignment_1, mod_info)

            # 3-3 generate dadda tree's input ports
            input_port = ""
            for i in range( int(self.MultWidth_b/2) ):  # all widths are even number s in default
                input_port += f".sum{i}\t\t\t\t(sum{i}\t\t)\t\t\t\t,\n\t\t"
            input_port += "\n"
            mod_info = re.sub("(<sum ports>)", input_port, mod_info)

            # 3-4 generate adder signal assignment
            CLAadderNumberAssignment = ""
            CLAadderNumberAssignment += "wire\t[" + str(self.MultWidth_f+self.MultWidth_b) + ":0]\t\t\t\tnumber_1\t\t\t\t;\n"
            CLAadderNumberAssignment += "\twire\t[" + str(self.MultWidth_f+self.MultWidth_b) + ":0]\t\t\t\tnumber_2\t\t\t\t;\n"
            CLAadderNumberAssignment += "\tassign number_1 = {\n\t\t"
            for i in range(self.MultWidth_f+self.MultWidth_b+3, 2, -1):
                if i != 3:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[0]\t\t\t,\n\t\t"
                else:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[0]\n\t};\n\t"
            CLAadderNumberAssignment += "assign number_2 = {\n\t\t"
            for i in range(self.MultWidth_f+self.MultWidth_b+3, 2, -1):
                if i != 3:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[1]\t\t\t,\n\t\t"
                else:
                    CLAadderNumberAssignment += "sum_" + str(i) + "[1]\n\t};\n\t"
            mod_info = re.sub("(<CLA adder number assignment>)", CLAadderNumberAssignment, mod_info)

            # 3-5 substitute identifiers for adder's width config info
            mod_info = re.sub("(<#width4>)", str(self.MultWidth_f + self.MultWidth_b), mod_info)
            mod_info = re.sub("(<#width5>)", str(self.CLAadderWidth-1), mod_info)
            mod_info = re.sub("(<#width6>)", str(self.CLAadderWidth), mod_info)
            if self.CLAadderWidth > self.MultWidth_f + self.MultWidth_b + 1:
                tmp_num = self.CLAadderWidth - self.MultWidth_f - self.MultWidth_b - 1
                mod_info = re.sub("(<#adderAreg>)", "{" + str(tmp_num) + "'b0, adder_A_reg}", mod_info)
                mod_info = re.sub("(<#adderBreg>)", "{" + str(tmp_num) + "'b0, adder_B_reg}", mod_info)
            else:
                mod_info = re.sub("(<#adderAreg>)", "adder_A_reg", mod_info)
                mod_info = re.sub("(<#adderBreg>)", "adder_B_reg", mod_info)
            
            # 3-6 write codes into top module file
            with open(self.mult_output_path, "w", encoding="utf-8") as f:
                f.write(mod_info)
            for i in range(2):
                f_input_list[i].close()


        return
    
    # ###################################################### end ##########################################################
    





    # ################################################# copy_CLAadderFiles #################################################
    # copy adder files to output directory
    def copy_2inputAdderFiles(self):
        # possible optimization: if approximate multipliers are configed with all-0-output modules, width of adders can be reduced
        if self.MultWidth_f + self.MultWidth_b <= 8:
            self.CLAadderWidth = 8
        elif 8 < self.MultWidth_f + self.MultWidth_b <= 16:
            self.CLAadderWidth = 16
        elif 16 < self.MultWidth_f + self.MultWidth_b <= 24:
            self.CLAadderWidth = 24
        elif 24 < self.MultWidth_f + self.MultWidth_b <= 32:
            self.CLAadderWidth = 32
        elif 32 < self.MultWidth_f + self.MultWidth_b <= 48:
            self.CLAadderWidth = 48
        elif 48 < self.MultWidth_f + self.MultWidth_b <= 64:
            self.CLAadderWidth = 64
        else:
            self.CLAadderWidth = 72
        adderfile_path = "../adder_src/adder" + str(self.CLAadderWidth) + "/"
        filenames = os.listdir(adderfile_path)
        for filename in filenames:
            copyfile(adderfile_path + filename, self.output_directory, filename)
        return
    # ###################################################### end ##########################################################






    # ################################################# gen_testbench #################################################
    # generate testbench
    def gen_testbench(self):
        if (self.useapp == 0) and (self.signed == 0):
            number_list = []
            for i in range(6):
                number_list.append( random.randint(2**(self.MultWidth_f-3), 2**(self.MultWidth_f-1)) )
                number_list.append( random.randint(2**(self.MultWidth_b-3), 2**(self.MultWidth_b-1)) )
            sys_clk_cycle = 10
            if not os.path.exists("../output/sim/"):
                os.mkdir("../output/sim/")
            if self.combinatory == 1:
                self.tb_path = "../mod_src/tb_combinatory/tb_acc_unsigned.v"
            else:
                self.tb_path = "../mod_src/tb_CPDtest/tb_acc_unsigned.v"
            with open(self.tb_path, "r", encoding="utf-8") as f_input, \
                open("../output/sim/tb.v", "w", encoding="utf-8") as f_output:
                tb_info = f_input.read()
                tb_info = re.sub("<#width1>", str(self.MultWidth_f), tb_info)
                tb_info = re.sub("<#width2>", str(self.MultWidth_b), tb_info)
                tb_info = re.sub("<#time>", str( 5 * sys_clk_cycle * (self.MultWidth_f + math.ceil(np.log2(self.MultWidth_b + 3)) + 2) ), tb_info)  # +1就够了
                for i in range(12):
                    tb_info = re.sub("<#number" + str(i+1) + ">", str(number_list[i]), tb_info)
                f_output.write(tb_info)
        elif (self.useapp == 0) and (self.signed == 1):
            number_list = []
            for i in range(6):
                number_list.append( random.randint(2**(self.MultWidth_f-3), 2**(self.MultWidth_f-1)) )
                number_list.append( random.randint(2**(self.MultWidth_b-3), 2**(self.MultWidth_b-1)) )
            sys_clk_cycle = 10
            if not os.path.exists("../output/sim/"):
                os.mkdir("../output/sim/")
            if self.combinatory == 1:
                self.tb_path = "../mod_src/tb_combinatory/tb_acc_signed.v"
            else:
                self.tb_path = "../mod_src/tb_CPDtest/tb_acc_signed.v"
            with open(self.tb_path, "r", encoding="utf-8") as f_input, \
                open("../output/sim/tb.v", "w", encoding="utf-8") as f_output:
                tb_info = f_input.read()
                tb_info = re.sub("<#width1>", str(self.MultWidth_f), tb_info)
                tb_info = re.sub("<#width2>", str(self.MultWidth_b), tb_info)
                # ##################################### self-selection for simulating time ################################
                tb_info = re.sub("<#time>", str( 5 * sys_clk_cycle * (self.MultWidth_f + math.ceil(np.log2(self.MultWidth_b/2 + 3)) + 1) ), tb_info)  # 后面+1就够了
                # #################################################### end ###############################################
                for i in range(12):
                    tb_info = re.sub("<#number" + str(i+1) + ">", str(number_list[i]), tb_info)
                f_output.write(tb_info)
        elif (self.useapp == 1) and (self.signed == 0):
            number_list = []
            for i in range(6):
                number_list.append( random.randint(2**(self.MultWidth_f-3), 2**(self.MultWidth_f-1)) )
                number_list.append( random.randint(2**(self.MultWidth_b-3), 2**(self.MultWidth_b-1)) )
            sys_clk_cycle = 10
            if not os.path.exists("../output/sim/"):
                os.mkdir("../output/sim/")
            if self.combinatory == 1:
                self.tb_path = "../mod_src/tb_combinatory/tb_app_unsigned.v"
            else:
                self.tb_path = "../mod_src/tb_CPDtest/tb_app_unsigned.v"
            with open(self.tb_path, "r", encoding="utf-8") as f_input, \
                open("../output/sim/tb.v", "w", encoding="utf-8") as f_output:
                tb_info = f_input.read()
                tb_info = re.sub("<#width1>", str(self.MultWidth_f), tb_info)
                tb_info = re.sub("<#width2>", str(self.MultWidth_b), tb_info)
                tb_info = re.sub("<#time>", str( 5 * sys_clk_cycle * (self.MultWidth_f + math.ceil(np.log2(self.MultWidth_b + 3)) + 2) ), tb_info)  # +1就够了
                for i in range(12):
                    tb_info = re.sub("<#number" + str(i+1) + ">", str(number_list[i]), tb_info)
                f_output.write(tb_info)
        elif (self.useapp == 1) and (self.signed == 1):
            number_list = []
            for i in range(6):
                number_list.append( random.randint(2**(self.MultWidth_f-3), 2**(self.MultWidth_f-1)) )
                number_list.append( random.randint(2**(self.MultWidth_b-3), 2**(self.MultWidth_b-1)) )
            sys_clk_cycle = 10
            if not os.path.exists("../output/sim/"):
                os.mkdir("../output/sim/")
            if self.combinatory == 1:
                self.tb_path = "../mod_src/tb_combinatory/tb_app_signed.v"
            else:
                self.tb_path = "../mod_src/tb_CPDtest/tb_app_signed.v"
            with open(self.tb_path, "r", encoding="utf-8") as f_input, \
                open("../output/sim/tb.v", "w", encoding="utf-8") as f_output:
                tb_info = f_input.read()
                tb_info = re.sub("<#width1>", str(self.MultWidth_f), tb_info)
                tb_info = re.sub("<#width2>", str(self.MultWidth_b), tb_info)
                tb_info = re.sub("<#time>", str( 5 * sys_clk_cycle * (self.MultWidth_f + math.ceil(np.log2(self.MultWidth_b/2 + 3)) + 1) ), tb_info)  # 后面+1就够了
                for i in range(12):
                    tb_info = re.sub("<#number" + str(i+1) + ">", str(number_list[i]), tb_info)
                f_output.write(tb_info)
        return
    # ###################################################### end ##########################################################


