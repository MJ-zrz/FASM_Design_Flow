`timescale 1ns/1ns

module tb
#(parameter width1 = <#width1>, width2 = <#width2>)
();

    reg sys_clk = 1'b1;
    reg sys_rst_n = 1'b0;

    reg mult_en = 1'b0;

    reg signed [width1-1 : 0] A = 'd0;
    reg signed [width2-1 : 0] B = 'd0;
    reg cin = 1'b0;
    wire signed [width1+width2-1 : 0] sum;

    always #5 sys_clk = ~sys_clk;

    initial begin
        #100
        sys_rst_n = 1'b1;
        cin = 1'b0;

        mult_en = 1'b1;
        A = 'd<#number1>;
        B = 'd<#number2>;
        #<#time>
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = 'd<#number3>;
        B = -'d<#number4>;
        #<#time>
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = -'d<#number5>;
        B = 'd<#number6>;
        #<#time>
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = 'd<#number7>;
        B = -'d<#number8>;
        #<#time>
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = -'d<#number9>;
        B = -'d<#number10>;
        #<#time>
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = -'d<#number11>;
        B = -'d<#number12>;
        #<#time>
        mult_en = 1'b0;

        $stop;
    end

    app_mult_signed<#width1>x<#width2> app_mult_signed<#width1>x<#width2>_inst(
        .en             (mult_en        )            ,
        .A              (A              )            ,
        .B              (B              )            ,
        .cin            (cin            )            ,
        .sum            (sum            )            ,

        .sys_clk        (sys_clk        )            ,
        .sys_rst_n      (sys_rst_n      )               //
    );

endmodule

