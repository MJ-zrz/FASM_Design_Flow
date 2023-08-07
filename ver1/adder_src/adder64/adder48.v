`timescale 1ns/1ns
module adder48(
    input           [48:1]      A                 ,
    input           [48:1]      B                 ,
    input                       c0                ,
    output          [48:1]      S                 ,
    output                      c48                     
);

    wire c16, c32;

    adder16 adder16_inst0(
        .A              (A[16:1]    )       ,
        .B              (B[16:1]    )       ,
        .c0             (c0         )       ,
        .S              (S[16:1]    )       ,
        .c16            (c16        )       
    );

    adder16 adder16_inst1(
        .A              (A[32:17]   )       ,
        .B              (B[32:17]   )       ,
        .c0             (c16        )       ,
        .S              (S[32:17]   )       ,
        .c16            (c32        )            
    );

    adder16 adder16_inst2(
        .A              (A[48:33]   )       ,
        .B              (B[48:33]   )       ,
        .c0             (c32        )       ,
        .S              (S[48:33]   )       ,
        .c16            (c48        )       
    );


endmodule


