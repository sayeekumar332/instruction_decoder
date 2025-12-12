`timescale 1ns/1ps
module instruction_decoder(
    input  wire [2:0] id,             
    input  wire [4:0] instr_in,
    input  wire       cc_in,
    input  wire       instr_en,
    output reg        cen, 
    output reg        rst, 
    output reg        oen, 
    output reg        inc, 
    output reg        rsel, 
    output reg        rce,  
    output reg        pc_mux_sel, 
    output reg [1:0]  a_mux_sel, 
    output reg [1:0]  b_mux_sel, 
    output reg        push,
    output reg        pop, 
    output reg        src_sel,
    output reg        stack_we,
    output reg        stack_re,
    output reg        out_ce
);

    // ----------------------------------------------------
    // Packed vectors for single-bit outputs (one bit per decoder)
    // ----------------------------------------------------
    wire [7:0] cen_w;
    wire [7:0] rst_w;
    wire [7:0] oen_w;
    wire [7:0] inc_w;
    wire [7:0] rsel_w;
    wire [7:0] rce_w;
    wire [7:0] pc_mux_sel_w;
    wire [7:0] push_w;
    wire [7:0] pop_w;
    wire [7:0] src_sel_w;
    wire [7:0] stack_re_w;
    wire [7:0] stack_we_w;
    wire [7:0] out_ce_w;

    // ----------------------------------------------------
    // two-bit buses: LSB and MSB per decoder
    // ----------------------------------------------------
    wire [7:0] a_mux_sel_w0; // bit0 for dec0..dec7 (LSB)
    wire [7:0] a_mux_sel_w1; // bit1 for dec0..dec7 (MSB)
    wire [7:0] b_mux_sel_w0;
    wire [7:0] b_mux_sel_w1;

    // ----------------------------------------------------
    // Instantiate all eight decoders
    // (Pass global id; connect 2-bit ports with explicit concatenation)
    // ----------------------------------------------------

    instruction_decoder_0 u_dec0(
        .id(id), .instr_in(instr_in), .cc_in(cc_in), .instr_en(instr_en),
        .cen(cen_w[0]), .rst(rst_w[0]), .oen(oen_w[0]), .inc(inc_w[0]),
        .rsel(rsel_w[0]), .rce(rce_w[0]), .pc_mux_sel(pc_mux_sel_w[0]),
        .a_mux_sel({a_mux_sel_w1[0], a_mux_sel_w0[0]}), .b_mux_sel({b_mux_sel_w1[0], b_mux_sel_w0[0]}),
        .push(push_w[0]), .pop(pop_w[0]), .src_sel(src_sel_w[0]),
        .stack_we(stack_we_w[0]), .stack_re(stack_re_w[0]), .out_ce(out_ce_w[0])
    );

    instruction_decoder_1 u_dec1(
        .id(id), .instr_in(instr_in), .cc_in(cc_in), .instr_en(instr_en),
        .cen(cen_w[1]), .rst(rst_w[1]), .oen(oen_w[1]), .inc(inc_w[1]),
        .rsel(rsel_w[1]), .rce(rce_w[1]), .pc_mux_sel(pc_mux_sel_w[1]),
        .a_mux_sel({a_mux_sel_w1[1], a_mux_sel_w0[1]}), .b_mux_sel({b_mux_sel_w1[1], b_mux_sel_w0[1]}),
        .push(push_w[1]), .pop(pop_w[1]), .src_sel(src_sel_w[1]),
        .stack_we(stack_we_w[1]), .stack_re(stack_re_w[1]), .out_ce(out_ce_w[1])
    );

    instruction_decoder_2 u_dec2(
        .id(id), .instr_in(instr_in), .cc_in(cc_in), .instr_en(instr_en),
        .cen(cen_w[2]), .rst(rst_w[2]), .oen(oen_w[2]), .inc(inc_w[2]),
        .rsel(rsel_w[2]), .rce(rce_w[2]), .pc_mux_sel(pc_mux_sel_w[2]),
        .a_mux_sel({a_mux_sel_w1[2], a_mux_sel_w0[2]}), .b_mux_sel({b_mux_sel_w1[2], b_mux_sel_w0[2]}),
        .push(push_w[2]), .pop(pop_w[2]), .src_sel(src_sel_w[2]),
        .stack_we(stack_we_w[2]), .stack_re(stack_re_w[2]), .out_ce(out_ce_w[2])
    );

    instruction_decoder_3 u_dec3(
        .id(id), .instr_in(instr_in), .cc_in(cc_in), .instr_en(instr_en),
        .cen(cen_w[3]), .rst(rst_w[3]), .oen(oen_w[3]), .inc(inc_w[3]),
        .rsel(rsel_w[3]), .rce(rce_w[3]), .pc_mux_sel(pc_mux_sel_w[3]),
        .a_mux_sel({a_mux_sel_w1[3], a_mux_sel_w0[3]}), .b_mux_sel({b_mux_sel_w1[3], b_mux_sel_w0[3]}),
        .push(push_w[3]), .pop(pop_w[3]), .src_sel(src_sel_w[3]),
        .stack_we(stack_we_w[3]), .stack_re(stack_re_w[3]), .out_ce(out_ce_w[3])
    );

    instruction_decoder_4 u_dec4(
        .id(id), .instr_in(instr_in), .cc_in(cc_in), .instr_en(instr_en),
        .cen(cen_w[4]), .rst(rst_w[4]), .oen(oen_w[4]), .inc(inc_w[4]),
        .rsel(rsel_w[4]), .rce(rce_w[4]), .pc_mux_sel(pc_mux_sel_w[4]),
        .a_mux_sel({a_mux_sel_w1[4], a_mux_sel_w0[4]}), .b_mux_sel({b_mux_sel_w1[4], b_mux_sel_w0[4]}),
        .push(push_w[4]), .pop(pop_w[4]), .src_sel(src_sel_w[4]),
        .stack_we(stack_we_w[4]), .stack_re(stack_re_w[4]), .out_ce(out_ce_w[4])
    );

    instruction_decoder_5 u_dec5(
        .id(id), .instr_in(instr_in), .cc_in(cc_in), .instr_en(instr_en),
        .cen(cen_w[5]), .rst(rst_w[5]), .oen(oen_w[5]), .inc(inc_w[5]),
        .rsel(rsel_w[5]), .rce(rce_w[5]), .pc_mux_sel(pc_mux_sel_w[5]),
        .a_mux_sel({a_mux_sel_w1[5], a_mux_sel_w0[5]}), .b_mux_sel({b_mux_sel_w1[5], b_mux_sel_w0[5]}),
        .push(push_w[5]), .pop(pop_w[5]), .src_sel(src_sel_w[5]),
        .stack_we(stack_we_w[5]), .stack_re(stack_re_w[5]), .out_ce(out_ce_w[5])
    );

    instruction_decoder_6 u_dec6(
        .id(id), .instr_in(instr_in), .cc_in(cc_in), .instr_en(instr_en),
        .cen(cen_w[6]), .rst(rst_w[6]), .oen(oen_w[6]), .inc(inc_w[6]),
        .rsel(rsel_w[6]), .rce(rce_w[6]), .pc_mux_sel(pc_mux_sel_w[6]),
        .a_mux_sel({a_mux_sel_w1[6], a_mux_sel_w0[6]}), .b_mux_sel({b_mux_sel_w1[6], b_mux_sel_w0[6]}),
        .push(push_w[6]), .pop(pop_w[6]), .src_sel(src_sel_w[6]),
        .stack_we(stack_we_w[6]), .stack_re(stack_re_w[6]), .out_ce(out_ce_w[6])
    );

    instruction_decoder_7 u_dec7(
        .id(id), .instr_in(instr_in), .cc_in(cc_in), .instr_en(instr_en),
        .cen(cen_w[7]), .rst(rst_w[7]), .oen(oen_w[7]), .inc(inc_w[7]),
        .rsel(rsel_w[7]), .rce(rce_w[7]), .pc_mux_sel(pc_mux_sel_w[7]),
        .a_mux_sel({a_mux_sel_w1[7], a_mux_sel_w0[7]}), .b_mux_sel({b_mux_sel_w1[7], b_mux_sel_w0[7]}),
        .push(push_w[7]), .pop(pop_w[7]), .src_sel(src_sel_w[7]),
        .stack_we(stack_we_w[7]), .stack_re(stack_re_w[7]), .out_ce(out_ce_w[7])
    );

    // ----------------------------------------------------
    // Output selection mux (explicit case — avoids vector-variable-index quirks)
    // ----------------------------------------------------
    always @(*) begin
        // default safe values in case of unexpected id
        cen        = 1'b0;
        rst        = 1'b0;
        oen        = 1'b0;
        inc        = 1'b0;
        rsel       = 1'b0;
        rce        = 1'b0;
        pc_mux_sel = 1'b0;
        a_mux_sel  = 2'b00;
        b_mux_sel  = 2'b00;
        push       = 1'b0;
        pop        = 1'b0;
        src_sel    = 1'b0;
        stack_we   = 1'b0;
        stack_re   = 1'b0;
        out_ce     = 1'b0;

        case (id)
            3'd0: begin
                cen        = cen_w[0];
                rst        = rst_w[0];
                oen        = oen_w[0];
                inc        = inc_w[0];
                rsel       = rsel_w[0];
                rce        = rce_w[0];
                pc_mux_sel = pc_mux_sel_w[0];
                a_mux_sel  = {a_mux_sel_w1[0], a_mux_sel_w0[0]};
                b_mux_sel  = {b_mux_sel_w1[0], b_mux_sel_w0[0]};
                push       = push_w[0];
                pop        = pop_w[0];
                src_sel    = src_sel_w[0];
                stack_we   = stack_we_w[0];
                stack_re   = stack_re_w[0];
                out_ce     = out_ce_w[0];
            end
            3'd1: begin
                cen        = cen_w[1];
                rst        = rst_w[1];
                oen        = oen_w[1];
                inc        = inc_w[1];
                rsel       = rsel_w[1];
                rce        = rce_w[1];
                pc_mux_sel = pc_mux_sel_w[1];
                a_mux_sel  = {a_mux_sel_w1[1], a_mux_sel_w0[1]};
                b_mux_sel  = {b_mux_sel_w1[1], b_mux_sel_w0[1]};
                push       = push_w[1];
                pop        = pop_w[1];
                src_sel    = src_sel_w[1];
                stack_we   = stack_we_w[1];
                stack_re   = stack_re_w[1];
                out_ce     = out_ce_w[1];
            end
            3'd2: begin
                cen        = cen_w[2];
                rst        = rst_w[2];
                oen        = oen_w[2];
                inc        = inc_w[2];
                rsel       = rsel_w[2];
                rce        = rce_w[2];
                pc_mux_sel = pc_mux_sel_w[2];
                a_mux_sel  = {a_mux_sel_w1[2], a_mux_sel_w0[2]};
                b_mux_sel  = {b_mux_sel_w1[2], b_mux_sel_w0[2]};
                push       = push_w[2];
                pop        = pop_w[2];
                src_sel    = src_sel_w[2];
                stack_we   = stack_we_w[2];
                stack_re   = stack_re_w[2];
                out_ce     = out_ce_w[2];
            end
            3'd3: begin
                cen        = cen_w[3];
                rst        = rst_w[3];
                oen        = oen_w[3];
                inc        = inc_w[3];
                rsel       = rsel_w[3];
                rce        = rce_w[3];
                pc_mux_sel = pc_mux_sel_w[3];
                a_mux_sel  = {a_mux_sel_w1[3], a_mux_sel_w0[3]};
                b_mux_sel  = {b_mux_sel_w1[3], b_mux_sel_w0[3]};
                push       = push_w[3];
                pop        = pop_w[3];
                src_sel    = src_sel_w[3];
                stack_we   = stack_we_w[3];
                stack_re   = stack_re_w[3];
                out_ce     = out_ce_w[3];
            end
            3'd4: begin
                cen        = cen_w[4];
                rst        = rst_w[4];
                oen        = oen_w[4];
                inc        = inc_w[4];
                rsel       = rsel_w[4];
                rce        = rce_w[4];
                pc_mux_sel = pc_mux_sel_w[4];
                a_mux_sel  = {a_mux_sel_w1[4], a_mux_sel_w0[4]};
                b_mux_sel  = {b_mux_sel_w1[4], b_mux_sel_w0[4]};
                push       = push_w[4];
                pop        = pop_w[4];
                src_sel    = src_sel_w[4];
                stack_we   = stack_we_w[4];
                stack_re   = stack_re_w[4];
                out_ce     = out_ce_w[4];
            end
            3'd5: begin
                cen        = cen_w[5];
                rst        = rst_w[5];
                oen        = oen_w[5];
                inc        = inc_w[5];
                rsel       = rsel_w[5];
                rce        = rce_w[5];
                pc_mux_sel = pc_mux_sel_w[5];
                a_mux_sel  = {a_mux_sel_w1[5], a_mux_sel_w0[5]};
                b_mux_sel  = {b_mux_sel_w1[5], b_mux_sel_w0[5]};
                push       = push_w[5];
                pop        = pop_w[5];
                src_sel    = src_sel_w[5];
                stack_we   = stack_we_w[5];
                stack_re   = stack_re_w[5];
                out_ce     = out_ce_w[5];
            end
            3'd6: begin
                cen        = cen_w[6];
                rst        = rst_w[6];
                oen        = oen_w[6];
                inc        = inc_w[6];
                rsel       = rsel_w[6];
                rce        = rce_w[6];
                pc_mux_sel = pc_mux_sel_w[6];
                a_mux_sel  = {a_mux_sel_w1[6], a_mux_sel_w0[6]};
                b_mux_sel  = {b_mux_sel_w1[6], b_mux_sel_w0[6]};
                push       = push_w[6];
                pop        = pop_w[6];
                src_sel    = src_sel_w[6];
                stack_we   = stack_we_w[6];
                stack_re   = stack_re_w[6];
                out_ce     = out_ce_w[6];
            end
            3'd7: begin
                cen        = cen_w[7];
                rst        = rst_w[7];
                oen        = oen_w[7];
                inc        = inc_w[7];
                rsel       = rsel_w[7];
                rce        = rce_w[7];
                pc_mux_sel = pc_mux_sel_w[7];
                a_mux_sel  = {a_mux_sel_w1[7], a_mux_sel_w0[7]};
                b_mux_sel  = {b_mux_sel_w1[7], b_mux_sel_w0[7]};
                push       = push_w[7];
                pop        = pop_w[7];
                src_sel    = src_sel_w[7];
                stack_we   = stack_we_w[7];
                stack_re   = stack_re_w[7];
                out_ce     = out_ce_w[7];
            end
            default: begin
                // already defaulted above; keep safe zeros
            end
        endcase
    end

endmodule

