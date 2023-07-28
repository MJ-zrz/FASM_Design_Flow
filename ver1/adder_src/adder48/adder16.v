`timescale 1ns/1ns
module adder16(
    input           [16:1]      A                 ,
    input           [16:1]      B                 ,
    input                       c0                ,
    output          [16:1]      S                 ,
    output                      c16               ,
    output                      sx                
);

    wire sx1, sx2, sx3, sx4;
    wire c4, c8, c12;

    adder4 adder4_inst0(
        .A              (A[4:1]     )       ,
        .B              (B[4:1]     )       ,
        .c0             (c0         )       ,
        .S              (S[4:1]     )       ,
        .c4             (c4         )       ,
        .sx             (sx1        )       
    );

    adder4 adder4_inst1(
        .A              (A[8:5]     )       ,
        .B              (B[8:5]     )       ,
        .c0             (c4         )       ,
        .S              (S[8:5]     )       ,
        .c4             (c8         )       ,
        .sx             (sx2        )       
    );

    adder4 adder4_inst2(
        .A              (A[12:9]    )       ,
        .B              (B[12:9]    )       ,
        .c0             (c8         )       ,
        .S              (S[12:9]    )       ,
        .c4             (c12        )       ,
        .sx             (sx3        )         
    );

    adder4 adder4_inst3(
        .A              (A[16:13]   )       ,
        .B              (B[16:13]   )       ,
        .c0             (c12        )       ,
        .S              (S[16:13]   )       ,
        .c4             ()       ,
        .sx             (sx4        )          
    );

    CC4 CC4_inst(
        .c0             (c0             )       ,
        .s1             (sx1            )       ,
        .s2             (sx2            )       ,
        .s3             (sx3            )       ,
        .s4             (sx4            )       ,
        .d1             (c0             )       ,
        .d2             (c4             )       ,
        .d3             (c8             )       ,
        .d4             (c12            )       ,
        .sx             (sx             )       ,
        .sum            ()                      ,
        .c1             ()                      ,
        .c2             ()                      ,
        .c3             ()                      ,
        .c4             (c16            )               
    );

endmodule

