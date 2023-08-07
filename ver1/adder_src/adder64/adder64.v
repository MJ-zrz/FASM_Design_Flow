`timescale 1ns/1ns
module adder64(
    input           [64:1]      A                 ,
    input           [64:1]      B                 ,
    input                       c0                ,
    output          [64:1]      S                 ,
    output                      c64               
);

    wire c16, c32, c48;

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

    adder16 adder16_inst3(
        .A              (A[64:49]   )       ,
        .B              (B[64:49]   )       ,
        .c0             (c48        )       ,
        .S              (S[64:49]   )       ,
        .c16            (c64        ) 
    );


endmodule


