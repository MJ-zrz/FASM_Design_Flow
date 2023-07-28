`timescale 1ns/1ns
module app_layer_signed16x2_common_2
#(parameter width1 = 16)
(
    input   signed  [width1-1 : 0]      A               ,
    input                               B_low           ,
    input                               B_high          ,
    input                               cin             ,
    output          [width1+1 : 0]      layer_sum       
);

    wire [19 : 0] S;
    wire [19 : 0] D;
    assign S[0] = D[0];
    assign S[width1] = D[width1];

    wire c_tmp_0;
	wire c_tmp_4;
	wire c_tmp_8;
	wire c_tmp_12;
	wire c_tmp_16;
	wire c_tmp_20;
	
    assign c_tmp_0 = cin;
    assign S[17] = 1'b0;
	assign D[17] = 1'b0;
	assign S[18] = 1'b0;
	assign D[18] = 1'b0;
	assign S[19] = 1'b0;
	assign D[19] = 1'b0;
	

    // #################### Look-up tables ########################

    LUT_a_app1 LUT_a_app1_inst0(
        .Am     (A[1]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[0]           )           ,
        .B_high (B_high         )           ,
        .S      (S[1]           )           ,
        .D      (D[1]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst1(
        .Am     (A[2]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[1]           )           ,
        .B_high (B_high         )           ,
        .S      (S[2]           )           ,
        .D      (D[2]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst2(
        .Am     (A[3]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[2]           )           ,
        .B_high (B_high         )           ,
        .S      (S[3]           )           ,
        .D      (D[3]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst3(
        .Am     (A[4]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[3]           )           ,
        .B_high (B_high         )           ,
        .S      (S[4]           )           ,
        .D      (D[4]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst4(
        .Am     (A[5]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[4]           )           ,
        .B_high (B_high         )           ,
        .S      (S[5]           )           ,
        .D      (D[5]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst5(
        .Am     (A[6]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[5]           )           ,
        .B_high (B_high         )           ,
        .S      (S[6]           )           ,
        .D      (D[6]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst6(
        .Am     (A[7]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[6]           )           ,
        .B_high (B_high         )           ,
        .S      (S[7]           )           ,
        .D      (D[7]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst7(
        .Am     (A[8]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[7]           )           ,
        .B_high (B_high         )           ,
        .S      (S[8]           )           ,
        .D      (D[8]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst8(
        .Am     (A[9]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[8]           )           ,
        .B_high (B_high         )           ,
        .S      (S[9]           )           ,
        .D      (D[9]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst9(
        .Am     (A[10]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[9]           )           ,
        .B_high (B_high         )           ,
        .S      (S[10]           )           ,
        .D      (D[10]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst10(
        .Am     (A[11]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[10]           )           ,
        .B_high (B_high         )           ,
        .S      (S[11]           )           ,
        .D      (D[11]           )           //  
    );
 
    LUT_a_app1 LUT_a_app1_inst11(
        .Am     (A[12]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[11]           )           ,
        .B_high (B_high         )           ,
        .S      (S[12]           )           ,
        .D      (D[12]           )           //  
    );
 
    LUT_a LUT_a_inst12(
        .Am     (A[13]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[12]           )           ,
        .B_high (B_high         )           ,
        .S      (S[13]           )           ,
        .D      (D[13]           )           //  
    );
 
    LUT_a LUT_a_inst13(
        .Am     (A[14]           )           ,
        .B_low  (B_low          )           ,
        .Am_1   (A[13]           )           ,
        .B_high (B_high         )           ,
        .S      (S[14]           )           ,
        .D      (D[14]           )           //  
    );
 
    LUT_c LUT_c_inst14(
        .Am     (A[14]           )           ,
        .B_low  (B_high          )           ,
        .Am_1   (A[15]           )           ,
        .B_high (B_low         )           ,
        .S      (S[15]           )           ,
        .D      (D[15]           )           //  
    );
 
    LUT_d LUT_d_inst15(
        .A0     (A[0]           )           ,
        .B_low  (B_low          )           ,
        .An_1   (A[15]           )           ,
        .B_high (B_high         )           ,
        .P_high (D[16]           )           ,
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
    CC4 CC4_inst_2(
        .c0             (c_tmp_8            )               ,
        .s1             (S[8]               )               ,
        .s2             (S[9]               )               ,
        .s3             (S[10]               )               ,
        .s4             (S[11]               )               ,
        .d1             (D[8]               )               ,
        .d2             (D[9]               )               ,
        .d3             (D[10]               )               ,
        .d4             (D[11]               )               ,
        .sx             ()                                  ,
        .sum            (layer_sum[11:8]     )               ,
        .c1             ()                                  ,
        .c2             ()                                  ,
        .c3             ()                                  ,
        .c4             (c_tmp_12            )               
    );
    CC4 CC4_inst_3(
        .c0             (c_tmp_12            )               ,
        .s1             (S[12]               )               ,
        .s2             (S[13]               )               ,
        .s3             (S[14]               )               ,
        .s4             (S[15]               )               ,
        .d1             (D[12]               )               ,
        .d2             (D[13]               )               ,
        .d3             (D[14]               )               ,
        .d4             (D[15]               )               ,
        .sx             ()                                  ,
        .sum            (layer_sum[15:12]     )               ,
        .c1             ()                                  ,
        .c2             ()                                  ,
        .c3             ()                                  ,
        .c4             (c_tmp_16            )               
    );
    CC4 CC4_inst_4(
        .c0             (c_tmp_16            )               ,
        .s1             (S[16]               )               ,
        .s2             (S[17]               )               ,
        .s3             (S[18]               )               ,
        .s4             (S[19]               )               ,
        .d1             (D[16]               )               ,
        .d2             (D[17]               )               ,
        .d3             (D[18]               )               ,
        .d4             (D[19]               )               ,
        .sx             ()                                  ,
        .sum            (layer_sum[17:16]     )               ,
        .c1             ()                                  ,
        .c2             ()                                  ,
        .c3             ()                                  ,
        .c4             (c_tmp_20            )               
    );


endmodule

