`timescale 1ns/1ns
module LUT_a_app2(
    input           Am          ,
    input           B_low       ,
    input           Am_1        ,
    input           B_high      ,
    output          S           ,
    output          D           //           
);

	assign D = Am;
	assign S = 1'b0;

endmodule // LUT_a_app2

