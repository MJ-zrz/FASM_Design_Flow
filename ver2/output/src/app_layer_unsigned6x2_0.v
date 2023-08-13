`timescale 1ns/1ns
module app_layer_unsigned6x2_0
#(parameter width1 = 6)
(
    input   [width1-1 : 0]          A               ,
    input                           B_low           ,
    input                           B_high          ,
    input                           cin             ,
    output  [width1+1 : 0]          layer_sum       
);

    wire [7 : 0] S;
    wire [7 : 0] D;
    assign S[0] = D[0];
    assign S[width1] = D[width1];

    wire c_tmp_0;
	wire c_tmp_4;
	wire c_tmp_8;
	
    assign c_tmp_0 = cin;
    assign S[7] = 1'b0;
	assign D[7] = 1'b0;
	

    // #################### Look-up tables ########################

    LUT_dse2 LUT_dse2_inst0(
        .Am     (A[1]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[0]           )           ,
        .B_high (B_high         )           ,
        .S      (S[1]           )           ,
        .D      (D[1]           )           //  
    );
 
    LUT_dse2 LUT_dse2_inst1(
        .Am     (A[2]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[1]           )           ,
        .B_high (B_high         )           ,
        .S      (S[2]           )           ,
        .D      (D[2]           )           //  
    );
 
    LUT_dse2 LUT_dse2_inst2(
        .Am     (A[3]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[2]           )           ,
        .B_high (B_high         )           ,
        .S      (S[3]           )           ,
        .D      (D[3]           )           //  
    );
 
    LUT_dse2 LUT_dse2_inst3(
        .Am     (A[4]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[3]           )           ,
        .B_high (B_high         )           ,
        .S      (S[4]           )           ,
        .D      (D[4]           )           //  
    );
 
    LUT_a LUT_a_inst4(
        .Am     (A[5]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[4]           )           ,
        .B_high (B_high         )           ,
        .S      (S[5]           )           ,
        .D      (D[5]           )           //  
    );
 
    LUT_b LUT_b_inst5(
        .A0     (A[0]           )           ,
        .B_low  (B_low          )           ,
        .An_1   (A[5]           )           ,
        .B_high (B_high         )           ,
        .P_high (D[6]           )           ,
        .P_low  (D[0]           )           //  
    );
  
    
    // ################### Carry Chains #######################

        CC4 CC4_inst_0(
        .c0             (c_tmp_0            )               ,
        .s1             (S[0]               )               ,
        .s2             (S[1]               )               ,
        .s3             (S[2]               )               ,
        .s4             (S[3]               )               ,
        .d1             (D[0]               )               ,
        .d2             (D[1]               )               ,
        .d3             (D[2]               )               ,
        .d4             (D[3]               )               ,
        .sx             ()                                  ,
        .sum            (layer_sum[3:0]     )               ,
        .c1             ()                                  ,
        .c2             ()                                  ,
        .c3             ()                                  ,
        .c4             (c_tmp_4            )               
    );
    CC4 CC4_inst_1(
        .c0             (c_tmp_4            )               ,
        .s1             (S[4]               )               ,
        .s2             (S[5]               )               ,
        .s3             (S[6]               )               ,
        .s4             (S[7]               )               ,
        .d1             (D[4]               )               ,
        .d2             (D[5]               )               ,
        .d3             (D[6]               )               ,
        .d4             (D[7]               )               ,
        .sx             ()                                  ,
        .sum            (layer_sum[7:4]     )               ,
        .c1             ()                                  ,
        .c2             ()                                  ,
        .c3             ()                                  ,
        .c4             (c_tmp_8            )               
    );


endmodule

