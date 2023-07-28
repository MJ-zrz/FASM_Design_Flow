`timescale 1ns/1ns

module tb
#(parameter width1 = 16, width2 = 16)
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
        A = 'd11158;
        B = 'd31500;
        #1050
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = 'd19578;
        B = -'d19518;
        #1050
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = -'d26736;
        B = 'd26838;
        #1050
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = 'd10804;
        B = -'d9342;
        #1050
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = -'d17655;
        B = -'d29914;
        #1050
        mult_en = 1'b0;

        #10
        mult_en = 1'b1;
        A = -'d19476;
        B = -'d28554;
        #1050
        mult_en = 1'b0;

        $stop;
    end

    app_mult_signed16x16 app_mult_signed16x16_inst(
        .en             (mult_en        )            ,
        .A              (A              )            ,
        .B              (B              )            ,
        .cin            (cin            )            ,
        .sum            (sum            )            ,

        .sys_clk        (sys_clk        )            ,
        .sys_rst_n      (sys_rst_n      )               //
    );

endmodule

