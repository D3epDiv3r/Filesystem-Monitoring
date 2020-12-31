#!/usr/bin/env python3

import os, sys
import time
# Use pip3 install watchdog to install watchdog 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# directories_to_watch = ["C:\\Users\\explo\\Documents", "C:\\xampp\\htdocs", "F:\\laravel-apps", "F:\\All Courses Mike"]
directories_to_watch = "C:\\Users\\explo\\Documents"
path_to_write = "C:\\Users\\explo\\Desktop"
file_name = "filesystem_monitoring.txt"
storage_path = path_to_write + '\\' + file_name

if not os.path.exists(directories_to_watch):
    print("The Directory/Path does not exist")
    sys.exit(1)

if not os.path.exists(path_to_write):
    print("The Path does not exist")
    sys.exit(1)


class Monitor:
    def __init__(self, watch_directory):
        self.observer = Observer()
        self.watch_directory = watch_directory

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watch_directory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(10)
        except:
            self.observer.stop()
            print(f"[+] Saved output to {path_to_write}\{file_name}")
            print("[-] Stopped Observer and Caught Exception.")
        self.observer.join()

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        # Take any action here when a file is first created.
        with open(storage_path, 'a') as file:
            file.write(f"[++] Created {event.src_path}")
            file.write("\n")
    def on_deleted(self, event):
        # Take any action here when a file is first deleted.
        with open(storage_path, 'a') as file:
            file.write(f"[!!] Deleted {event.src_path}")
            file.write("\n")
    # Excluded modified function cause of inconsistency, e.g
    # For every creation and deletion there is a modification,
    # and for every real modification there is a modification,
    # thus inconsistency in determining the real modification.
    # def on_modified(self, event):
    #     # Take any action here when a file is first modified.
    #     print(f"on_modified {event.src_path}")
    def on_moved(self, event):
        # Take any action here when a file is first moved (Renamed).
        with open(storage_path, 'a') as file:
            file.write(f"[>>] Renamed {event.src_path} to {event.dest_path}")
            file.write("\n")

if __name__ == '__main__':
    m = Monitor(directories_to_watch)
    m.run()
