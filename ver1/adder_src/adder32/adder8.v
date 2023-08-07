`timescale 1ns/1ns
module adder8(
    input           [8:1]       A                   ,
    input           [8:1]       B                   ,  
    input                       c0                  ,
    output          [8:1]       S                   ,
    output                      c8                  
);

    wire c4;

    adder4 adder4_inst0(
        .A              (A[4:1]     )       ,
        .B              (B[4:1]     )       ,
        .c0             (c0         )       ,
        .S              (S[4:1]     )       ,
        .c4             (c4         )       
    );

    adder4 adder4_inst1(
        .A              (A[8:5]     )       ,
        .B              (B[8:5]     )       ,
        .c0             (c4         )       ,
        .S              (S[8:5]     )       ,
        .c4             (c8         )             
    );


endmodule

