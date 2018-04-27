#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/user.h>
#include <sys/syscall.h>
#include <sys/reg.h>


unsigned ANTI_PID = 0x12345678;

int main(int argc, char **argv) {
    // Make the malware stop waiting for our output by forking a child process:
    if (fork() != 0) {
        // Kill the parent process so we stop waiting from the malware
        return 0;
    } else {
        // Close the output stream so we stop waiting from the malware
        fclose(stdout);
    }

    // The rest of your code goes here

    unsigned pid = ANTI_PID;
    int status = 0; // indicate if the tracee stopped
    int syscall_n = 0; // will hold the system call identifier (value from origin_eax)
    int enter_syscall = 1; // will indicate whether we are before or after the system call
    struct user_regs_struct regs; // struct to hold registers values

    if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {  // Attach to the process
        perror("attach");
        return -1;
    }

    wait( &status ); // wait for an event 

    while (1) {
        ptrace(PTRACE_SYSCALL, pid, NULL, NULL); // notify before or after system calls

        wait(&status); // syscall event occurred
        if(WIFEXITED(status)){ // if for some reason the tracee exited - exit the loop
            break;
        }

        ptrace(PTRACE_GETREGS, pid, NULL, &regs); // read theh tracee's registers
        syscall_n = regs.orig_eax;

        if (syscall_n == SYS_read) { // we are only interested in read syscalls
        if (enter_syscall) { 
        // we are before the read syscall - just indicate that the next stop will be after the syscall
            enter_syscall = 0;
        }

        else { // we are after the read was performed - now intercept the return value and change it to zero
          ptrace( PTRACE_GETREGS, pid, NULL, &regs );
          regs.eax = 0; // this holds the return value
          ptrace( PTRACE_SETREGS, pid, NULL, &regs ); // write the new return value to tracee's process registers
          enter_syscall = 1; // also indicate that the next stop will be before a syscall
        }
      }
    }

    if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {  // Detach when done
        perror("detach");
        return -1;
    }   

    return 0;
}
