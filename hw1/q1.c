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
        /* Your code starts here. */

        "MOV ESI, EBX;" // copy input register from EBX to ESI (denote "n")
        "MOV ECX, 2;" // first divisor is: d = 2
        "MOV EDI, 0;" // defualt return value (max_factor) is 0 - for value less than 1

        "_LOOP1:;" // first while
        "CMP ESI, 1;"
        "JLE _END;" // if n <= 1 - terminate

        /* Begining of first while loop */

        "_LOOP2:;" // second while
        "MOV EAX, ESI;" // put the number we want to divide in EAX - n
        "MOV EDX, 0;"
        "MOV EBX, ECX;" // put the divisor (the value d) in EBX 
        "IDIV EBX;" // quotient now in EAX, reminder ins EDX

        "CMP EDX, 0;" // check if n % d = 0
        "JNE _INC_DIVISOR;" // if value is false don't enter second while loop

        /* Begining of second while loop */

        "CMP ECX, EDI;" // compare d to max_factor 
        "JLE _DONT_UPDATE_DIV;" // if d <= max_factor we "jump over" the update

        "MOV EDI, ECX;" // perform max_factor = d

        "_DONT_UPDATE_DIV:;"
        "MOV ESI, EAX;" // update n = n/d we already have the result in EAX
        "JMP _LOOP2;" // jump to begining of seconds loop

        /* End of second while loop */

        "_INC_DIVISOR:;"
        "ADD ECX, 1;" // perform d += 1
        "JMP _LOOP1;" // jump back to begining of first while

        /* End of first while loop */

        "_END:;"
        "MOV EAX, EDI;" // Move our return value to EAX as needed

        /* Your code stops  here. */
    );

    asm ("MOV %0, EAX"
        : "=r"(output));

    printf("%d\n", output);
    
    return 0;
}
