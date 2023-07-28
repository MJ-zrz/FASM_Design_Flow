`timescale 1ns/1ns
module Dadda#(
	parameter	InputWidth 		= 	<#width1>				,
	parameter 	OutputWidth 	= 	<#width2>
)
(
	<input definition>
	output				[OutputWidth-1 : 0]						vector0							,
	output				[OutputWidth-1 : 0]						vector1							   //
);

	<sum_column signal definition>

	<mid signal assignment>

	<sum_column signal assignment>

	<HA & FA>

	<vector assignment>

endmodule

