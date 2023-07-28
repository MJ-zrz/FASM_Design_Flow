import math
import re

'''
Dadda Tree related function:
gen_dadda_countlist function generates basic info about how many rows there are in each column;
gen_dadda_config function generates dadda Tree's config info;
gen_dadda_output function generates dadda Tree's codes
'''

def gen_dadda_countlist(MultWidth_f, MultWidth_b, signed, type="baugh-wooley"):
    if type == "baugh-wooley":
        cols_eachrow = MultWidth_f + 2
        count_list = [0] * (MultWidth_f + MultWidth_b)  # for example, 16x16 -> 32
        rows = math.ceil(MultWidth_b / 2)  # here are "rows" layer modules in a multiplier
        for i in range(rows):
            for j in range(2*i, cols_eachrow + 2*i):  # for example, as for a 16x16 multiplier, every layer outputs a 18-length vector, then j is ranged from 0~17, 2~19, ..., 14~31 and so forth
                count_list[j] += 1
        
        # for signed cases, here are extra constants required by Baugh-Wooley algorithm 
        if signed == 1:
            if MultWidth_f != MultWidth_b:
                count_list[MultWidth_f-1] += 1
                count_list[MultWidth_b-1] += 1
                count_list[MultWidth_f+MultWidth_b-1] += 1
            else:
                count_list[MultWidth_f] += 1
                count_list[2*MultWidth_f-1] += 1
    elif type == "booth":
        cols_eachrow = MultWidth_f + 2
        count_list = [0] * (MultWidth_f + MultWidth_b)  # for example, 16x16 -> 32
        rows = math.ceil(MultWidth_b / 2)  # here are "rows" layer modules in a multiplier
        for i in range(rows):
            for j in range(2*i, MultWidth_f + MultWidth_b):
                count_list[j] += 1

    return count_list



def gen_dadda_config(count_list):
    dadda_config_list = []  # each element: (a,b,c,d,e) or (a,b,c,d). element[-2] refers to index of own column, while element[-1] refers to index of next column
    
    count_list_remaining = count_list[:]
    count_list_finishnum = [0] * len(count_list[:])
    count_list_maxindex = [x-1 for x in count_list[:]]  # the max index used yet for each column
    # num_t refers to row number this column
    # num_n refers to row number next column
    # use 1 HA: num_t - 1, num_n + 1
    # use 1 FA: num_t - 2, num_n + 1
        
    while(max(count_list_remaining) > 2):
        FA_START_FLAG = 0
        for i in range( len(count_list_remaining) ):
            element = []
            count = count_list_remaining[i]
            if count > 2 and FA_START_FLAG == 0:
                FA_START_FLAG = 1
                # 1HA
                element.append(i)
                element.append(count_list_finishnum[i])
                element.append(count_list_finishnum[i]+1)
                element.append(count_list_maxindex[i]+1)
                element.append(count_list_maxindex[i+1]+1)
                count_list_remaining[i] -= 1
                count_list_remaining[i+1] += 1
                count_list_finishnum[i] += 2
                count_list_maxindex[i] += 1
                count_list_maxindex[i+1] += 1
            elif count > 2 and FA_START_FLAG == 1:
                # 1FA
                if i != len(count_list_remaining)-1:
                    element.append(i)
                    element.append(count_list_finishnum[i])
                    element.append(count_list_finishnum[i]+1)
                    element.append(count_list_finishnum[i]+2)
                    element.append(count_list_maxindex[i]+1)
                    element.append(count_list_maxindex[i+1]+1)
                    count_list_remaining[i] -= 2
                    count_list_remaining[i+1] += 1
                    count_list_finishnum[i] += 3
                    count_list_maxindex[i] += 1
                    count_list_maxindex[i+1] += 1
                else:
                    element.append(i)
                    element.append(count_list_finishnum[i])
                    element.append(count_list_finishnum[i]+1)
                    element.append(count_list_finishnum[i]+2)
                    element.append(count_list_maxindex[i]+1)
                    element.append("")
                    count_list_remaining[i] -= 2
                    count_list_finishnum[i] += 3
                    count_list_maxindex[i] += 1
            if len(element) > 1:
                dadda_config_list.append( tuple(element) )
    return dadda_config_list, count_list_maxindex, count_list_remaining


# def replace_FA(dadda_config_list):
#     CARRY4_list = []
#     for i in range( len(dadda_config_list) ):
#         adder = dadda_config_list[i]
#         if len(adder) == 5:
#             continue
#         elif len(adder) == 6:



#     return


def gen_dadda_output(dadda_output_path, dadda_config_list, count_list_initial, count_list_maxindex, count_list_remaining, MultWidth_f, MultWidth_b, signed, type):
    print(count_list_initial)
    print(count_list_maxindex)
    mod_info = ""
    with open(dadda_output_path, "r", encoding="utf-8") as f:
        mod_info = f.read()

    definition = ""
    for i in range( len(count_list_initial) ):
        index = count_list_initial[i]-1
        if i == 0:
            definition += f"wire\t\t[{index}:0]\t\t\t\tsum_column{i}\t\t\t\t;\n"
        else:
            definition += f"\twire\t\t[{index}:0]\t\t\t\tsum_column{i}\t\t\t\t;\n"
    mod_info = re.sub("(<sum_column signal definition>)", definition, mod_info)

    HA_FA = ""
    FA_instantiation = '''
    FA FA_inst_<#width1>(
        .A              (sum_column<#width2>[<#width4>])            ,
        .B              (sum_column<#width2>[<#width5>])            ,
        .Cin            (sum_column<#width2>[<#width6>])            ,
        .sum            (sum_column<#width2>[<#width7>])            ,
        .carry          (sum_column<#width3>[<#width8>])               //           
    );    
    '''
    HA_instantiation = '''
    HA HA_inst_<#width1>(
        .A              (sum_column<#width2>[<#width4>])            ,
        .B              (sum_column<#width2>[<#width5>])            ,
        .sum            (sum_column<#width2>[<#width6>])            ,
        .carry          (sum_column<#width3>[<#width7>])               //           
    );   
    '''
    for i in range( len(dadda_config_list) ):
        element = dadda_config_list[i]
        inst = ""
        if len(element) == 5:
            inst = re.sub("(<#width1>)", str(i), HA_instantiation)
            inst = re.sub("(<#width2>)", str(element[0]), inst)
            inst = re.sub("(<#width3>)", str(element[0]+1), inst)
            inst = re.sub("(<#width4>)", str(element[1]), inst)
            inst = re.sub("(<#width5>)", str(element[2]), inst)
            inst = re.sub("(<#width6>)", str(element[3]), inst)
            inst = re.sub("(<#width7>)", str(element[4]), inst)
        elif len(element) == 6:
            inst = re.sub("(<#width1>)", str(i), FA_instantiation)
            inst = re.sub("(<#width2>)", str(element[0]), inst)
            inst = re.sub("(<#width3>)", str(element[0]+1), inst)
            inst = re.sub("(<#width4>)", str(element[1]), inst)
            inst = re.sub("(<#width5>)", str(element[2]), inst)
            inst = re.sub("(<#width6>)", str(element[3]), inst)
            inst = re.sub("(<#width7>)", str(element[4]), inst)
            inst = re.sub("(<#width8>)", str(element[5]), inst)
        HA_FA += inst

    for i in range( len(count_list_initial) ):
        for j in range(count_list_initial[i], count_list_maxindex[i]+1):
            HA_FA = re.sub("(sum_column"+str(i)+"\["+str(j)+"\])", f"sum_column{i}_{j}", HA_FA)
    HA_FA = re.sub("(sum_column"+str(MultWidth_f+MultWidth_b)+"\[])", "", HA_FA)
    mod_info = re.sub("(<HA & FA>)", HA_FA, mod_info)


    vector_assignment = '''assign vector0 = {\n\
        <vector0>
    };\n\
    assign vector1 = {\n\
        <vector1>
    };\n
    '''
    vector0 = ""
    vector1 = ""
    for i in range( len(count_list_maxindex)-1, -1, -1 ):
        maxindex = count_list_maxindex[i]
        if i == 0:
            vector0 += f"\t\tsum_column0[0]\t\t\t\t\t\t\t\t\n"
            vector1 += f"\t\t1'b0\t\t\t\t\t\t\t\t\t\t\n"
        elif i == 1:
            vector0 += f"\t\tsum_column1[0]\t\t\t\t,\t\t\t\t\n"
            vector1 += f"\t\t1'b0\t\t\t\t\t\t,\t\t\t\t\n"
        else:
            if count_list_remaining[i] == 2:
                if i == len(count_list_maxindex) - 1:
                    if maxindex-1 >= count_list_initial[i]:
                        vector0 += f"sum_column{i}_{maxindex-1}\t\t\t\t,\t\t\t\t\n"
                    else:
                        vector0 += f"sum_column{i}[{maxindex-1}]\t\t\t\t,\t\t\t\t\n"
                    if maxindex >= count_list_initial[i]:
                        vector1 += f"sum_column{i}_{maxindex}\t\t\t\t,\t\t\t\t\n"
                    else:
                        vector1 += f"sum_column{i}[{maxindex}]\t\t\t\t,\t\t\t\t\n"
                else:
                    if maxindex-1 >= count_list_initial[i]:
                        vector0 += f"\t\tsum_column{i}_{maxindex-1}\t\t\t\t,\t\t\t\t\n"
                    else:
                        vector0 += f"\t\tsum_column{i}[{maxindex-1}]\t\t\t\t,\t\t\t\t\n"
                    if maxindex >= count_list_initial[i]:
                        vector1 += f"\t\tsum_column{i}_{maxindex}\t\t\t\t,\t\t\t\t\n"
                    else:
                        vector1 += f"\t\tsum_column{i}[{maxindex}]\t\t\t\t,\t\t\t\t\n"
            elif count_list_remaining[i] == 1:
                if i == len(count_list_maxindex) - 1:
                    vector0 += f"1'b0\t\t\t\t\t\t\t,\t\t\t\t\n"
                    if maxindex >= count_list_initial[i]:
                        vector1 += f"sum_column{i}_{maxindex}\t\t\t\t,\t\t\t\t\n"
                    else:
                        vector1 += f"sum_column{i}[{maxindex}]\t\t\t\t,\t\t\t\t\n"
                else:
                    vector0 += f"\t\t1'b0\t\t\t\t\t\t\t,\t\t\t\t\n"
                    if maxindex >= count_list_initial[i]:
                        vector1 += f"\t\tsum_column{i}_{maxindex}\t\t\t\t,\t\t\t\t\n"
                    else:
                        vector1 += f"\t\tsum_column{i}[{maxindex}]\t\t\t\t,\t\t\t\t\n"
    vector_assignment = re.sub("(<vector0>)", vector0, vector_assignment)
    vector_assignment = re.sub("(<vector1>)", vector1, vector_assignment)
    mod_info = re.sub("(<vector assignment>)", vector_assignment, mod_info)

    sum_column_assignment = ""
    sum_column_assignment_list = []
    cols_eachrow = MultWidth_f + 2
    rows = math.ceil(MultWidth_b / 2)  # here are "rows" layer modules in a multiplier
    for i in range(MultWidth_f + MultWidth_b):
        sum_column_assignment_list.append([])
    if type == "baugh-wooley":
        for i in range(rows):
            for j in range(2*i, cols_eachrow + 2*i):
                sum_column_assignment_list[j].append( tuple([i, j-2*i]) )
        for i in range(MultWidth_f + MultWidth_b):
            thiscol_outputinfo_list = sum_column_assignment_list[i]  # a list whose elements are tuples
            thiscol_outputinfo = "assign\t\tsum_column" + str(i) +"\t\t\t\t=\t\t{"
            if signed == 1:
                if MultWidth_f != MultWidth_b:
                    if i == MultWidth_f - 1 or i == MultWidth_b - 1 or i == MultWidth_f+MultWidth_b-1:
                        thiscol_outputinfo += "1'b1, "
                else:
                    if i == MultWidth_f or i == 2*MultWidth_f-1:
                        thiscol_outputinfo += "1'b1, "
            for j in range( len(thiscol_outputinfo_list) ):
                thiscol_outputinfo += "sum" + str(thiscol_outputinfo_list[j][0]) + "[" + str(thiscol_outputinfo_list[j][1]) + "]"
                if j != len(thiscol_outputinfo_list) - 1:
                    thiscol_outputinfo += ", "
                else:
                    thiscol_outputinfo += "}\t\t\t\t;\n\t"
            sum_column_assignment += thiscol_outputinfo
    elif type == "booth":
        for i in range(rows):
            for j in range(2*i, MultWidth_f + MultWidth_b):
                sum_column_assignment_list[j].append( tuple([i, j-2*i]) )
        for i in range(MultWidth_f + MultWidth_b):
            thiscol_outputinfo_list = sum_column_assignment_list[i]  # a list whose elements are tuples
            thiscol_outputinfo = "assign\t\tsum_column" + str(i) +"\t\t\t\t=\t\t{"
            for j in range( len(thiscol_outputinfo_list) ):
                thiscol_outputinfo += "sum" + str(thiscol_outputinfo_list[j][0]) + "[" + str(thiscol_outputinfo_list[j][1]) + "]"
                if j != len(thiscol_outputinfo_list) - 1:
                    thiscol_outputinfo += ", "
                else:
                    thiscol_outputinfo += "}\t\t\t\t;\n\t"
            sum_column_assignment += thiscol_outputinfo        
    mod_info = re.sub("(<sum_column signal assignment>)", sum_column_assignment, mod_info)

    mid_signal_assignment = ""
    for i in range( len(count_list_initial) ):
        for j in range(count_list_initial[i], count_list_maxindex[i]+1):
            mid_signal_assignment += f"\twire\t\tsum_column{i}_{j}\t\t\t\t;\n"
    mod_info = re.sub("(<mid signal assignment>)", mid_signal_assignment, mod_info)

    input_definition = ""
    if type == "baugh-wooley":
        for i in range( int(MultWidth_b/2) ):  # all widths are even number s in default
            input_definition += f"input\t\t\t\t[InputWidth-1 : 0]\t\t\t\tsum{i}\t\t\t\t,\n\t"
    elif type == "booth":
        for i in range( int(MultWidth_b/2) ):
            if i == int(MultWidth_b/2)-1:
                input_definition += f"input\t\t\t\t[InputWidth-1 : 0]\t\t\t\tsum{i}\t\t\t\t,\n\t"
            else:
                input_definition += f"input\t\t\t\t[InputWidth+{MultWidth_b - 2 - 2*i - 1} : 0]\t\t\t\tsum{i}\t\t\t\t,\n\t"

    input_definition += "\n"
    mod_info = re.sub("(<input definition>)", input_definition, mod_info)

    mod_info = re.sub("(<#width1>)", str(MultWidth_f + 2), mod_info)
    mod_info = re.sub("(<#width2>)", str(MultWidth_f + MultWidth_b), mod_info)

    with open(dadda_output_path, "w", encoding="utf-8") as f:
        f.write(mod_info)

    return


if __name__ == "__main__":
    MultWidth_f = 16
    MultWidth_b = 16
    signed = 1
    count_list = gen_dadda_countlist(MultWidth_f, MultWidth_b, signed)
    count_list_initial = count_list[:]
    dadda_config_list, count_list_maxindex, count_list_remaining = gen_dadda_config(count_list)
    # for config in dadda_config_list:
    #     print(config)
    # print(count_list_maxindex)
    # print(count_list_remaining)

    dadda_output_path = "./dadda.v"
    gen_dadda_output(dadda_output_path, dadda_config_list, count_list_initial, count_list_maxindex, count_list_remaining, MultWidth_f, MultWidth_b, signed)

