`timescale 1ns/1ns
module acc_mult_unsigned<#width1>x<#width2>
#(parameter width1 = <#width1>, width2 = <#width2>)
(
    input   [width1-1 : 0]          A               ,
    input   [width2-1 : 0]          B               ,
    input                           cin             ,
    output  [width1+width2-1 : 0]   sum             
);

    // ########################## Definitions ##########################

    <wire sum>

    wire [width1+width2-1 : 0] vector0;
    wire [width1+width2-1 : 0] vector1;

    // ############################ Layers ############################

    <layer instantiation>

    // ######################### Dadda Tree #################################

    Dadda Dadda_inst(
	    <sum ports>
	    .vector0		(vector0    )				,
	    .vector1		(vector1    )				   //
    );

    // ########################### CLA Adder ############################

    wire [<#width5>:0] adder_S;
    adder<#width6> adder<#width6>_inst(
        .A              (vector0     )         ,
        .B              (vector1     )         ,
        .c0             (1'b0        )         ,
        .S              (adder_S     )         ,
        .c<#width6>            ()
    );

    // ########################### Outputs ############################

    assign sum = adder_S;

endmodule

