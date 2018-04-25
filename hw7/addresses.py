import struct


def address_to_bytes(address):
    """Convert an address to bytes, in little endian."""
    return struct.pack('<L', address)


########### QUESTION 2 ##############

# Memory address where the check_if_virus function begins.
# USE THIS IN `q2.py`
CHECK_IF_VIRUS_CODE = 0x080485f0

########### QUESTION 3 ##############

# Memory address of the GOT entry of check_if_virus.
# USE THIS IN `q3.py`
CHECK_IF_VIRUS_GOT = 0x804a01c

# Memory address of the function to use as an alternative for check_if_virus
# (i.e. a function with the same signature that you'll write to the GOT instead
# of the address of check_if_virus).
CHECK_IF_VIRUS_ALTERNATIVE = 0x0804878b # the address of "is_directory" function
