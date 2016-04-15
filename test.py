import os
import sys
import time
import json
from time import strftime
from datetime import datetime, timedelta
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists as path_exists
from pprint import pprint

last_time = datetime.now()
host = '127.0.0.1'
port = '2222'
user = 'vagrant'
password = 'vagrant'
is_local =True

class MyHandler(FileSystemEventHandler):

    def __init__(self, observer):
        self.observer = observer

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        # print now only for degug
        print event.src_path, event.event_type, strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def on_any_event(self, event):
        global last_time, host, port, user, password, is_local
        
        if last_time + timedelta(seconds=3) < datetime.now():
            self.process(event)
            self.set_env(host, port, user, password)
            
            if is_local:
                current_path=os.path.dirname(os.path.realpath(__file__))
                filename=os.path.join(current_path,"unittesting.py")
                cmd = "python {} -v".format(filename)
                os.system(cmd)
            else:
                commands = []
                commands.append(
                    "phpunit /var/www/html/sqs/test/test.php --debug")
                commands.append("python "+filename)
                for cmd in commands:
                    run(cmd)
                
            last_time = datetime.now()

    def set_env(self, host, port, user, password):
        """
            Set enviroment
        """
        env.host = host
        env.port = port
        env.host_string = host + ":" + port
        env.user = user
        env.password = password
        env.warn_only = True

def activate_event():
    path=os.path.dirname(os.path.realpath(__file__))
    filename='test.log'
    filename=os.path.join(path,filename)
    f=open(filename,'w')
    f.write(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
    f.close

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    observer.schedule(MyHandler(observer), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
            if last_time + timedelta(minutes=120) < datetime.now():
                activate_event()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
