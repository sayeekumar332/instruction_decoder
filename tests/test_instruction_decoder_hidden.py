import cocotb
from cocotb.triggers import Timer
import os
import random
from pathlib import Path
from cocotb_tools.runner import get_runner

# -------------------------------------------------------
# GLOBAL HELPER (visible to all testcases)
# -------------------------------------------------------
def safe(value):
    try:
        return int(value)
    except ValueError:
        raise AssertionError(f"X/Z detected on signal {value}")

# ---- Golden output helper ----
def expect(dut, expected):
    for sig, exp_val in expected.items():
        dut_val = safe(getattr(dut, sig).value)
        assert dut_val == exp_val, f"{sig}: expected={exp_val} got={dut_val}"

# -------------------------------------------------------
# MAIN DIRECTED TEST (NO EXHAUSTIVE TESTING)
# -------------------------------------------------------
@cocotb.test()
async def test_instruction_decoder_0(dut):

    dut.id.value = 0   # Enable decoder 0

    # --------------------------------------
    # 1. INSTRUCTION DISABLE  → instr_en = 1
    # --------------------------------------
    dut.instr_in.value = 5
    dut.cc_in.value = 0
    dut.instr_en.value = 1
    await Timer(1, "ns")

    expect(dut, dict(
        rst=0, out_ce=0, rsel=0, rce=0, cen=0,
        stack_re=0, pop=0,
        a_mux_sel=2, b_mux_sel=2,
        oen=1, pc_mux_sel=0, inc=0, src_sel=0,
        push=0, stack_we=0
    ))

    # --------------------------------------
    # 2. RESET (00000x0)
    # --------------------------------------
    dut.instr_in.value = 0b00000
    dut.cc_in.value = 0
    dut.instr_en.value = 0
    await Timer(1, "ns")

    expect(dut, dict(
        rst=1, out_ce=0, rsel=0, rce=1, cen=1,
        stack_re=0, pop=0,
        a_mux_sel=2, b_mux_sel=2,
        oen=1, pc_mux_sel=0, inc=1, src_sel=0,
        push=0, stack_we=0
    ))

    # --------------------------------------
    # 3. FETCH PC (00001x0)
    # --------------------------------------
    dut.instr_in.value = 0b00001
    dut.cc_in.value = 0
    dut.instr_en.value = 0
    await Timer(1, "ns")

    expect(dut, dict(
        rst=0, out_ce=0, rsel=0, rce=1, cen=0,
        stack_re=0, pop=0,
        a_mux_sel=2, b_mux_sel=0,
        oen=1, pc_mux_sel=1, inc=1, src_sel=0,
        push=0, stack_we=0
    ))

    # --------------------------------------
    # 4. FETCH R (00010x0)
    # --------------------------------------
    dut.instr_in.value = 0b00010
    dut.cc_in.value = 0
    dut.instr_en.value = 0
    await Timer(1, "ns")

    expect(dut, dict(
        rst=0, out_ce=0, rsel=0, rce=1, cen=0,
        stack_re=0, pop=0,
        a_mux_sel=1, b_mux_sel=2,
        oen=1, pc_mux_sel=1, inc=1, src_sel=0,
        push=0, stack_we=0
    ))

    # --------------------------------------
    # 5. FETCH D (00011x0)
    # --------------------------------------
    dut.instr_in.value = 0b00011
    dut.cc_in.value = 0
    dut.instr_en.value = 0
    await Timer(1, "ns")

    expect(dut, dict(
        rst=0, out_ce=0, rsel=0, rce=1, cen=0,
        stack_re=0, pop=0,
        a_mux_sel=0, b_mux_sel=2,
        oen=1, pc_mux_sel=1, inc=1, src_sel=0,
        push=0, stack_we=0
    ))

    # --------------------------------------
    # 6. DEFAULT CASE
    # --------------------------------------
    dut.instr_in.value = 0b10101
    dut.cc_in.value = 1
    dut.instr_en.value = 0
    await Timer(1, "ns")

    expect(dut, dict(
        rst=0, out_ce=0, rsel=0, rce=0, cen=0,
        stack_re=0, pop=0,
        a_mux_sel=2, b_mux_sel=2,
        oen=0, pc_mux_sel=0, inc=0, src_sel=0,
        push=0, stack_we=0
    ))

    cocotb.log.info("Directed test for instruction_decoder_0 PASSED!")

# ===============================================================
#  INSTRUCTION DECODER 1 — DIRECTED TESTCASES
#  Place these AFTER the instruction_decoder_0 test cases
# ===============================================================

@cocotb.test()
async def test_instruction_disable_dec1(dut):
    """Decoder 1: 7'bxxxxxx1 → Instruction Disable"""
    dut.id.value = 1
    dut.instr_in.value = 7
    dut.cc_in.value = 0
    dut.instr_en.value = 1

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 0
    assert safe(dut.rst.value) == 0
    assert safe(dut.rce.value) == 0
    assert safe(dut.stack_re.value) == 0
    assert safe(dut.pop.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 0
    cocotb.log.info("Decoder 1 — Instruction Disable case passed")


@cocotb.test()
async def test_fetch_R_D_dec1(dut):
    """Decoder 1: 7'b00100x0 → Fetch R + D"""
    dut.id.value = 1
    dut.instr_in.value = 0b00100
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 1
    assert safe(dut.rce.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 3
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 1 — Fetch R + D case passed")


@cocotb.test()
async def test_fetch_PC_D_dec1(dut):
    """Decoder 1: 7'b00101x0 → Fetch PC + D"""
    dut.id.value = 1
    dut.instr_in.value = 0b00101
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 1
    assert safe(dut.rce.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 1 — Fetch PC + D case passed")


@cocotb.test()
async def test_fetch_PC_R_dec1(dut):
    """Decoder 1: 7'b00110x0 → Fetch PC + R"""
    dut.id.value = 1
    dut.instr_in.value = 0b00110
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 1
    assert safe(dut.rce.value) == 1
    assert safe(dut.a_mux_sel.value) == 1
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 1 — Fetch PC + R case passed")


@cocotb.test()
async def test_fetch_S_D_dec1(dut):
    """Decoder 1: 7'b00111x0 → Fetch S + D"""
    dut.id.value = 1
    dut.instr_in.value = 0b00111
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 1
    assert safe(dut.rce.value) == 1
    assert safe(dut.stack_re.value) == 1
    assert safe(dut.pop.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 1
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 1 — Fetch S + D case passed")


@cocotb.test()
async def test_default_dec1(dut):
    """Decoder 1: DEFAULT case"""
    dut.id.value = 1
    dut.instr_in.value = 0b10101
    dut.cc_in.value = 1
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 0
    assert safe(dut.rce.value) == 0
    assert safe(dut.oen.value) == 0
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    cocotb.log.info("Decoder 1 — DEFAULT case passed")




# ===============================================================
#  INSTRUCTION DECODER 2 — DIRECTED TESTCASES
#  Place these AFTER the instruction_decoder_1 test cases
# ===============================================================


@cocotb.test()
async def test_instruction_disable_dec2(dut):
    """Decoder 2: 7'b0100011 → Instruction Disable"""
    dut.id.value = 2
    dut.instr_in.value = 0b01000   # exact match
    dut.cc_in.value = 1
    dut.instr_en.value = 1

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 0
    assert safe(dut.rst.value) == 0
    assert safe(dut.rce.value) == 0
    assert safe(dut.stack_re.value) == 0
    assert safe(dut.pop.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 0
    cocotb.log.info("Decoder 2 — Instruction Disable case passed")


@cocotb.test()
async def test_fetch_PC_to_R_dec2(dut):
    """Decoder 2: 7'b01000x0 → Fetch PC --> R"""
    dut.id.value = 2
    dut.instr_in.value = 0b01000
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.out_ce.value) == 1
    assert safe(dut.rsel.value) == 1
    assert safe(dut.rce.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 2 — Fetch PC → R case passed")



@cocotb.test()
async def test_fetch_R_D_to_R_dec2(dut):
    """Decoder 2: 7'b01001x0 → Fetch R + D --> R"""
    dut.id.value = 2
    dut.instr_in.value = 0b01001
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 1
    assert safe(dut.rce.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 3
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 2 — Fetch R + D → R case passed")



@cocotb.test()
async def test_load_R_dec2(dut):
    """Decoder 2: 7'b01010x0 → Load R"""
    dut.id.value = 2
    dut.instr_in.value = 0b01010
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.out_ce.value) == 0
    assert safe(dut.rsel.value) == 0
    assert safe(dut.rce.value) == 1
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 2 — Load R case passed")



@cocotb.test()
async def test_push_PC_dec2(dut):
    """Decoder 2: 7'b01011x0 → Push PC"""
    dut.id.value = 2
    dut.instr_in.value = 0b01011
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.push.value) == 1
    assert safe(dut.stack_we.value) == 1
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 2 — Push PC case passed")



@cocotb.test()
async def test_default_dec2(dut):
    """Decoder 2: DEFAULT case"""
    dut.id.value = 2
    dut.instr_in.value = 0b11101
    dut.cc_in.value = 1
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 0
    assert safe(dut.rce.value) == 0
    assert safe(dut.oen.value) == 0
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2

    cocotb.log.info("Decoder 2 — DEFAULT case passed")

# ===============================================================
#  INSTRUCTION DECODER 3 — DIRECTED TESTCASES
#  Place these AFTER decoder_2 tests
# ===============================================================


@cocotb.test()
async def test_instruction_disable_dec3(dut):
    """Decoder 3: 7'b0110101 → Instruction Disable"""
    dut.id.value = 3
    dut.instr_in.value = 0b01101   # exact pattern
    dut.cc_in.value = 0
    dut.instr_en.value = 1         # final bit must be 1

    await Timer(1, "ns")

    assert safe(dut.oen.value) == 1
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.stack_re.value) == 0
    assert safe(dut.pop.value) == 0
    cocotb.log.info("Decoder 3 — Instruction Disable case passed")



@cocotb.test()
async def test_push_D_dec3(dut):
    """Decoder 3: 7'b01100x0 → PUSH D"""
    dut.id.value = 3
    dut.instr_in.value = 0b01100
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.push.value) == 1
    assert safe(dut.stack_we.value) == 1
    assert safe(dut.src_sel.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 3 — PUSH D case passed")



@cocotb.test()
async def test_pop_S_dec3(dut):
    """Decoder 3: 7'b01101x0 → POP S"""
    dut.id.value = 3
    dut.instr_in.value = 0b01101
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.stack_re.value) == 1
    assert safe(dut.pop.value) == 1
    assert safe(dut.b_mux_sel.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 3 — POP S case passed")



@cocotb.test()
async def test_pop_PC_dec3(dut):
    """Decoder 3: 7'b01110x0 → POP PC"""
    dut.id.value = 3
    dut.instr_in.value = 0b01110
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.stack_re.value) == 1
    assert safe(dut.pop.value) == 1
    assert safe(dut.b_mux_sel.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 3 — POP PC case passed")



@cocotb.test()
async def test_hold_PC_dec3(dut):
    """Decoder 3: 7'b01111x0 → HOLD PC"""
    dut.id.value = 3
    dut.instr_in.value = 0b01111
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.stack_re.value) == 0
    assert safe(dut.pop.value) == 0
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 0
    cocotb.log.info("Decoder 3 — HOLD PC case passed")



@cocotb.test()
async def test_default_dec3(dut):
    """Decoder 3: DEFAULT case"""
    dut.id.value = 3
    dut.instr_in.value = 0b10110
    dut.cc_in.value = 1
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 0
    assert safe(dut.rce.value) == 0
    assert safe(dut.oen.value) == 0
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    cocotb.log.info("Decoder 3 — DEFAULT case passed")


# ===============================================================
#  INSTRUCTION DECODER 4 — DIRECTED TESTCASES
#  Place these AFTER decoder_3 tests
# ===============================================================


@cocotb.test()
async def test_instruction_disable_dec4(dut):
    """Decoder 4: 7'b0110101 → Instruction Disable"""
    dut.id.value = 4
    dut.instr_in.value = 0b01101
    dut.cc_in.value = 0
    dut.instr_en.value = 1

    await Timer(1, "ns")

    assert safe(dut.oen.value) == 1
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.stack_re.value) == 0
    assert safe(dut.pop.value) == 0
    cocotb.log.info("Decoder 4 — Instruction Disable case passed")



@cocotb.test()
async def test_fail_conditional_dec4(dut):
    """Decoder 4: 7'b1xxxx10 → Fail Conditional Test"""
    dut.id.value = 4

    # Choose a matching candidate: instr_in = 10000, cc = 1, instr_en = 0
    dut.instr_in.value = 0b10000
    dut.cc_in.value = 1
    dut.instr_en.value = 0   # last bit must be 0 → matches x10

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 4 — Fail Conditional Test case passed")



@cocotb.test()
async def test_jump_R_dec4(dut):
    """Decoder 4: 7'b1000000 → Jump R"""
    dut.id.value = 4
    dut.instr_in.value = 0b10000
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.a_mux_sel.value) == 1
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 4 — Jump R case passed")



@cocotb.test()
async def test_jump_D_dec4(dut):
    """Decoder 4: 7'b1000100 → Jump D"""
    dut.id.value = 4
    dut.instr_in.value = 0b10001
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 4 — Jump D case passed")



@cocotb.test()
async def test_jump_0_dec4(dut):
    """Decoder 4: 7'b1001000 → Jump 0"""
    dut.id.value = 4
    dut.instr_in.value = 0b10010
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 4 — Jump 0 case passed")



@cocotb.test()
async def test_default_dec4(dut):
    """Decoder 4: DEFAULT case"""
    dut.id.value = 4

    # pattern that does NOT match any RTL case
    dut.instr_in.value = 0b00111
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 0
    assert safe(dut.rce.value) == 0
    assert safe(dut.oen.value) == 0
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2

    cocotb.log.info("Decoder 4 — DEFAULT case passed")

# ===============================================================
#  INSTRUCTION DECODER 5 — DIRECTED TESTCASES
#  Place these AFTER decoder_4 tests
# ===============================================================


@cocotb.test()
async def test_instruction_disable_dec5(dut):
    """Decoder 5: 7'b0110101 → Instruction Disable"""
    dut.id.value = 5
    dut.instr_in.value = 0b01101
    dut.cc_in.value = 0
    dut.instr_en.value = 1

    await Timer(1, "ns")

    assert safe(dut.oen.value) == 1
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.stack_re.value) == 0
    assert safe(dut.pop.value) == 0
    cocotb.log.info("Decoder 5 — Instruction Disable case passed")



@cocotb.test()
async def test_fail_conditional_dec5(dut):
    """Decoder 5: 7'b1xxxx10 → Fail Conditional Test"""
    dut.id.value = 5

    # Choose matching pattern: instr_in = 10000, cc=1, instr_en=0 → 1000010
    dut.instr_in.value = 0b10000
    dut.cc_in.value = 1
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.cen.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 5 — Fail Conditional Test case passed")



@cocotb.test()
async def test_jump_R_D_dec5(dut):
    """Decoder 5: 7'b1001100 → Jump R + D"""
    dut.id.value = 5
    dut.instr_in.value = 0b10011
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.cen.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 3
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 5 — Jump R + D case passed")



@cocotb.test()
async def test_jump_PC_D_dec5(dut):
    """Decoder 5: 7'b1010000 → Jump PC + D"""
    dut.id.value = 5
    dut.instr_in.value = 0b10100
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.cen.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 5 — Jump PC + D case passed")



@cocotb.test()
async def test_jump_PC_R_dec5(dut):
    """Decoder 5: 7'b1010100 → Jump PC + R"""
    dut.id.value = 5
    dut.instr_in.value = 0b10101
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.cen.value) == 1
    assert safe(dut.a_mux_sel.value) == 1
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.oen.value) == 1
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 1
    cocotb.log.info("Decoder 5 — Jump PC + R case passed")



@cocotb.test()
async def test_default_dec5(dut):
    """Decoder 5: DEFAULT case"""
    dut.id.value = 5

    # Choose a pattern that does NOT match any case
    dut.instr_in.value = 0b00111
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 0
    assert safe(dut.rce.value) == 0
    assert safe(dut.oen.value) == 0
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2

    cocotb.log.info("Decoder 5 — DEFAULT case passed")

# ===============================================================
#  INSTRUCTION DECODER 6 — DIRECTED TESTCASES
#  Place these AFTER decoder_5 tests
# ===============================================================


@cocotb.test()
async def test_instruction_disable_dec6(dut):
    """Decoder 6: 7'b0110101 → Instruction Disable"""
    dut.id.value = 6
    dut.instr_in.value = 0b01101
    dut.cc_in.value = 0
    dut.instr_en.value = 1

    await Timer(1, "ns")

    assert safe(dut.oen.value) == 1
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.stack_re.value) == 0
    assert safe(dut.pop.value) == 0

    cocotb.log.info("Decoder 6 — Instruction Disable case passed")

@cocotb.test()
async def test_jsb_R_dec6(dut):
    """Decoder 6: 7'b1011000 → JSB R"""
    dut.id.value = 6
    dut.instr_in.value = 0b10110
    dut.cc_in.value = 0
    dut.instr_en.value = 0   # last two bits = 00 → matches ...1000

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.push.value) == 1
    assert safe(dut.stack_we.value) == 1
    assert safe(dut.a_mux_sel.value) == 1
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.oen.value) == 1
    assert safe(dut.inc.value) == 1

    cocotb.log.info("Decoder 6 — JSB R case passed")



@cocotb.test()
async def test_jsb_D_dec6(dut):
    """Decoder 6: 7'b1011100 → JSB D"""
    dut.id.value = 6
    dut.instr_in.value = 0b10111
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.push.value) == 1
    assert safe(dut.stack_we.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.oen.value) == 1
    assert safe(dut.inc.value) == 1

    cocotb.log.info("Decoder 6 — JSB D case passed")



@cocotb.test()
async def test_jsb_0_dec6(dut):
    """Decoder 6: 7'b1100000 → JSB 0"""
    dut.id.value = 6
    dut.instr_in.value = 0b11000
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.push.value) == 1
    assert safe(dut.stack_we.value) == 1
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2
    assert safe(dut.inc.value) == 1

    cocotb.log.info("Decoder 6 — JSB 0 case passed")



@cocotb.test()
async def test_jsb_R_D_dec6(dut):
    """Decoder 6: 7'b1100100 → JSB R + D"""
    dut.id.value = 6
    dut.instr_in.value = 0b11001
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.cen.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 3
    assert safe(dut.push.value) == 1
    assert safe(dut.stack_we.value) == 1
    assert safe(dut.inc.value) == 1

    cocotb.log.info("Decoder 6 — JSB R + D case passed")



@cocotb.test()
async def test_jsb_PC_D_dec6(dut):
    """Decoder 6: 7'b1101000 → JSB PC + D"""
    dut.id.value = 6
    dut.instr_in.value = 0b11010
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.cen.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.push.value) == 1
    assert safe(dut.stack_we.value) == 1
    assert safe(dut.inc.value) == 1

    cocotb.log.info("Decoder 6 — JSB PC + D case passed")



@cocotb.test()
async def test_default_dec6(dut):
    """Decoder 6: DEFAULT case"""
    dut.id.value = 6

    # choose a pattern that does NOT match any JSB instruction or disable case
    dut.instr_in.value = 0b00111
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.cen.value) == 0
    assert safe(dut.rce.value) == 0
    assert safe(dut.oen.value) == 0
    assert safe(dut.pc_mux_sel.value) == 0
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2

    cocotb.log.info("Decoder 6 — DEFAULT case passed")


# ===============================================================
#  INSTRUCTION DECODER 7 — DIRECTED TESTCASES
# ===============================================================


@cocotb.test()
async def test_instruction_disable_dec7(dut):
    """Decoder 7: 7'b0110101 → Instruction Disable"""
    dut.id.value = 7
    dut.instr_in.value = 0b01101
    dut.cc_in.value = 0
    dut.instr_en.value = 1

    await Timer(1, "ns")

    assert safe(dut.oen.value) == 1
    assert safe(dut.inc.value) == 0
    assert safe(dut.stack_re.value) == 0
    assert safe(dut.pop.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2

    cocotb.log.info("Decoder 7 — Instruction Disable case passed")



@cocotb.test()
async def test_jsb_PC_R_dec7(dut):
    """Decoder 7: 7'b1101100 → JSB PC + R"""
    dut.id.value = 7
    dut.instr_in.value = 0b11011  # instr = 11011, cc=0, en=0 → ...1100
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.cen.value) == 1
    assert safe(dut.push.value) == 1
    assert safe(dut.stack_we.value) == 1
    assert safe(dut.a_mux_sel.value) == 1
    assert safe(dut.b_mux_sel.value) == 0
    assert safe(dut.inc.value) == 1

    cocotb.log.info("Decoder 7 — JSB PC + R case passed")



@cocotb.test()
async def test_return_S_dec7(dut):
    """Decoder 7: 7'b1110000 → Return S"""
    dut.id.value = 7
    dut.instr_in.value = 0b11100
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.stack_re.value) == 1
    assert safe(dut.pop.value) == 1
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1

    cocotb.log.info("Decoder 7 — Return S case passed")



@cocotb.test()
async def test_return_S_D_dec7(dut):
    """Decoder 7: 7'b1110100 → Return S + D"""
    dut.id.value = 7
    dut.instr_in.value = 0b11101
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.stack_re.value) == 1
    assert safe(dut.pop.value) == 1
    assert safe(dut.cen.value) == 1
    assert safe(dut.a_mux_sel.value) == 0
    assert safe(dut.b_mux_sel.value) == 1
    assert safe(dut.inc.value) == 1

    cocotb.log.info("Decoder 7 — Return S + D case passed")



@cocotb.test()
async def test_hold_dec7(dut):
    """Decoder 7: 7'b1111000 → HOLD"""
    dut.id.value = 7
    dut.instr_in.value = 0b11110
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.cen.value) == 0
    assert safe(dut.pop.value) == 0
    assert safe(dut.stack_re.value) == 0
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 0

    cocotb.log.info("Decoder 7 — HOLD case passed")



@cocotb.test()
async def test_suspend_dec7(dut):
    """Decoder 7: 7'b1111100 → SUSPEND"""
    dut.id.value = 7
    dut.instr_in.value = 0b11111
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 1
    assert safe(dut.cen.value) == 0
    assert safe(dut.pc_mux_sel.value) == 1
    assert safe(dut.inc.value) == 0
    assert safe(dut.oen.value) == 0
    assert safe(dut.push.value) == 0

    cocotb.log.info("Decoder 7 — SUSPEND case passed")



@cocotb.test()
async def test_default_dec7(dut):
    """Decoder 7: DEFAULT case"""
    dut.id.value = 7

    # Choose unmatched pattern
    dut.instr_in.value = 0b00011
    dut.cc_in.value = 0
    dut.instr_en.value = 0

    await Timer(1, "ns")

    assert safe(dut.rce.value) == 0
    assert safe(dut.cen.value) == 0
    assert safe(dut.oen.value) == 0
    assert safe(dut.inc.value) == 0
    assert safe(dut.a_mux_sel.value) == 2
    assert safe(dut.b_mux_sel.value) == 2

    cocotb.log.info("Decoder 7 — DEFAULT case passed")

def test_instruction_decoder_hidden_runner():
    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent

    sources = [
    proj_path / "sources/instruction_decoder.v",       
    proj_path / "sources/instruction_decoder_0.v",
    proj_path / "sources/instruction_decoder_1.v",
    proj_path / "sources/instruction_decoder_2.v",
    proj_path / "sources/instruction_decoder_3.v",
    proj_path / "sources/instruction_decoder_4.v",
    proj_path / "sources/instruction_decoder_5.v",
    proj_path / "sources/instruction_decoder_6.v",
    proj_path / "sources/instruction_decoder_7.v",
   ]

    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="instruction_decoder",
        always=True,
    )
    runner.test(hdl_toplevel="instruction_decoder", test_module="test_instruction_decoder_hidden")
