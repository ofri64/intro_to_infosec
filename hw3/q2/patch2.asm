MOV EBX, 0x08048631
JMP EBX
lea eax, [ebp-0x40c]
mov eax, [eax]
cmp eax, 0x23
jne label
lea eax, [ebp-0x40c]
mov eax, [eax+1]
cmp eax, 0x21
jne label
label:
MOV EBX, 0x0804863A
JMP EBX