import sys
import time
from time import strftime
from datetime import datetime,timedelta
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

browser = webdriver.Chrome()
url="http://localhost:5000"
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
        global last_time
        if last_time + timedelta(seconds=1) < datetime.now():
            try:
                self.process(event)
                browser.switch_to_window(home_window)
                browser.refresh()
                last_time=datetime.now()
            except:
                quit()
            
def activate_event():
    path=os.path.dirname(os.path.realpath(__file__))
    filename='test.log'
    filename=os.path.join(path,filename)
    f=open(filename,'w')
    f.write('test')
    f.close

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    observer = Observer()
    observer.schedule(MyHandler(observer), path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
            if last_time + timedelta(minutes=10) < datetime.now():
                activate_event()
    except KeyboardInterrupt:
        browser.close()
        observer.stop()
    observer.join()
