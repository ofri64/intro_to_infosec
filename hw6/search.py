import assemble
import string
import itertools, re, struct


GENERAL_REGISTERS = [
    'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi'
]


ALL_REGISTERS = GENERAL_REGISTERS + [
    'esp', 'eip', 'ebp'
]


class GadgetSearch(object):
    def __init__(self, dump_path, start_addr):
        """
        Construct the GadgetSearch object.

        Input:
            dump_path: The path to the memory dump file created with GDB.
            start_addr: The starting memory address of this dump.
        """
        self.start_addr = start_addr
        with open(dump_path, 'rb') as f:
            self.dump = f.read()

    def get_format_count(self, gadget_format):
        """
        Get how many different register placeholders are in the pattern.
        
        Examples:
            self.get_format_count('POP ebx')
            => 0
            self.get_format_count('POP {0}')
            => 1
            self.get_format_count('XOR {0}, {0}; ADD {0}, {1}')
            => 2
        """
        # Hint: Use the string.Formatter().parse method:
        #
        #   import string
        #   print string.Formatter().parse(gadget_format)

        tuples_iter = string.Formatter().parse(gadget_format) # returns iterator
        # filter parts without format using the filter method over the iterator
        tuples_iter_only_placeholders = itertools.ifilter(lambda x: x[1]!=None, tuples_iter)
        placeholders_list = [t[1] for t in tuples_iter_only_placeholders]
        placeholders_set = set(placeholders_list) # remove duplicats by converting to set instead of list
        return len(placeholders_set)


    def get_register_combos(self, nregs, registers):
        """
        Return all the combinations of `registers` with `nregs` registers in
        each combination. Duplicates ARE allowed!

        Example:
            self.get_register_combos(2, ('eax', 'ebx'))
            => [['eax', 'eax'],
                ['eax', 'ebx'],
                ['ebx', 'eax'],
                ['ebx', 'ebx']]
        """
        # itertools.products for counting with replacement and ordering
        combs_iter = itertools.product(registers, repeat=nregs)
        combs = [list(c) for c in combs_iter]
        return combs

    def format_all_gadgets(self, gadget_format, registers):
        """
        Format all the possible gadgets for this format with the given
        registers.

        Example:
            self.format_all_gadgets("POP {0}; ADD {0}, {1}", ('eax', 'ecx'))
            => [['POP eax; ADD eax, eax'],
                ['POP eax; ADD eax, ecx'],
                ['POP ecx; ADD ecx, eax'],
                ['POP ecx; ADD ecx, ecx']]
        """
        # Hints:
        #
        # 0. Use the previous functions to count the number of placeholders,
        #    and get all combinations of registers.
        #
        # 1. Use the `format` function to build the string:
        #
        #    'Hi {0}! I am {1}, you are {0}'.format('Luke', 'Vader')
        #    => 'Hi Luke! I am Vader, you are Luke'
        #
        # 2. You can use pass a list of arguments instead of specifying each
        #    argument individually. Use the internet, the force is strong with
        #    StackOverflow.

        num_placeholders = self.get_format_count(gadget_format)
        registers_comb = self.get_register_combos(num_placeholders, registers) # get combinations use num_placeholders
        format_gadgets = [gadget_format.format(*comb) for comb in registers_comb] # transform to gadgets using string.format
        return format_gadgets

    def find_all(self, gadget):
        """
        Return all the addresses of the gadget inside the memory dump.

        Example:
            self.find_all('POP eax')
            => < all ABSOLUTE addresses in memory of 'POP eax; RET' >
        """
        # Notes:
        #
        # 1. Addresses are ABSOLUTE (for example, 0x08403214), NOT RELATIVE to
        #    the beginning of the file (for example, 12).
        #
        # 2. Don't forget to add the 'RET'.
        gadget_with_ret = gadget + '; RET'
        assembled_gadget = assemble.assemble_data(gadget_with_ret) # tranform to bytes from the assembly code
        # print [hex(struct.unpack("B",o)[0]) for o in assembled_gadget]
        # use re moudle to search in the dump file. add the offset to base address to get absolut addresses
        gadget_addresses = [hex(g.start() + self.start_addr)[:-1] for g in re.finditer(re.escape(assembled_gadget), self.dump)]
        return gadget_addresses

    def find(self, gadget, condition=None):
        """
        Return the first result of find_all. If condition is specified, only
        consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(addr for addr in self.find_all(gadget)
                        if condition(addr))
        except StopIteration:
            raise ValueError("Couldn't find matching address for " + gadget)

    def find_all_formats(self, gadget_format, registers=GENERAL_REGISTERS):
        """
        Similar to find_all - but return all the addresses of all
        possible gadgets that can be created with this format and registers.
        Every elemnt in the result will be a tuple of the gadget string and
        the address in which it appears.

        Example:
            self.find_all_formats('POP {0}; POP {1}')
            => [('POP eax; POP ebx', address1),
                ('POP ecx; POP esi', address2),
                ...]
        """
        format_gadgets = self.format_all_gadgets(gadget_format, registers) # first get all formats
        all_formats_for_gadgets = [zip(itertools.cycle([g]), self.find_all(g)) for g in format_gadgets]
        # we have a list of lists, we need to expand it to a single list using itertools.chain
        all_formats = list(itertools.chain.from_iterable(all_formats_for_gadgets))
        return all_formats

    def find_format(self, gadget_format, registers=GENERAL_REGISTERS,
                    condition=None):
        """
        Return the first result of find_all_formats. If condition is specified,
        only consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(
                addr for addr in self.find_all_formats(gadget_format, registers)
                if condition(addr)
            )
        except StopIteration:
            raise ValueError(
                "Couldn't find matching address for " + gadget_format)



# if __name__ == '__main__':
    # gs = GadgetSearch("./libc.bin", 0xb7c38750)
    # print gs.get_register_combos(3, ('eax', 'ebx'))
    # print gs.get_format_count('XOR {0}, {0}; ADD {0}, {1}')
    # print gs.format_all_gadgets("POP {0}; ADD {0}, {1}", ('eax', 'ecx'))
    # print gs.find_all('dec eax; inc')
    # print gs.find_all_formats('POP {0}; POP {1}', registers=['esi', 'edi'])
    # print gs.find_format('POP {0}; POP {1}', registers=['esi', 'edi'])
