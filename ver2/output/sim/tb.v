`timescale 1ns/1ns

module tb
#(parameter width1 = 6, width2 = 6)
();

    reg sys_clk = 1'b1;
    reg sys_rst_n = 1'b0;

    reg mult_en = 1'b0;

    reg [width1-1 : 0] A = 'd0;
    reg [width2-1 : 0] B = 'd0;
    reg cin = 1'b0;
    wire [width1+width2-1 : 0] sum;

    always #5 sys_clk = ~sys_clk;

    initial begin
        #100
        sys_rst_n = 1'b1;
        cin = 1'b0;

        mult_en = 1'b1;
        A = 'd10;
        B = 'd22;
        #600
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = 'd31;
        B = -'d16;
        #600
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = -'d19;
        B = 'd19;
        #600
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = 'd11;
        B = -'d26;
        #600
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = -'d15;
        B = -'d13;
        #600
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = -'d18;
        B = -'d11;
        #600
        mult_en = 1'b0;

        $stop;
    end

    app_mult_unsigned6x6 app_mult_unsigned6x6_inst(
        .en             (mult_en        )            ,
        .A              (A              )            ,
        .B              (B              )            ,
        .cin            (cin            )            ,
        .sum            (sum            )            ,

        .sys_clk        (sys_clk        )            ,
        .sys_rst_n      (sys_rst_n      )               //
    );

endmodule

