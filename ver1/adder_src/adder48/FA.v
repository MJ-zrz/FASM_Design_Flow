`timescale 1ns/1ns
module FA(
    input           A            ,
    input           B            ,
    input           Cin          ,
    output          sum          ,
    output          carry           //           
);

   // ################################ Outputs ##################################

   assign sum = A ^ B ^ Cin;
   assign carry = (A ^ B) & Cin | (A & B);

endmodule // FA

