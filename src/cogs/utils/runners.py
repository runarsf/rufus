import os
import re
import subprocess

def python(message, lang: str = 'python3'):
    with open('./runners/python.py', 'w+') as runner_file:
        runner_file.write(re.sub(r'^\w+\s{1}', '', message.content[3:-3]))
    build = subprocess.run([lang, './runners/python.py'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    os.remove('./runners/python.py')
    return build
