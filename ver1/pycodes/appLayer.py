'''
approximation related function:
gen_appAttributes function generates approximation bits' info;
gen_appunsignedLayer_configInfo and gen_appsignedLayer_configInfo functions generate approximation config info
'''

def gen_appAttributes(MultWidth_f, MultWidth_b, useapp, AppBits):
    if useapp == 0:
        return 0, 0, 0, int( MultWidth_b/2 )
    # for cases where the approximate bit width is very high, the reverse calculation can be used for cases where the approximate bit width is very low
    num = int( MultWidth_b/2 )
    num_app = 0
    num_allapp = 0
    num_otherapp = 0
    num_noapp = 0
    if AppBits < MultWidth_f:
        num_app = int( (AppBits+1)/2 )
        num_allapp = 0
        num_otherapp = num_app
        num_noapp = num - num_app
    elif MultWidth_f <= AppBits < MultWidth_b:
        num_app = int( (AppBits+1)/2 )
        num_allapp = int( (AppBits-MultWidth_f)/2 ) + 1
        num_otherapp = num_app - num_allapp
        num_noapp = num - num_app
    elif AppBits >= MultWidth_b:
        num_app = num
        num_allapp = int( (AppBits-MultWidth_f)/2 ) + 1
        num_otherapp = num_app - num_allapp
        num_noapp = 0
    # print(num_app, num_allapp, num_otherapp, num_noapp)
    return num_app, num_allapp, num_otherapp, num_noapp



def gen_appunsignedLayer_configInfo(MultWidth_f, AppBits, AppAttributes):
    # elements of configInfo_list are dicts storing modules needed for each layer. Keys are presented as "LUT_a", "LUT_a_app", "ifLUT_b_app", "LUT_CC", "LUT_CC_app" and so forth
    # len(configInfo_list) = num_app
    configInfo_list = []
    num_app = AppAttributes[0]
    num_allapp = AppAttributes[1]
    num_noapp = AppAttributes[3]

    for i in range(num_app):
        list_element = {}
        list_element["LUT_a_app"]               =   0
        list_element["LUT_a"]                   =   0
        list_element["ifLUT_b_app"]             =   0  # LUT_b/LUT_b_app is used only once in a layer
        configInfo_list.append(list_element)

    for i in range(num_app):
        if num_allapp > 0:
            if i < num_allapp:
                configInfo_list[i]["LUT_a_app"]                 =   MultWidth_f - 1
                configInfo_list[i]["LUT_a"]                     =   0
                configInfo_list[i]["ifLUT_b_app"]               =   1
            else:
                if AppBits % 2 == 0:
                    configInfo_list[i]["LUT_a_app"]                 =   MultWidth_f - 2 - 2*(i - num_allapp)
                    configInfo_list[i]["LUT_a"]                     =   1 + 2*(i - num_allapp)
                    configInfo_list[i]["ifLUT_b_app"]               =   0
                else:
                    configInfo_list[i]["LUT_a_app"]                 =   MultWidth_f - 1 - 2*(i - num_allapp)
                    configInfo_list[i]["LUT_a"]                     =   2*(i - num_allapp)
                    configInfo_list[i]["ifLUT_b_app"]               =   0
        else:
            if (num_noapp != 0) or ((num_noapp == 0) and (i != num_app-1)):
                configInfo_list[i]["LUT_a_app"]                 =   AppBits - 2*i
                configInfo_list[i]["LUT_a"]                     =   MultWidth_f - AppBits + 2*i - 2
                configInfo_list[i]["ifLUT_b_app"]               =   0
    return configInfo_list


def gen_appsignedLayer_configInfo(MultWidth_f, AppBits, AppAttributes):
    # elements of configInfo_list are dicts storing modules needed for each layer. Keys are presented as "LUT_a", "LUT_a_app", "ifLUT_c_app", "ifLUT_d_app", "LUT_CC", "LUT_CC_app" and so forth
    # len(configInfo_list) = num_app
    configInfo_list = []
    num_app = AppAttributes[0]
    num_allapp = AppAttributes[1]
    num_otherapp = AppAttributes[2]
    num_noapp = AppAttributes[3]

    for i in range(num_app):
        if num_noapp != 0:
            list_element = {}
            list_element["LUT_a_app"] = 0
            list_element["LUT_a"] = 0
            list_element["ifLUT_c_app"] = 0  # LUT_c_app here is type2 LUT_c
            list_element["ifLUT_d_app"] = 0
            configInfo_list.append(list_element)
        else:
            if i != num_app - 1:
                list_element = {}
                list_element["LUT_a_app"] = 0
                list_element["LUT_a"] = 0
                list_element["ifLUT_c_app"] = 0  # LUT_c_app here is type2 LUT_c
                list_element["ifLUT_d_app"] = 0
                configInfo_list.append(list_element)
            else:
                list_element = {}
                list_element["LUT_c_app"] = 0
                list_element["LUT_c"] = 0
                list_element["ifLUT_e_app"] = 0
                list_element["ifLUT_b_app"] = 0
                configInfo_list.append(list_element)                           

    for i in range(num_app):
        if num_allapp != 0:
            if i < num_allapp:
                configInfo_list[i]["LUT_a_app"]                 =   MultWidth_f - 2
                configInfo_list[i]["LUT_a"]                     =   0
                configInfo_list[i]["ifLUT_c_app"]               =   1
                configInfo_list[i]["ifLUT_d_app"]               =   1
            else:
                if (num_noapp != 0) or ((num_noapp == 0) and (i != num_app-1)):
                    if AppBits % 2 == 0:
                        configInfo_list[i]["LUT_a_app"]                 =   MultWidth_f - 2 - 2*(i - num_allapp)
                        configInfo_list[i]["LUT_a"]                     =   2*(i - num_allapp)
                        configInfo_list[i]["ifLUT_c_app"]               =   0
                        configInfo_list[i]["ifLUT_d_app"]               =   0
                    else:
                        if i == num_allapp:
                            configInfo_list[i]["LUT_a_app"]                 =   MultWidth_f - 2
                            configInfo_list[i]["LUT_a"]                     =   0
                            configInfo_list[i]["ifLUT_c_app"]               =   1
                            configInfo_list[i]["ifLUT_d_app"]               =   0
                        else:
                            configInfo_list[i]["LUT_a_app"]                 =   MultWidth_f - 1 - 2*(i - num_allapp)
                            configInfo_list[i]["LUT_a"]                     =   2*(i - num_allapp) - 1
                            configInfo_list[i]["ifLUT_c_app"]               =   0
                            configInfo_list[i]["ifLUT_d_app"]               =   0
                else:  # if num_noapp is 0, last layer should also be approximate type
                    if AppBits % 2 == 0:
                        configInfo_list[i]["LUT_c_app"]                 =   MultWidth_f - 2 - 2*(i - num_allapp)
                        configInfo_list[i]["LUT_c"]                     =   2*(i - num_allapp)
                        configInfo_list[i]["ifLUT_e_app"]               =   0
                        configInfo_list[i]["ifLUT_b_app"]               =   0
                    else:
                        configInfo_list[i]["LUT_c_app"]                 =   MultWidth_f - 1 - 2*(i - num_allapp)
                        configInfo_list[i]["LUT_c"]                     =   2*(i - num_allapp) - 1
                        configInfo_list[i]["ifLUT_e_app"]               =   0
                        configInfo_list[i]["ifLUT_b_app"]               =   0
        else:
            if (num_noapp != 0) or ((num_noapp == 0) and (i != num_app-1)):
                if AppBits == MultWidth_f - 1:
                    configInfo_list[i]["LUT_a_app"]                 =   AppBits - 1
                    configInfo_list[i]["LUT_a"]                     =   0
                    configInfo_list[i]["ifLUT_c_app"]               =   1
                    configInfo_list[i]["ifLUT_d_app"]               =   0
                else:
                    configInfo_list[i]["LUT_a_app"]                 =   AppBits - 2*i
                    configInfo_list[i]["LUT_a"]                     =   MultWidth_f - AppBits + 2*i - 2
                    configInfo_list[i]["ifLUT_c_app"]               =   0
                    configInfo_list[i]["ifLUT_d_app"]               =   0
            else:  # if num_noapp is 0, last layer should also be approximate type
                configInfo_list[i]["LUT_c_app"]                 =   AppBits - 2*i
                configInfo_list[i]["LUT_c"]                     =   MultWidth_f - AppBits + 2*i - 2
                configInfo_list[i]["ifLUT_e_app"]               =   0
                configInfo_list[i]["ifLUT_b_app"]               =   0 
    # print(configInfo_list)
    return configInfo_list

