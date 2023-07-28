`timescale 1ns/1ns
module adder24(
    input           [24:1]      A                 ,
    input           [24:1]      B                 ,
    input                       c0                ,
    output          [24:1]      S                 ,
    output                      c24               ,
    output                      sx                
);

    wire sx1, sx2, sx3;
    wire c8, c16;

    adder8 adder8_inst0(
        .A              (A[8:1]     )       ,
        .B              (B[8:1]     )       ,
        .c0             (c0         )       ,
        .S              (S[8:1]     )       ,
        .c8             (c8         )       ,
        .sx             (sx1        )       
    );

    adder8 adder8_inst1(
        .A              (A[16:9]    )       ,
        .B              (B[16:9]    )       ,
        .c0             (c8         )       ,
        .S              (S[16:9]    )       ,
        .c8             (c16        )       ,
        .sx             (sx2        )       
    );

    adder8 adder8_inst2(
        .A              (A[24:17]   )       ,
        .B              (B[24:17]   )       ,
        .c0             (c16        )       ,
        .S              (S[24:17]   )       ,
        .c8             (c24        )       ,
        .sx             (sx3        )       
    );

    CC3 CC3_inst(
        .c0             (c0             )       ,
        .s1             (sx1            )       ,
        .s2             (sx2            )       ,
        .s3             (sx3            )       ,
        .d1             (c0             )       ,
        .d2             (c8             )       ,
        .d3             (c16            )       ,
        .sx             (sx             )       ,
        .sum            ()                      ,
        .c1             ()                      ,
        .c2             ()                      ,
        .c3             (c24)                      
    );


endmodule
