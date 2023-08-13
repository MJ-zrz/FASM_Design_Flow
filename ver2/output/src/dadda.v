`timescale 1ns/1ns
module Dadda#(
	parameter	InputWidth 		= 	8				,
	parameter 	OutputWidth 	= 	12
)
(
	input				[InputWidth-1 : 0]				sum0				,
	input				[InputWidth-1 : 0]				sum1				,
	input				[InputWidth-1 : 0]				sum2				,
	

	output				[OutputWidth-1 : 0]						vector0							,
	output				[OutputWidth-1 : 0]						vector1							   //
);

	wire		[0:0]				sum_column0				;
	wire		[0:0]				sum_column1				;
	wire		[1:0]				sum_column2				;
	wire		[1:0]				sum_column3				;
	wire		[2:0]				sum_column4				;
	wire		[2:0]				sum_column5				;
	wire		[2:0]				sum_column6				;
	wire		[2:0]				sum_column7				;
	wire		[1:0]				sum_column8				;
	wire		[1:0]				sum_column9				;
	wire		[0:0]				sum_column10				;
	wire		[0:0]				sum_column11				;


	wire		sum_column4_3				;
	wire		sum_column5_3				;
	wire		sum_column5_4				;
	wire		sum_column6_3				;
	wire		sum_column6_4				;
	wire		sum_column7_3				;
	wire		sum_column7_4				;
	wire		sum_column8_2				;
	wire		sum_column8_3				;
	wire		sum_column9_2				;
	wire		sum_column9_3				;
	wire		sum_column10_1				;
	

	assign		sum_column0				=		{sum0[0]}				;
	assign		sum_column1				=		{sum0[1]}				;
	assign		sum_column2				=		{sum0[2], sum1[0]}				;
	assign		sum_column3				=		{sum0[3], sum1[1]}				;
	assign		sum_column4				=		{sum0[4], sum1[2], sum2[0]}				;
	assign		sum_column5				=		{sum0[5], sum1[3], sum2[1]}				;
	assign		sum_column6				=		{sum0[6], sum1[4], sum2[2]}				;
	assign		sum_column7				=		{sum0[7], sum1[5], sum2[3]}				;
	assign		sum_column8				=		{sum1[6], sum2[4]}				;
	assign		sum_column9				=		{sum1[7], sum2[5]}				;
	assign		sum_column10				=		{sum2[6]}				;
	assign		sum_column11				=		{sum2[7]}				;
	

	
    HA HA_inst_0(
        .A              (sum_column4[0])            ,
        .B              (sum_column4[1])            ,
        .sum            (sum_column4_3)            ,
        .carry          (sum_column5_3)               //           
    );   
    
    FA FA_inst_1(
        .A              (sum_column5[0])            ,
        .B              (sum_column5[1])            ,
        .Cin            (sum_column5[2])            ,
        .sum            (sum_column5_4)            ,
        .carry          (sum_column6_3)               //           
    );    
    
    FA FA_inst_2(
        .A              (sum_column6[0])            ,
        .B              (sum_column6[1])            ,
        .Cin            (sum_column6[2])            ,
        .sum            (sum_column6_4)            ,
        .carry          (sum_column7_3)               //           
    );    
    
    FA FA_inst_3(
        .A              (sum_column7[0])            ,
        .B              (sum_column7[1])            ,
        .Cin            (sum_column7[2])            ,
        .sum            (sum_column7_4)            ,
        .carry          (sum_column8_2)               //           
    );    
    
    HA HA_inst_4(
        .A              (sum_column8[0])            ,
        .B              (sum_column8[1])            ,
        .sum            (sum_column8_3)            ,
        .carry          (sum_column9_2)               //           
    );   
    
    HA HA_inst_5(
        .A              (sum_column9[0])            ,
        .B              (sum_column9[1])            ,
        .sum            (sum_column9_3)            ,
        .carry          (sum_column10_1)               //           
    );   
    

	assign vector0 = {
        1'b0							,				
		sum_column10[0]				,				
		sum_column9_2				,				
		sum_column8_2				,				
		sum_column7_3				,				
		sum_column6_3				,				
		sum_column5_3				,				
		sum_column4[2]				,				
		sum_column3[0]				,				
		sum_column2[0]				,				
		sum_column1[0]				,				
		sum_column0[0]								

    };
    assign vector1 = {
        sum_column11[0]				,				
		sum_column10_1				,				
		sum_column9_3				,				
		sum_column8_3				,				
		sum_column7_4				,				
		sum_column6_4				,				
		sum_column5_4				,				
		sum_column4_3				,				
		sum_column3[1]				,				
		sum_column2[1]				,				
		1'b0						,				
		1'b0										

    };

    

endmodule

