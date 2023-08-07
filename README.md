# HeFAMDesignFlow

Here is the description of HeFAMDesignFlow. We propose an automatic design flow for high-efficiency FPGA-based approximate multipliers which are noted as **HeFAMs**. 

## Usage

For usage, please first write configuration information into `/pycodes/config.json` and then run `/pycodes/main.py`. The format of configuration information is shown as, 

```json
{
  "width": [6, 6],
  "signed": [0],
  "app": [1],
  "apptype": [1, 1],
  "appbits": [4],
  "type": "baugh-wooley",
  "combinatory": [0]
}
```

## Description of Configuration Infomation

`"width"` refers to the bit widths of two operands. Value range: `width[0]` ≥ 4, `width[1]` ≥ 4, and `width[0]+width[1]` ≤ 72

`"signed"` decides an unsigned or signed multiplier. Value range: `signed` == 1 -> a signed multiplier; `signed` == 0 -> an unsigned multiplier

`"app"` decides an approximate or accurate multiplier. Value range: `app` == 1 -> an approximate multiplier; `app` == 0 -> an accurate multiplier

We have explored the design space of CU_typeA and CU_typeC approximate modules. After testing for 9 types of approximate modules named ranging from Dse-1 to Dse-9, we find Dse-1, Dse-2 and Dse-4 on the Pareto Frontier

`"apptype"` chooses the approximate module type of CU_typeA and CU_typeC which make up the majority of computing units in our proposed multipliers. Value range: `[0, 0]`  -> CU_typeA_dse1 and CU_typeC_dse1 (Dse-1 modules); `[1, 1]`  -> CU_typeA_dse2 and CU_typeC_dse2 (Dse-2 modules); `[2, 2]`  -> CU_typeA_dse4 and CU_typeC_dse4 (Dse-4 modules) . For the approximate modules of CU_typeB and CU_typeD, they are chosen automatically according to the approximation level of the approximate multiplier. If  `app` == 0, this item does not matter

`"appbits"` sets the approximation level of the approximate multiplier.  If  `app` == 0, this item does not matter

`"type"`: only support `"baugh-wooley"` now, and other multiplier types may be included in the future

`"combinatory"`: `combinatory` == 1 -> combinatory multipliers; `combinatory` == 0 -> sequential multipliers (add registers after inputs and before outputs, and these are mainly used for critical path delay tests). We only support combinatory or one-cycle multiplier design now, and other multiplier types may be included in the future

## Examples

Multiplication operation can be viewed as the shifting and accumulation of partial product groups. Both accurate and approximate multipliers comprise multiple stages, including the computation, reduction and final summation of partial products. 

### 1. Partial Product Computation

6×6 unsigned accurate multiplier:

<img src="Figures\acc_layer_unsigned6x6_00.png" alt="" style="height:350px;" />

6×6 signed accurate multiplier:

<img src="Figures\acc_layer_signed6x6_00.png" alt="" style="height:350px;" />

6×6 unsigned approximate multiplier:

<img src="Figures\app_layer_unsigned6x6_00.png" alt="" style="height:350px;" />

### 2. Partial Product Reduction

8x8 unsigned multiplier (suitable for both accurate and approximate type):

<img src="Figures\Fig7_00.png" alt="" style="height:135px;" />

<img src="Figures\8x8_dadda_00.png" alt="" style="height:250px;" />

### 3. Partial Product Final Summation

For final summation, the ripple carry adders with appropriate bit widths are selected automatically based on the bit widths of multiplier design. 

### 4. 16×24 App-25 Dse-1 signed approximate multiplier

The configuration information for the design of a 16×24 App-25 Dse-1 signed approximate multiplier is shown below.

```json
{
  "width": [16, 24],
  "signed": [1],
  "app": [1],
  "apptype": [0, 0],
  "appbits": [4],
  "type": "baugh-wooley",
  "combinatory": [0]
}
```

## Supplements

Users can search in codes for "self-selection for simulating time"  to find where to change simulating time for each computation task. 



