`timescale 1ns/1ns
module LUT_d_app2(
    input           A0          ,
    input           B_low       ,
    input           An_1        ,
    input           B_high      ,
    output          P_high      ,
    output          P_low       //             
);

   assign P_high = 1'b0;
   assign P_low = 1'b0;

endmodule // LUT_d_app2

