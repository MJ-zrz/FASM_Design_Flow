`timescale 1ns/1ns
module adder4(
    input       [4:1]       A                   ,
    input       [4:1]       B                   ,
    input                   c0                  ,
    output      [4:1]       S                   ,
    output                  c4                  
);

    wire s1, s2, s3, s4;
    assign s1 = A[1] ^ B[1];      
    assign s2 = A[2] ^ B[2];
    assign s3 = A[3] ^ B[3];
    assign s4 = A[4] ^ B[4];

    CC4 CC4_inst(
        .c0             (c0             )       ,
        .s1             (s1             )       ,
        .s2             (s2             )       ,
        .s3             (s3             )       ,
        .s4             (s4             )       ,
        .d1             (A[1]           )       ,
        .d2             (A[2]           )       ,
        .d3             (A[3]           )       ,
        .d4             (A[4]           )       ,
        .sx             ()       ,
        .sum            (S              )       ,
        .c1             ()                      ,
        .c2             ()                      ,
        .c3             ()                      ,
        .c4             (c4             )               
    );


endmodule

