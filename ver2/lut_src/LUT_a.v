`timescale 1ns/1ns
module LUT_a(
    input           Am          ,
    input           B_low       ,
    input           Am_1        ,
    input           B_high      ,
    output          S           ,  // O6
    output          D              // O5          
);

   assign S = (Am & B_low) ^ (Am_1 & B_high);
   assign D = Am & B_low;

endmodule // LUT_a

