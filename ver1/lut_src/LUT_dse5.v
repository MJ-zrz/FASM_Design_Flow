`timescale 1ns/1ns
module LUT_dse5(
    input           Am          ,
    input           B_low       ,
    input           Am_1        ,
    input           B_high      ,
    output          S           ,
    output          D           //           
);

	assign D = Am;
	assign S = Am_1 & B_high;

endmodule // LUT_dse5

