#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    int input, output;

    if (argc != 2) {
        printf("USAGE: %s <number>\n", argv[0]);
        return -1;
    }

    input = atoi(argv[1]);

    asm ("MOV EBX, %0"
        :
        : "r"(input));

    asm (

        "PUSH EBX;" // push to stack function argument
        "CALL fibo_rec;" 
        "ADD ESP, 4;" // restore stack
        "JMP _END;" 

        "fibo_rec:;"

            /* Prologue */

            "PUSH EBP;"
            "MOV EBP, ESP;"

            /* function logic */

            // Stop criterion

            "MOV EAX, 0;"
            "MOV EDX, [EBP + 8];" // our argument is right after EBP, RA so need EBP+8
            "CMP EDX, EAX;"      
            "JL _END_FIBO_REC;" // if n < 0 jump to end
            "MOV EAX, EDX;"
            "CMP EDX, 1;" // if n <= 1 return n(together with above mean n = 0 or n = 1)
            "JLE _END_FIBO_REC;"

            // Enter to recursive step

            "MOV EDX, [EBP + 8];"
            "SUB EDX, 1;" // EDX = n-1
            "PUSH EDX;"
            "CALL fibo_rec;" // f[n-1]
            "ADD ESP, 4;"
            "PUSH EAX;" // function result is in EAX - save it to stack

            "MOV EDX, [EBP + 8];"
            "SUB EDX, 2;" // EDX = n-2
            "PUSH EDX;"  
            "CALL fibo_rec;" // f[n-2]
            "ADD ESP, 4;"

            "ADD EAX, [ESP];" // Now EAX holds f[n-1] + f[n-2]
            "ADD ESP, 4;" // restore stack (used by the first recursive call)

            "_END_FIBO_REC:;"

            /* Epilogue */

            "MOV ESP, EBP;"
            "POP EBP;"

            "RET;"

        "_END:"

    );

    asm ("MOV %0, EAX"
        : "=r"(output));

    printf("%d\n", output);
    
    return 0;
}
