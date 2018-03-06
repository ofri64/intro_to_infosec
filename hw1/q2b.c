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

        "MOV EAX, 0;" // for non positive arguments return 0
        "CMP EBX, EAX;"
        "JLE _END;" // if agrument n <= 0 jump to end and return 0

        "MOV ESI, 0;" // start with no = 0
        "MOV EDI, 1;" // and n1 = 1
        "MOV EAX, ESI;"
        "ADD EAX, EDI;" // together with command above, performing f[n] = f[n-1] + f[n-2]
        "MOV ECX, 2;" // initiate counter variable 

        "_WHILE_LOOP:;"
        "CMP ECX, EBX;" // compare between counter and n
        "JGE _END;" // if counter >= n we are done
        
        /* Begining of while loop */

        "MOV ESI, EDI;" // f[n-2] = f[n-1]
        "MOV EDI, EAX;" // f[n-1] = f[n]
        "MOV EAX, ESI;" 
        "ADD EAX, EDI;" // again, with the line above performing f[n+1] = f[n] + f[n-1]
        "ADD ECX, 1;" // perform counter += 1
        "JMP _WHILE_LOOP;"

        /* End of while loop */       

        "_END:;"

    );

    asm ("MOV %0, EAX"
        : "=r"(output));

    printf("%d\n", output);
    
    return 0;
}
