`timescale 1ns/1ns
module app_mult_unsigned<#width1>x<#width2>
#(parameter width1 = <#width1>, width2 = <#width2>)
(
    input   [width1-1 : 0]          A               ,
    input   [width2-1 : 0]          B               ,
    input                           cin             ,
    output  [width1+width2-1 : 0]   sum             ,

    input                           sys_clk         ,
    input                           sys_rst_n       ,
    input                           en                 //
);

    // ########################## Definitions ##########################

    <wire sum>

    wire [width1+width2-1 : 0] vector0;
    wire [width1+width2-1 : 0] vector1;

    reg [width1-1 : 0] A_reg;
    reg [width2-1 : 0] B_reg;
    reg [width1+width2-1 : 0] sum_reg;

    // ############################# Layers ############################

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

    // ###################### Sequential Logic #######################

    always @(posedge sys_clk or negedge sys_rst_n) begin
        if(!sys_rst_n || !en) begin
            A_reg <= 'd0;
            B_reg <= 'd0;
            sum_reg <= 'd0;
        end
        else begin
            A_reg <= A;
            B_reg <= B;
            sum_reg <= adder_S;
        end
    end

    // ########################### Outputs ############################

    assign sum = sum_reg;



endmodule

