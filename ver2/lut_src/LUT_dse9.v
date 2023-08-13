`timescale 1ns/1ns
module LUT_dse9(
    input           Am          ,
    input           B_low       ,
    input           Am_1        ,
    input           B_high      ,
    output          S           ,
    output          D           //           
);

	assign D = B_low;
	assign S = (Am & B_low) ^ (Am_1 & B_high);

endmodule // LUT_dse9

