`timescale 1ns/1ns
module app_layer_unsigned<#width1>x2_<#width3>
#(parameter width1 = <#width1>)
(
    input   [width1-1 : 0]          A               ,
    input                           B_low           ,
    input                           B_high          ,
    input                           cin             ,
    output  [width1+1 : 0]          layer_sum       
);

    wire [<#width4> : 0] S;
    wire [<#width4> : 0] D;
    assign S[0] = D[0];
    assign S[width1] = D[width1];

    <c_tmp definition>
    assign c_tmp_0 = cin;
    <S_D assignment>

    // #################### Look-up tables ########################

    <LUT instantiation>
    // ################### Carry Chains #######################

    <CC4 instantiation>

endmodule

