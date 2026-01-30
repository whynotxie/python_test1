module dff (
  input clk,
  input rst,
  input [7:0] d,
  output [7:0] q
);
reg [7:0] q_reg;

assign q = q_reg;

always @(posedge clk or posedge rst) begin
    if (rst) q_reg <= 0;
    else q_reg <= d;
end
endmodule // dff