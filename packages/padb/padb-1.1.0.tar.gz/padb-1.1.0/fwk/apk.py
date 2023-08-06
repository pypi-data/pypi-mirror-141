

from subprocess import TimeoutExpired, run
import platform
import re
import os
import time
from concurrent.futures import ThreadPoolExecutor
import signal
import sys
from multiprocessing.connection import Client, Listener, wait, Pipe
from multiprocessing import Queue, Process, Pool, Process, Lock, Value, Array, Manager
from fwk import compat
__t_pool = ThreadPoolExecutor()


def __cmd_list(cmd, fn=None):
    print('[ cmd ] ', cmd, end='\n')
    if fn is None:
        run(cmd, shell=True)
    else:

        with compat.popen(cmd) as pipe:
            try:
                res = pipe.communicate()[0]
                fn(res)
            except KeyboardInterrupt as e:
                os.killpg(pipe.pid, signal.SIGINT)
            except TimeoutExpired as e:
                os.killpg(pipe.pid, signal.SIGINT)


def am_cmd(serial_no):
    pass


def pm_cmd(serial_no):
    ''' adb shell pm list packages [-f] [-d] [-e] [-s] [-3] [-i] [-u] [--user USER_ID] [FILTER]'''
    pass


def top_activity(serial_no):
    cmd = 'adb -s %s shell dumpsys activity activities | grep mResumedActivity' % serial_no
    __cmd_list(cmd)


def running_services(serial_no, packagename):
    '''adb shell dumpsys activity services [ < packagename > ]'''
    cmd = 'adb -s %s shell dumpsys activity service %s' % (
        serial_no, packagename)
    __cmd_list(cmd)


def open_app(serial_no, act):
    __cmd_list("adb -s "+serial_no + " shell am start -n {}".format(act))



def __is_macos():
    return "Darwin" in platform.system()


def __process_list_interal(pipe, serial_no, app_uid):
    try:
        # for line in iter(lambda: pipe.stdout.readline(), ''):
        isFrist = True

        while True:
            line = pipe.stdout.readline()

            if line is None or len(line) == 0:
                print('end'+"="*20)
                break
            elif isFrist:
                ret = line.split()
                if ret is not None and len(ret) == 8:
                    uid = ret[0]
                    pid = ret[1]
                    ppid = ret[2]
                    c = ret[3]
                    start_time = ret[4]
                    tty = ret[5]
                    time = ret[6]
                    cmd = ret[7]

                    print(uid+'\t'+pid+'\t'+'p_oom_score'+'\t'+ppid+'\t'+'pp_oom_score'+'\t' +
                          c+' '+start_time+'   ' + tty+' '+time+'\t' + cmd)
                isFrist = False

            elif app_uid in line:
                # -f Full listing (-o USER:12=UID,PID,PPID,C,STIME,TTY,TIME,ARGS=CMD)
                # -l Long listing (-o F,S,UID,PID,PPID,C,PRI,NI,ADDR,SZ,WCHAN,TTY,TIME,CMD)
                ret = line.split()
                if ret is not None and len(ret) == 8:
                    uid = ret[0]
                    pid = ret[1]
                    ppid = ret[2]
                    c = ret[3]
                    start_time = ret[4]
                    tty = ret[5]
                    time = ret[6]
                    cmd = ret[7]

                    adb_cmd = 'adb -s '+serial_no + ' shell cat /proc/'+pid+'/oom_score'
                    p_oom_score = os.popen(adb_cmd).read().strip()
                    adb_cmd = 'adb -s '+serial_no + ' shell cat /proc/'+ppid+'/oom_score'
                    pp_oom_score = os.popen(adb_cmd).read().strip()
                    print(uid+'\t'+pid+'\t'+p_oom_score+'\t\t'+ppid+'\t'+pp_oom_score+'\t\t' +
                          c+' '+start_time+' ' + tty+' '+time+'\t' + cmd)

    except KeyboardInterrupt as e:
        os.killpg(pipe.pid, signal.SIGINT)
    except TimeoutExpired as e:
        os.killpg(pipe.pid, signal.SIGINT)


def process_list(serial_no, pkg_name):
    # adb  shell ps -ef |findstr "com.hawksjamesf"

    if __is_macos():
        uid =os.popen('adb  -s '+serial_no+' shell dumpsys package '+pkg_name+' | grep userId= ').read().strip()
        uid ='u0_a'+uid.split('=')[1][-3:]
    else:
        uid =os.popen('adb  -s '+serial_no+' shell dumpsys package '+pkg_name+'| findstr userId= ').read().strip()
        uid ='u0_a'+uid.split('=')[1][-3:]
    with compat.popen("adb -s "+serial_no + " shell ps - ef") as pipe:
        __process_list_interal(pipe, serial_no, uid)


if __name__ == "__main__":
    # while True:
    process_list('c4c81150', 'com.sankuai.meituan')
    process_list('c4c81150', 'com.hawksjamesf.spacecraft.debug')
    # time.sleep(1)



