`timescale 1ns/1ns
module CC4(
    input               c0                  ,
    input               s1                  ,
    input               s2                  ,
    input               s3                  ,
    input               s4                  ,
    input               d1                  ,
    input               d2                  ,
    input               d3                  ,
    input               d4                  ,

    output              sx                  ,
    output [3:0]        sum                 ,
    output              c1                  ,
    output              c2                  ,
    output              c3                  ,
    output              c4                     //        
);

//   CARRY4    : In order to incorporate this function into the design,
//   Verilog   : the following instance declaration needs to be placed
//  instance   : in the body of the design code.  The instance name
// declaration : (CARRY4_inst) and/or the port declarations within the
//    code     : parenthesis may be changed to properly reference and
//             : connect this function to the design. All inputs and
//             : and outputs of this primitive should be connected.

//  <-----Cut code below this line---->

   // CARRY4: Fast Carry Logic Component
   //         Artix-7
   // Xilinx HDL Language Template, version 2019.2

   CARRY4 CARRY4_inst (
      .CO({c4, c3, c2, c1}),         // 4-bit carry out
      .O(sum),           // 4-bit carry chain XOR data out
      .CI(c0),         // 1-bit carry cascade input
      .CYINIT(1'b0), // 1-bit carry initialization
      .DI({d4, d3, d2, d1}),         // 4-bit carry-MUX data in
      .S({s4, s3, s2, s1})            // 4-bit carry-MUX select input
   );

   // End of CARRY4_inst instantiation
				
    assign sx = s4 & s3 & s2 & s1;

endmodule

