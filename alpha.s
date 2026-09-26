/*
 * ALPHA: Irreducible Bootstrap Seed
 * Canonical Root Artifact: alpha.bin
 * Machine Contract: CONTRACT-QEMU-VIRT-AARCH64-M1
 * Entry Point: 0x00000000 (Flash Base)
 */

.global _start
.section .text
.balign 64

_start:
    /* 1. Mask all interrupts (DAIF: D=1, A=1, I=1, F=1) */
    msr daifset, #0xf

    /* 2. Initialize Stack Pointer to Scratchpad RAM */
    ldr x0, =0x401FF000
    mov sp, x0

    /* 3. Initialize UART MMIO Base Pointer in x20 */
    ldr x20, =0x09000000

    /* 4. Emit Diagnostic Checkpoint 1: AWAKEN */
    adr x21, msg_awaken
    bl print_string

    /* 5. Populate Machine Boot Descriptor at 0x401FE000 */
    ldr x22, =0x401FE000
    ldr x0, =0x40000000
    str x0, [x22, #0]           /* +0:  RAM Base */
    ldr x0, =0x08000000
    str x0, [x22, #8]           /* +8:  RAM Size (128 MiB) */
    mov x0, x20
    str x0, [x22, #16]          /* +16: UART MMIO Base */
    ldr x0, =0x40200000
    str x0, [x22, #24]          /* +24: Physics Payload Base */
    mov x0, #256
    str x0, [x22, #32]          /* +32: Physics Payload Size */

    /* 6. Emit Diagnostic Checkpoint 2: VERIFY */
    adr x21, msg_verify
    bl print_string

    /* 7. Verify PHYSICS-0 Integrity (64-bit FNV-1a Hash) */
    ldr x23, =0x40200000        /* Payload Base */
    mov x24, #256               /* Byte count */
    ldr x25, =0xcbf29ce484222325 /* FNV Offset Basis */
    ldr x26, =0x00000100000001b3 /* FNV Prime */

.Lverify_loop:
    ldrb w27, [x23], #1
    eor x25, x25, x27
    mul x25, x25, x26
    subs x24, x24, #1
    b.ne .Lverify_loop

    /* Compare computed digest against pinned expected digest */
    ldr x28, =0x106e6d37dd96e28b
    cmp x25, x28
    b.ne .Lrefuse_handoff

    /* 8. Emit Diagnostic Checkpoint 3: HANDOFF */
    adr x21, msg_handoff
    bl print_string

    /* 9. Establish PHYSICS_ENTRY_ABI */
    mov x0, x22                 /* x0 = pointer to Boot Descriptor (0x401FE000) */
    mov x1, #256                /* x1 = payload size (256 bytes) */
    ldr x2, =0x5048595349435330 /* x2 = verification cookie ('PHYSICS0') */
    ldr x19, =0x40200000        /* Physics entry address */

    /* 10. Transfer Control to Physics */
    br x19

    /* Terminal fallthrough trap */
    b .Lquiescent_halt

.Lrefuse_handoff:
    /* Emit Refusal Diagnostic */
    adr x21, msg_refuse
    bl print_string

.Lquiescent_halt:
    /* Fail-Closed Quiescence: no external side effects, no fallthrough */
    wfe
    b .Lquiescent_halt

/* Helper: Polled UART String Output */
print_string:
.Lprint_char:
    ldrb w0, [x21], #1
    cbz w0, .Lprint_ret
    str w0, [x20]
    b .Lprint_char
.Lprint_ret:
    ret

.balign 4
msg_awaken:
    .asciz "ALPHA: AWAKEN\n"
msg_verify:
    .asciz "ALPHA: VERIFY\n"
msg_handoff:
    .asciz "ALPHA: HANDOFF\n"
msg_refuse:
    .asciz "ALPHA: REFUSE\n"

.ltorg
.balign 64
_end:
