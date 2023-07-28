`timescale 1ns/1ns
module app_mult_signed16x16
#(parameter width1 = 16, width2 = 16)
(
    input   signed  [width1-1 : 0]              A               ,
    input   signed  [width2-1 : 0]              B               ,
    input                                       cin             ,
    output  signed  [width1+width2-1 : 0]       sum             ,

    input                                       sys_clk         ,
    input                                       sys_rst_n       ,
    input                                       en                 //

);

    // ########################## Definitions ##########################

    wire [width1+1 : 0] sum0;
	wire [width1+1 : 0] sum1;
	wire [width1+1 : 0] sum2;
	wire [width1+1 : 0] sum3;
	wire [width1+1 : 0] sum4;
	wire [width1+1 : 0] sum5;
	wire [width1+1 : 0] sum6;
	wire [width1+1 : 0] sum7;
	

    wire signed [width1+width2-1 : 0] vector0;
    wire signed [width1+width2-1 : 0] vector1;

    reg signed [width1-1 : 0] A_reg;
    reg signed [width2-1 : 0] B_reg;
    reg [width1+width2-1 : 0] sum_reg;

    // ############################# Layers ############################

    app_layer_signed16x2_common_0 app_layer_signed16x2_common_0_inst0(
        .A              (A_reg              )           ,
        .B_low          (B_reg[0]          )           ,
        .B_high         (B_reg[1]          )           ,
        .cin            (cin            )           ,
        .layer_sum      (sum0           )           //
    );   

    app_layer_signed16x2_common_1 app_layer_signed16x2_common_1_inst1(
        .A              (A_reg              )           ,
        .B_low          (B_reg[2]          )           ,
        .B_high         (B_reg[3]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum1           )           //
    );   

    app_layer_signed16x2_common_2 app_layer_signed16x2_common_2_inst2(
        .A              (A_reg              )           ,
        .B_low          (B_reg[4]          )           ,
        .B_high         (B_reg[5]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum2           )           //
    );   

    app_layer_signed16x2_common_3 app_layer_signed16x2_common_3_inst3(
        .A              (A_reg              )           ,
        .B_low          (B_reg[6]          )           ,
        .B_high         (B_reg[7]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum3           )           //
    );   

    app_layer_signed16x2_common_4 app_layer_signed16x2_common_4_inst4(
        .A              (A_reg              )           ,
        .B_low          (B_reg[8]          )           ,
        .B_high         (B_reg[9]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum4           )           //
    );   

    app_layer_signed16x2_common_5 app_layer_signed16x2_common_5_inst5(
        .A              (A_reg              )           ,
        .B_low          (B_reg[10]          )           ,
        .B_high         (B_reg[11]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum5           )           //
    );   

    app_layer_signed16x2_common_6 app_layer_signed16x2_common_6_inst6(
        .A              (A_reg              )           ,
        .B_low          (B_reg[12]          )           ,
        .B_high         (B_reg[13]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum6           )           //
    );   

    app_layer_signed16x2_last app_layer_signed16x2_last_inst7(
        .A              (A_reg              )           ,
        .B_low          (B_reg[14]          )           ,
        .B_high         (B_reg[15]          )           ,
        .cin            (1'b0           )           ,
        .layer_sum      (sum7           )           //
    );   

    

    // ######################### Dadda Tree #################################

    Dadda Dadda_inst(
	    .sum0				(sum0		)				,
		.sum1				(sum1		)				,
		.sum2				(sum2		)				,
		.sum3				(sum3		)				,
		.sum4				(sum4		)				,
		.sum5				(sum5		)				,
		.sum6				(sum6		)				,
		.sum7				(sum7		)				,
		

	    .vector0		(vector0    )				,
	    .vector1		(vector1    )				   //
    );

    // ########################### CLA Adder ############################

    wire [31:0] adder_S;
    adder32 adder32_inst(
        .A              (vector0     )         ,
        .B              (vector1     )         ,
        .c0             (1'b0        )         ,
        .S              (adder_S     )         ,
        .c32            ()   //
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

