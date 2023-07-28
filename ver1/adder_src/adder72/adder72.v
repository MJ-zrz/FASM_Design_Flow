`timescale 1ns/1ns
module adder72(
    input           [72:1]      A                 ,
    input           [72:1]      B                 ,
    input                       c0                ,
    output          [72:1]      S                 ,
    output                      c72               ,
    output                      sx                
);

    wire sx1, sx2, sx3;
    wire c24, c48;

    adder24 adder24_inst0(
        .A              (A[24:1]    )       ,
        .B              (B[24:1]    )       ,
        .c0             (c0         )       ,
        .S              (S[24:1]    )       ,
        .c24            (c24        )       ,
        .sx             (sx1        )       
    );

    adder24 adder24_inst1(
        .A              (A[48:25]   )       ,
        .B              (B[48:25]   )       ,
        .c0             (c24        )       ,
        .S              (S[48:25]   )       ,
        .c24            (c48        )       ,
        .sx             (sx2        )       
    );

    adder24 adder24_inst2(
        .A              (A[72:49]   )       ,
        .B              (B[72:49]   )       ,
        .c0             (c48        )       ,
        .S              (S[72:49]   )       ,
        .c24            (c72        )       ,
        .sx             (sx3        )       
    );

    CC3 CC3_inst(
        .c0             (c0             )       ,
        .s1             (sx1            )       ,
        .s2             (sx2            )       ,
        .s3             (sx3            )       ,
        .d1             (c0             )       ,
        .d2             (c24            )       ,
        .d3             (c48            )       ,
        .sx             (sx             )       ,
        .sum            ()                      ,
        .c1             ()                      ,
        .c2             ()                      ,
        .c3             (c72)                      
    );


endmodule


