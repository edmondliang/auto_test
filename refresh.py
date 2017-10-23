import os
import sys
import time
import traceback
import signal
from time import strftime
from datetime import datetime,timedelta
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class MyHandler(FileSystemEventHandler):

    def __init__(self,observer, url='http://127.0.0.1'):
        self.url=url
        self.observer = observer
        
        self.last_time = datetime.now()
        self.browser = webdriver.Chrome()
        self.browser.get(url)
        self.home_window = self.browser.current_window_handle
        self.refresh_ext = ('html','css','js','pyc','py')

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
            # user_input = input()
            ext = event.src_path.split('.')[-1].lower()
            if self.last_time + timedelta(seconds=1) < datetime.now() and ext in self.refresh_ext:
                self.process(event)
                # self.browser.switch_to_window(self.home_window)
                self.browser.refresh()
                self.last_time=datetime.now()
        except:
            traceback.print_exc()
            self.browser.close()
            self.observer.stop()
            print 'Process has been terminated.'
            



class Watcher(object):

    def __init__(self, path, url):
        self.observer = Observer()
        self.path = path
        self.url = url

    def service_shutdown(self):
        self.observer.stop()

    def run(self):
        event_handler = MyHandler(self.observer, self.url)
        self.observer.schedule(event_handler, self.path, recursive=True)

        try:
            self.observer.start()
            while self.observer.isAlive():
                time.sleep(1)

        except:
            if self.observer.isAlive():
                self.observer.stop()
            traceback.print_exc()

        self.observer.join()
        

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    url="http://127.0.0.1:8080"
    w = Watcher(path, url)
    w.run()


        
