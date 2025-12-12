`timescale 1ns/1ps
module instruction_decoder_1(
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
always @(*) begin : instruction_decoder
    // --------------------------------------
    // If ID != 001 → decoder is disabled
    // --------------------------------------
    if (id != 3'b001) begin
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
    // ID == 001 → normal decoder operation
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
          7'b00100x0 : begin  // Fetch R + D
                     rst         = 1'b0;
                     out_ce      = 1'b0;
                     rsel        = 1'b0; 
                     rce         = 1'b1; 
                     cen         = 1'b1;  
                     stack_re    = 1'b0;
                     pop         = 1'b0;
                     a_mux_sel   = 2'b00; 
                     b_mux_sel   = 2'b11;  
                     oen         = 1'b1; 
                     pc_mux_sel  = 1'b1; 
                     inc         = 1'b1; 
                     src_sel     = 1'b0;
                     push        = 1'b0;
                     stack_we    = 1'b0;
                  end
     7'b00101x0 : begin // Fetch PC + D
                     rst         = 1'b0;
                     out_ce      = 1'b0;
                     rsel        = 1'b0; 
                     rce         = 1'b1; 
                     cen         = 1'b1; 
                     stack_re    = 1'b0;
                     pop         = 1'b0;
                     a_mux_sel   = 2'b00; 
                     b_mux_sel   = 2'b00;  
                     oen         = 1'b1;  
                     pc_mux_sel  = 1'b1;  
                     inc         = 1'b1;  
                     src_sel     = 1'b0;
                     push        = 1'b0;
                     stack_we    = 1'b0;
                  end
     7'b00110x0 : begin  // Fetch PC + R
                     rst         = 1'b0;
                     out_ce      = 1'b0;
                     rsel        = 1'b0; 
                     rce         = 1'b1; 
                     cen         = 1'b1; 
                     stack_re    = 1'b0;
                     pop         = 1'b0;
                     a_mux_sel   = 2'b01; 
                     b_mux_sel   = 2'b00;  
                     oen         = 1'b1; 
                     pc_mux_sel  = 1'b1; 
                     inc         = 1'b1; 
                     src_sel     = 1'b0;
                     push        = 1'b0;
                     stack_we    = 1'b0;
                  end
     7'b00111x0 : begin // Fetch S + D
                     rst         = 1'b0;
                     out_ce      = 1'b0;
                     rsel        = 1'b0; 
                     rce         = 1'b1; 
                     cen         = 1'b1; 
                     stack_re    = 1'b1;
                     pop         = 1'b1;
                     a_mux_sel   = 2'b00; 
                     b_mux_sel   = 2'b01;  
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
