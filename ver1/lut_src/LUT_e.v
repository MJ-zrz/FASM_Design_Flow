`timescale 1ns/1ns
module LUT_e(
    input           Am          ,
    input           B_low       ,
    input           Am_1        ,
    input           B_high      ,
    output          S           ,
    output          D           //           
);

   assign S = (!(Am & B_low)) ^ (!(Am_1 & B_high));
   assign D = !(Am & B_low);

endmodule // LUT_e

