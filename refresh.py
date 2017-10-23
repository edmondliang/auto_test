import os
import sys
import time
import traceback
from time import strftime
from datetime import datetime,timedelta
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url="http://127.0.0.1:8080"
refresh_ext = ('html','css','js','pyc','py')
browser.get(url)
home_window = browser.current_window_handle
last_time=datetime.now()

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
        print event.src_path, event.event_type ,strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # print now only for degug

    def on_any_event(self, event):
        try:
            global last_time
            ext = event.src_path.split('.')[-1].lower()
            if last_time + timedelta(seconds=1) < datetime.now() and ext in refresh_ext:
                self.process(event)
                # browser.switch_to_window(home_window)
                browser.refresh()
                last_time=datetime.now()
                raise Exception('test error')
        except:
            traceback.print_exc()
            print 'Process has been terminated.'
            browser.close()
            observer.stop()
            quit()


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    observer = Observer()
    observer.schedule(MyHandler(observer), path, recursive=True)
    observer.start()
    observer.join()
