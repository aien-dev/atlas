/*
 * ATLAS: Irreducible Bootstrap Seed
 * Canonical Root Artifact: atlas.bin
 * Formerly designated Alpha (alpha.bin) in early lineage bootstrap drafting.
 * Machine Contract: CONTRACT-QEMU-VIRT-AARCH64-M1
 * Cryptographic Integrity Scheme: Standard SHA-256
 * Pinned Digest: e1d89bb1e0854ebaccd2be5c756c8a2ff8c5ecc8c0f90b4abd461fb7bf98374c
 * Entry Point: 0x00000000 (Flash Base)
 */

.global _start
.section .text
.balign 64

_start:
    /* 1. Mask all interrupts (DAIF: D=1, A=1, I=1, F=1) */
    msr daifset, #0xf

    /* 2. Initialize Stack Pointer to Scratchpad RAM (Disjoint from Descriptor @ 0x401FE000) */
    ldr x0, =0x401FC000
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

    /* 7. Verify PHYSICS-0 Integrity using Cryptographic SHA-256 */
    /* sha256_256bytes(payload, scratch_buf, out_digest) */
    ldr x0, =0x40200000         /* Arg 0: Payload base */
    ldr x1, =0x401FE100         /* Arg 1: 64-byte scratchpad for padding block */
    ldr x2, =0x401FE080         /* Arg 2: 32-byte digest output buffer */
    bl sha256_256bytes

    /* Compare computed 32-byte SHA-256 against pinned expected digest */
    ldr x2, =0x401FE080
    adr x3, pinned_sha256_digest

    /* Compare 8 x 32-bit words (2 x 64-bit pair loads) */
    ldp x4, x5, [x2, #0]
    ldp x6, x7, [x3, #0]
    cmp x4, x6
    b.ne .Lrefuse_handoff
    cmp x5, x7
    b.ne .Lrefuse_handoff

    ldp x4, x5, [x2, #16]
    ldp x6, x7, [x3, #16]
    cmp x4, x6
    b.ne .Lrefuse_handoff
    cmp x5, x7
    b.ne .Lrefuse_handoff

    /* 8. Emit Diagnostic Checkpoint 3: HANDOFF */
    adr x21, msg_handoff
    bl print_string

    /* 9. Establish PHYSICS_ENTRY_ABI */
    mov x0, x22                 /* x0 = pointer to Boot Descriptor (0x401FE000) */
    mov x1, #256                /* x1 = payload size (256 bytes) */
    ldr x2, =0x5048595349435330 /* x2 = verification cookie ('PHYSICS0') */

    /* Static Target Proof: x19 is explicitly loaded from literal 0x40200000 immediately before branch */
    ldr x19, =0x40200000        /* Target: Contract-defined Physics Entry */

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

.balign 8
msg_awaken:
    .asciz "ATLAS: AWAKEN\n"
msg_verify:
    .asciz "ATLAS: VERIFY\n"
msg_handoff:
    .asciz "ATLAS: HANDOFF\n"
msg_refuse:
    .asciz "ATLAS: REFUSE\n"

.balign 8
pinned_sha256_digest:
    /* e1d89bb1 e0854eba ccd2be5c 756c8a2f f8c5ecc8 c0f90b4a bd461fb7 bf98374c */
    .word 0xe1d89bb1, 0xe0854eba, 0xccd2be5c, 0x756c8a2f
    .word 0xf8c5ecc8, 0xc0f90b4a, 0xbd461fb7, 0xbf98374c

.ltorg
.balign 64
code_end:
