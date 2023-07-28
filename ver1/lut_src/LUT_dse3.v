`timescale 1ns/1ns
module LUT_dse3(
    input           Am          ,
    input           B_low       ,
    input           Am_1        ,
    input           B_high      ,
    output          S           ,
    output          D           //           
);

	assign D = B_low;
	assign S = 1'b0;

endmodule // LUT__dse3

