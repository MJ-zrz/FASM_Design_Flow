`timescale 1ns/1ns
module adder32(
    input           [32:1]      A                 ,
    input           [32:1]      B                 ,
    input                       c0                ,
    output          [32:1]      S                 ,
    output                      c32               ,
    output                      sx                
);

    wire sx1, sx2, sx3, sx4;
    wire c8, c16, c24;

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

    adder8 adder8_inst3(
        .A              (A[32:25]   )       ,
        .B              (B[32:25]   )       ,
        .c0             (c24        )       ,
        .S              (S[32:25]   )       ,
        .c8             ()       ,
        .sx             (sx4        )       
    );

    CC4 CC4_inst(
        .c0             (c0             )       ,
        .s1             (sx1            )       ,
        .s2             (sx2            )       ,
        .s3             (sx3            )       ,
        .s4             (sx4            )       ,
        .d1             (c0             )       ,
        .d2             (c8             )       ,
        .d3             (c16            )       ,
        .d4             (c24            )       ,
        .sx             (sx             )       ,
        .sum            ()                      ,
        .c1             ()                      ,
        .c2             ()                      ,
        .c3             ()                      ,
        .c4             (c32            )               
    );

endmodule


