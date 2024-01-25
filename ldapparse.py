import subprocess
import os
import concurrent.futures
import random
import string

def get_ip(current_string):
        ip_start = current.find("Naming Context for")+19
        ip_end = ip_start + current[ip_start:].find("\n")
        return current[ip_start:ip_end]

def get_naming_context(current_string):
        namingContexts_start = 0
        naming_context_list = []
        while namingContexts_start != -1:
                namingContexts_start = current_string.find("namingContexts")
                if namingContexts_start == -1:
                        break
                namingContexts_end = namingContexts_start + current_string[namingContexts_start:].find("\n")
                naming_context_list.append(current_string[namingContexts_start+16:namingContexts_end])
                current_string = current_string[namingContexts_end:]
        return naming_context_list

def call_command(command):
        print(f"Calling {command}...")
        command_call = subprocess.run([command], shell=True,stdout=subprocess.PIPE)
        if (b"successful bind" not in command_call.stdout) and (b"Insufficient access" not in command_call.stdout) and (b"Invalid DN syntax" not in command_call.stdout):
                filename = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
                with open(f"OUTPUT/{filename}.out", 'w') as f:
                        f.write(command + "\n")
                        f.write(command_call.stdout.decode('utf-8'))

with open("ldap_search.output") as f:
        data = f.read()

all_data = data.split("##########################################")
commands = []

for current in all_data:
        current_ip = get_ip(current)
        current_naming_context = get_naming_context(current)
        if current_naming_context:
                # print(current_ip, current_naming_context)
                for naming_context in current_naming_context:
                        command = f"ldapsearch -x -H ldap://{current_ip} -b '{naming_context}' -E pr=1000/noprompt"
                        commands.append(command)

os.makedirs("OUTPUT", exist_ok=True)
count = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_request = {executor.submit(call_command, command): command for command in commands}
        for future in concurrent.futures.as_completed(future_request):
                result = future.result()
                                                                
