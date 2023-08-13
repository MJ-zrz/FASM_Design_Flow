`timescale 1ns/1ns
module app_mult_unsigned6x6
#(parameter width1 = 6, width2 = 6)
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

    wire [width1+1 : 0] sum0;
	wire [width1+1 : 0] sum1;
	wire [width1+1 : 0] sum2;
	

    wire [width1+width2-1 : 0] vector0;
    wire [width1+width2-1 : 0] vector1;

    reg [width1-1 : 0] A_reg;
    reg [width2-1 : 0] B_reg;
    reg [width1+width2-1 : 0] sum_reg;

    // ############################# Layers ############################

    app_layer_unsigned6x2_0 app_layer_unsigned6x2_inst0(
        .A              (A_reg              )           ,
        .B_low          (B_reg[0]          )           ,
        .B_high         (B_reg[1]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum0           )           //
    );   

    app_layer_unsigned6x2_1 app_layer_unsigned6x2_inst1(
        .A              (A_reg              )           ,
        .B_low          (B_reg[2]          )           ,
        .B_high         (B_reg[3]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum1           )           //
    );   

    app_layer_unsigned6x2_2 app_layer_unsigned6x2_inst2(
        .A              (A_reg              )           ,
        .B_low          (B_reg[4]          )           ,
        .B_high         (B_reg[5]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum2           )           //
    );   

    

    // ######################### Dadda Tree #################################

    Dadda Dadda_inst(
	    .sum0				(sum0		)				,
		.sum1				(sum1		)				,
		.sum2				(sum2		)				,
		

	    .vector0		(vector0    )				,
	    .vector1		(vector1    )				   //
    );

    // ########################### CLA Adder ############################

    wire [11:0] adder_S;
    adder12 adder12_inst(
        .A              (vector0     )         ,
        .B              (vector1     )         ,
        .c0             (1'b0        )         ,
        .S              (adder_S     )         ,
        .c12            ()       
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

