#!/usr/bin/env python3

import os, sys
import time
# Use pip3 install watchdog to install watchdog 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# DIRECTORIES_TO_WATCH = ["C:\Users\explo\Documents", "C:\xampp\htdocs", "F:\laravel-apps"]
DIRECTORIES_TO_WATCH = "C:/Users/explo/Documents"

if not os.path.exists(DIRECTORIES_TO_WATCH):
    print("The File/Path does not exist")
    sys.exit(1)


class Monitor:
    global DIRECTORIES_TO_WATCH

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, DIRECTORIES_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error Occured")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        # Take any action here when a file is first created.
        print(f"[++] Created {event.src_path}")
    def on_deleted(self, event):
        # Take any action here when a file is first deleted.
        print(f"[!!] Deleted {event.src_path}")
    # Excluded modified function cause of inconsistency, e.g
    # For every creation and deletion there is a modification,
    # and for every real modification there is a modification,
    # thus inconsistency in determining real modification.
    # def on_modified(self, event):
    #     # Take any action here when a file is first modified.
    #     print(f"on_modified {event.src_path}")
    def on_moved(self, event):
        # Take any action here when a file is first moved (Renamed).
        print(f"[>>] Renamed {event.src_path} to {event.dest_path}")


if __name__ == '__main__':
    m = Monitor()
    m.run()
