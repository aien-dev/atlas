/*
 * PHYSICS-0: Minimal Machine Authority Handoff Stub
 * Milestone 1 Target: Verifies PHYSICS_ENTRY_ABI and signals successful authorization.
 * Entry Point: 0x40200000
 * Exact Payload Size: 256 bytes (0x100)
 */

.global _start
.section .text
.balign 256

_start:
    /* Check Verification Cookie in x2: ASCII 'PHYSICS0' = 0x5048595349435330 */
    ldr x3, =0x5048595349435330
    cmp x2, x3
    b.ne .Lphysics_denied

    /* Check Boot Descriptor pointer in x0 */
    ldr x4, =0x401FE000
    cmp x0, x4
    b.ne .Lphysics_denied

    /* Check Payload Size in x1 (256 bytes) */
    cmp x1, #256
    b.ne .Lphysics_denied

    /* Load UART Base from Boot Descriptor (offset 16) */
    ldr x5, [x0, #16]

    /* Emit "PHYSICS-0: AUTHORIZED\n" */
    adr x6, msg_authorized
.Lemit_auth:
    ldrb w7, [x6], #1
    cbz w7, .Lphysics_quiescent
    str w7, [x5]
    b .Lemit_auth

.Lphysics_denied:
    ldr x5, =0x09000000
    adr x6, msg_denied
.Lemit_denied:
    ldrb w7, [x6], #1
    cbz w7, .Lphysics_quiescent
    str w7, [x5]
    b .Lemit_denied

.Lphysics_quiescent:
    wfe
    b .Lphysics_quiescent

.balign 4
msg_authorized:
    .asciz "PHYSICS-0: AUTHORIZED\n"
msg_denied:
    .asciz "PHYSICS-0: DENIED\n"

.ltorg

/* Pad exactly to 256 bytes from _start */
.space 256 - (. - _start), 0
_end:
