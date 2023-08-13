'''
`"width"` refers to the bit widths of two operands. Value range: `width[0]` ≥ 4, `width[1]` ≥ 4, and `width[0]+width[1]` ≤ 72
`"signed"` decides an unsigned or signed multiplier. Value range: `signed` == 1 -> a signed multiplier; `signed` == 0 -> an unsigned multiplier
`"app"` decides an approximate or accurate multiplier. Value range: `app` == 1 -> an approximate multiplier; `app` == 0 -> an accurate multiplier
We have explored the design space of CU_typeA and CU_typeC approximate modules. After testing for 9 types of approximate modules named ranging from Dse-1 to Dse-9, we find Dse-1, Dse-2 and Dse-4 on the Pareto Frontier
`"apptype"` chooses the approximate module type of CU_typeA and CU_typeC which make up the majority of computing units in our proposed multipliers. Value range: `[0, 0]`  -> CU_typeA_dse1 and CU_typeC_dse1 (Dse-1 modules); `[1, 1]`  -> CU_typeA_dse2 and CU_typeC_dse2 (Dse-2 modules); `[2, 2]`  -> CU_typeA_dse4 and CU_typeC_dse4 (Dse-4 modules) . For the approximate modules of CU_typeB and CU_typeD, they are chosen automatically according to the approximation level of the approximate multiplier. If  `app` == 0, this item does not matter
`"appbits"` sets the approximation level of the approximate multiplier.  If  `app` == 0, this item does not matter
`"type"`: only support `"baugh-wooley"` now, and other multiplier types may be included in the future
`"combinatory"`: `combinatory` == 1 -> combinatory multipliers; `combinatory` == 0 -> sequential multipliers (add registers after inputs and before outputs, and these are mainly used for critical path delay tests). We only support combinatory or one-cycle multiplier design now, and other multiplier types may be included in the future
'''

from multiplier import *


if __name__ == "__main__":
    filepath = "./config.json"
    MultWidth, signed, useapp, AppBits, AppType, type, combinatory = readjson(filepath)
    if max(MultWidth) <= 2:
        print("Small multiplier modules' codes do not need this design flow.")
    else:
        Multiplier = Multiplier(MultWidth, signed, useapp, AppBits, AppType, type, combinatory)
        Multiplier.copy_underlyingFiles()
        Multiplier.gen_layerFiles()
        Multiplier.gen_adderTree()
        Multiplier.gen_2inputAdderFiles()
        Multiplier.gen_topFile()
        Multiplier.gen_testbench()

