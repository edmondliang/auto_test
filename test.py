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

last_time = datetime.now()
host = '127.0.0.1'
port = '2222'
user = 'vagrant'
password = 'vagrant'


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
        global last_time, host, port, user, password
        self.process(event)
        if last_time + timedelta(seconds=3) < datetime.now():
            # os.system("plink vagrant@127.0.0.1 -P 2222 -pw vagrant phpunit /var/www/html/sqs/sqs_handler/unittest.php --debug")
            self.set_env(host, port, user, password)
            commands = []
            commands.append(
                "phpunit /var/www/html/sqs/sqs_handler/unittest.php --debug")
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


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    observer = Observer()
    observer.schedule(MyHandler(observer), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
