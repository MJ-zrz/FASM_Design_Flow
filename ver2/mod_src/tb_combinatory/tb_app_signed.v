`timescale 1ns/1ns

module tb
#(parameter width1 = <#width1>, width2 = <#width2>)
();

    reg signed [width1-1 : 0] A = 'd0;
    reg signed [width2-1 : 0] B = 'd0;
    reg cin = 1'b0;
    wire signed [width1+width2-1 : 0] sum;

    initial begin
        #100
        cin = 1'b0;

        A = 'd<#number1>;
        B = 'd<#number2>;
        #<#time>

        #10
        A = 'd<#number3>;
        B = -'d<#number4>;
        #<#time>

        #10
        A = -'d<#number5>;
        B = 'd<#number6>;
        #<#time>

        #10
        A = 'd<#number7>;
        B = -'d<#number8>;
        #<#time>

        #10
        A = -'d<#number9>;
        B = -'d<#number10>;
        #<#time>

        #10
        A = -'d<#number11>;
        B = -'d<#number12>;
        #<#time>

        $stop;
    end

    app_mult_signed<#width1>x<#width2> app_mult_signed<#width1>x<#width2>_inst(
        .A              (A              )            ,
        .B              (B              )            ,
        .cin            (cin            )            ,
        .sum            (sum            )            
    );

endmodule

