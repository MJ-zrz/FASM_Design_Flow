LUT_b LUT_b_inst<#width1>(
        .A0     (A[0]           )           ,
        .B_low  (B_low          )           ,
        .An_1   (A[<#width1>]           )           ,
        .B_high (B_high         )           ,
        .P_high (D[<#width2>]           )           ,
        .P_low  (D[0]           )           //  
    );
  
    