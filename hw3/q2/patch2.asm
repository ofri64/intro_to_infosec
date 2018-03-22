MOV EBX, 0x08048631
JMP EBX
mov ax, [eax]
movzx eax, al
cmp eax, 0x23
jne small_dead_zone_end
lea eax, [ebp-0x40c]
mov ax, [eax+1]
movzx eax, al
cmp eax, 0x21
jne small_dead_zone_end
lea eax, [ebp-0x40c]
add eax, 2
push eax
call 0x08048460
pop eax
MOV EBX, 0x08048631
JMP EBX
small_dead_zone_end:
MOV EBX, 0x0804863A
JMP EBX