'''
This is the main file of the multplier's design flow
For usage, please first write configuration information into config.json and then run main.py
config.json description:
    width: [A_width, B_width]
    signed: 1 -> signed multipliers
    app: 1 -> approximate multipliers (only support Baugh-Wooley multipliers now, and other types may be included in the future)
    appbits: from that bit position and below, approximation is introduced into partial product calculation stage
    type: only support "baugh-wooley" now, and other types may be included in the future
    combinatory: 1 -> combinatory multipliers; 0-> sequential multipliers (add registers after inputs and before outputs, and these are mainly used for CPD tests)

As for approximate multiplier design, users may choose different approximate modules
Users can search in codes for "self-selection" to find where to change selection of approximate module
Users can search in codes for "self-selection for simulating time"  to find where to change simulating time for each computation task
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
        Multiplier.copy_2inputAdderFiles()
        Multiplier.gen_topFile()
        Multiplier.gen_testbench()

