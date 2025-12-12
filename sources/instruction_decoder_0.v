`timescale 1ns/1ps
module instruction_decoder_0(
    input wire [2:0] id,             // <--- NEW 3-bit ID
    input wire [4:0] instr_in,
    input wire cc_in,
    input wire instr_en,
    output reg cen, 
    output reg rst, 
    output reg oen, 
    output reg inc, 
    output reg rsel, 
    output reg rce,  
    output reg pc_mux_sel, 
    output reg [1:0] a_mux_sel, 
    output reg [1:0] b_mux_sel, 
    output reg push,
    output reg pop, 
    output reg src_sel,
    output reg stack_we,
    output reg stack_re,
    output reg out_ce
);
always @(*) begin : instruction_decoder_0
    // --------------------------------------
    // If ID != 000 → decoder is disabled
    // --------------------------------------
    if (id != 3'b000) begin
        rst         = 1'b0;
        out_ce      = 1'b0;
        rsel        = 1'b0; 
        rce         = 1'b0; 
        cen         = 1'b0; 
        stack_re    = 1'b0; 
        pop         = 1'b0;
        a_mux_sel   = 2'b10;
        b_mux_sel   = 2'b10;
        oen         = 1'b0; 
        pc_mux_sel  = 1'b0; 
        inc         = 1'b0; 
        src_sel     = 1'b0;
        push        = 1'b0;
        stack_we    = 1'b0;
    end
    // --------------------------------------
    // ID == 000 → normal decoder operation
    // --------------------------------------
    else begin
        casex({instr_in, cc_in, instr_en})
          7'bxxxxxx1 : begin   // Instruction Disable
              rst        = 1'b0;
              out_ce     = 1'b0;
              rsel       = 1'b0;
              rce        = 1'b0;
              cen        = 1'b0;
              stack_re   = 1'b0;
              pop        = 1'b0;
              a_mux_sel  = 2'b10;
              b_mux_sel  = 2'b10;
              oen        = 1'b1;
              pc_mux_sel = 1'b0;
              inc        = 1'b0;
              src_sel    = 1'b0;
              push       = 1'b0;
              stack_we   = 1'b0;
          end
          7'b00000x0 : begin   // RESET
              rst        = 1'b1;
              out_ce     = 1'b0;
              rsel       = 1'b0;
              rce        = 1'b1; 
              cen        = 1'b1;  
              stack_re   = 1'b0;
              pop        = 1'b0;
              a_mux_sel  = 2'b10;  
              b_mux_sel  = 2'b10;  
              oen        = 1'b1;  
              pc_mux_sel = 1'b0; 
              inc        = 1'b1; 
              src_sel    = 1'b0; 
              push       = 1'b0;
              stack_we   = 1'b0;
          end
          7'b00001x0 : begin   // FETCH PC
              rst         = 1'b0;
              out_ce      = 1'b0;
              rsel        = 1'b0; 
              rce         = 1'b1; 
              cen         = 1'b0; 
              stack_re    = 1'b0;
              pop         = 1'b0;
              a_mux_sel   = 2'b10; 
              b_mux_sel   = 2'b00;  
              oen         = 1'b1; 
              pc_mux_sel  = 1'b1; 
              inc         = 1'b1; 
              src_sel     = 1'b0;
              push        = 1'b0;
              stack_we    = 1'b0;
          end
          7'b00010x0 : begin   // FETCH R
              rst         = 1'b0;
              out_ce      = 1'b0;
              rsel        = 1'b0; 
              rce         = 1'b1; 
              cen         = 1'b0; 
              stack_re    = 1'b0;
              pop         = 1'b0;
              a_mux_sel   = 2'b01; 
              b_mux_sel   = 2'b10;  
              oen         = 1'b1; 
              pc_mux_sel  = 1'b1; 
              inc         = 1'b1; 
              src_sel     = 1'b0;
              push        = 1'b0;
              stack_we    = 1'b0;
          end
          7'b00011x0 : begin  // FETCH D
              rst         = 1'b0;
              out_ce      = 1'b0;
              rsel        = 1'b0; 
              rce         = 1'b1; 
              cen         = 1'b0;  
              stack_re    = 1'b0;
              pop         = 1'b0;
              a_mux_sel   = 2'b00; 
              b_mux_sel   = 2'b10;  
              oen         = 1'b1; 
              pc_mux_sel  = 1'b1; 
              inc         = 1'b1; 
              src_sel     = 1'b0;
              push        = 1'b0;
              stack_we    = 1'b0;
          end
          default : begin
              rst         = 1'b0;
              out_ce      = 1'b0;
              rsel        = 1'b0; 
              rce         = 1'b0; 
              cen         = 1'b0; 
              stack_re    = 1'b0; 
              pop         = 1'b0;
              a_mux_sel   = 2'b10;
              b_mux_sel   = 2'b10;
              oen         = 1'b0; 
              pc_mux_sel  = 1'b0; 
              inc         = 1'b0; 
              src_sel     = 1'b0;
              push        = 1'b0;
              stack_we    = 1'b0;
          end

        endcase
    end
end
endmodule
