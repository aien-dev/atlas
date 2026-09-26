	.arch armv8-a
	.file	"sha256_clean.c"
	.text
	.align	2
	.p2align 4,,11
	.global	sha256_transform
	.type	sha256_transform, %function
sha256_transform:
	stp	x29, x30, [sp, -320]!
	sub	x4, x1, #4
	mov	x1, 1
	mov	x29, sp
	add	x12, sp, 64
	stp	x19, x20, [sp, 16]
	stp	x21, x22, [sp, 32]
	stp	x23, x24, [sp, 48]
	.p2align 3,,7
.L2:
	add	x3, x12, x1, lsl 2
	ldr	w2, [x4, x1, lsl 2]
	add	x1, x1, 1
	rev	w2, w2
	str	w2, [x3, -4]
	cmp	x1, 17
	bne	.L2
	ldr	w5, [sp, 64]
	add	x4, sp, 68
	ldp	w13, w11, [sp, 100]
	add	x15, sp, 260
	ldp	w10, w9, [sp, 108]
	ldp	w8, w3, [sp, 116]
	ldr	w7, [sp, 124]
	.p2align 3,,7
.L3:
	add	w6, w5, w13
	ldr	w5, [x4]
	mov	w13, w11
	ror	w2, w3, 19
	eor	w2, w2, w3, ror 17
	mov	w11, w10
	eor	w2, w2, w3, lsr 10
	ror	w1, w5, 18
	eor	w1, w1, w5, ror 7
	mov	w10, w9
	eor	w1, w1, w5, lsr 3
	mov	w9, w8
	add	w1, w1, w2
	mov	w8, w3
	add	x4, x4, 4
	mov	w3, w7
	add	w7, w1, w6
	str	w7, [x4, 56]
	cmp	x4, x15
	bne	.L3
	ldp	w20, w19, [x0]
	adrp	x13, .LANCHOR0
	ldp	w30, w18, [x0, 8]
	add	x13, x13, :lo12:.LANCHOR0
	ldp	w17, w16, [x0, 16]
	mov	w5, w20
	ldp	w15, w14, [x0, 24]
	mov	w8, w19
	mov	w6, w30
	mov	w11, w18
	mov	w4, w17
	mov	w10, w16
	mov	w9, w15
	mov	w21, w14
	mov	x7, 1
	b	.L4
	.p2align 2,,3
.L5:
	mov	w9, w10
	mov	w6, w8
	mov	w10, w4
	mov	w8, w5
	mov	w4, w3
	mov	w5, w2
.L4:
	lsl	x1, x7, 2
	ror	w22, w4, 6
	add	x23, x13, x1
	add	x1, x12, x1
	and	w3, w4, w10
	eor	w22, w22, w4, ror 11
	bic	w2, w9, w4
	eor	w22, w22, w4, ror 25
	ldr	w24, [x1, -4]
	eor	w2, w2, w3
	ldr	w23, [x23, -4]
	eor	w3, w8, w6
	add	w2, w22, w2
	ror	w1, w5, 13
	and	w3, w3, w5
	and	w22, w8, w6
	eor	w1, w1, w5, ror 2
	add	w23, w23, w24
	eor	w3, w3, w22
	eor	w1, w1, w5, ror 22
	add	w2, w2, w23
	add	w1, w1, w3
	add	w2, w2, w21
	add	x7, x7, 1
	add	w3, w2, w11
	mov	w21, w9
	add	w2, w2, w1
	mov	w11, w6
	cmp	x7, 65
	bne	.L5
	add	w20, w20, w2
	add	w19, w19, w5
	add	w30, w30, w8
	add	w18, w18, w6
	add	w17, w17, w3
	add	w16, w16, w4
	add	w15, w15, w10
	add	w14, w14, w9
	stp	w20, w19, [x0]
	stp	w30, w18, [x0, 8]
	stp	w17, w16, [x0, 16]
	stp	w15, w14, [x0, 24]
	ldp	x19, x20, [sp, 16]
	ldp	x21, x22, [sp, 32]
	ldp	x23, x24, [sp, 48]
	ldp	x29, x30, [sp], 320
	ret
	.size	sha256_transform, .-sha256_transform
	.align	2
	.p2align 4,,11
	.global	sha256_compute
	.type	sha256_compute, %function
sha256_compute:
	stp	x29, x30, [sp, -64]!
	mov	x5, 58983
	mov	x4, 62322
	mov	x29, sp
	stp	x21, x22, [sp, 32]
	mov	x22, x3
	mov	x3, 21119
	str	x23, [sp, 48]
	mov	x23, x1
	mov	x1, 55723
	movk	x5, 0x6a09, lsl 16
	movk	x4, 0x3c6e, lsl 16
	movk	x3, 0x510e, lsl 16
	movk	x1, 0x1f83, lsl 16
	movk	x5, 0xae85, lsl 32
	movk	x4, 0xf53a, lsl 32
	movk	x3, 0x688c, lsl 32
	movk	x1, 0xcd19, lsl 32
	stp	x19, x20, [sp, 16]
	movk	x5, 0xbb67, lsl 48
	movk	x4, 0xa54f, lsl 48
	movk	x3, 0x9b05, lsl 48
	movk	x1, 0x5be0, lsl 48
	stp	x5, x4, [x22]
	mov	x19, x0
	stp	x3, x1, [x22, 16]
	mov	x21, x2
	cmp	x23, 63
	bls	.L21
	sub	x20, x23, #64
	and	x20, x20, -64
	add	x20, x20, 64
	add	x20, x0, x20
	.p2align 3,,7
.L12:
	mov	x1, x19
	mov	x0, x22
	add	x19, x19, 64
	bl	sha256_transform
	cmp	x19, x20
	bne	.L12
	and	x2, x23, 63
.L11:
	mov	x0, x21
	add	x4, x21, 128
	.p2align 3,,7
.L13:
	strb	wzr, [x0], 1
	cmp	x0, x4
	bne	.L13
	cbz	x2, .L14
	mov	x0, 0
	.p2align 3,,7
.L15:
	ldrb	w1, [x20, x0]
	strb	w1, [x21, x0]
	add	x0, x0, 1
	cmp	x0, x2
	bne	.L15
	mov	w1, -128
	strb	w1, [x21, x0]
	mov	w19, 2
	mov	w1, 120
	cmp	x0, 55
	bls	.L17
.L18:
	lsl	x23, x23, 3
	add	x1, x21, w1, uxtw
	mov	w0, 56
	.p2align 3,,7
.L19:
	lsr	x2, x23, x0
	sub	w0, w0, #8
	strb	w2, [x1], 1
	cmn	w0, #8
	bne	.L19
	mov	x0, x22
	mov	x1, x21
	bl	sha256_transform
	cmp	w19, 2
	beq	.L29
	ldp	x19, x20, [sp, 16]
	ldp	x21, x22, [sp, 32]
	ldr	x23, [sp, 48]
	ldp	x29, x30, [sp], 64
	ret
.L14:
	mov	w0, -128
	strb	w0, [x21]
.L17:
	mov	w1, 56
	mov	w19, 1
	b	.L18
.L29:
	ldp	x19, x20, [sp, 16]
	add	x1, x21, 64
	ldp	x21, x22, [sp, 32]
	ldr	x23, [sp, 48]
	ldp	x29, x30, [sp], 64
	b	sha256_transform
.L21:
	mov	x20, x0
	mov	x2, x23
	b	.L11
	.size	sha256_compute, .-sha256_compute
	.align	2
	.p2align 4,,11
	.global	sha256_256bytes
	.type	sha256_256bytes, %function
sha256_256bytes:
	mov	x3, x2
	mov	x2, x1
	mov	x1, 256
	b	sha256_compute
	.size	sha256_256bytes, .-sha256_256bytes
	.section	.rodata
	.align	3
	.set	.LANCHOR0,. + 0
	.type	K, %object
	.size	K, 256
K:
	.word	1116352408
	.word	1899447441
	.word	-1245643825
	.word	-373957723
	.word	961987163
	.word	1508970993
	.word	-1841331548
	.word	-1424204075
	.word	-670586216
	.word	310598401
	.word	607225278
	.word	1426881987
	.word	1925078388
	.word	-2132889090
	.word	-1680079193
	.word	-1046744716
	.word	-459576895
	.word	-272742522
	.word	264347078
	.word	604807628
	.word	770255983
	.word	1249150122
	.word	1555081692
	.word	1996064986
	.word	-1740746414
	.word	-1473132947
	.word	-1341970488
	.word	-1084653625
	.word	-958395405
	.word	-710438585
	.word	113926993
	.word	338241895
	.word	666307205
	.word	773529912
	.word	1294757372
	.word	1396182291
	.word	1695183700
	.word	1986661051
	.word	-2117940946
	.word	-1838011259
	.word	-1564481375
	.word	-1474664885
	.word	-1035236496
	.word	-949202525
	.word	-778901479
	.word	-694614492
	.word	-200395387
	.word	275423344
	.word	430227734
	.word	506948616
	.word	659060556
	.word	883997877
	.word	958139571
	.word	1322822218
	.word	1537002063
	.word	1747873779
	.word	1955562222
	.word	2024104815
	.word	-2067236844
	.word	-1933114872
	.word	-1866530822
	.word	-1538233109
	.word	-1090935817
	.word	-965641998
	.ident	"GCC: (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0"
	.section	.note.GNU-stack,"",@progbits
