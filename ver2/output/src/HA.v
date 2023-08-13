`timescale 1ns/1ns
module HA(
    input           A            ,
    input           B            ,
    output          sum          ,
    output          carry           //           
);

   assign sum = A ^ B;
   assign carry = A & B;

endmodule // HA

