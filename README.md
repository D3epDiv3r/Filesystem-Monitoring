# Filesystem-Monitoring
A basic Filesystem or Directory Event Monitoring tool for Windows built using Python's API Library "[Watchdog](https://github.com/gorakhargosh/watchdog)".

Works on Python 3+.

This program uses Tkinter as the control center interface to help start and stop the observers. It also uses multiprocessing to process multiple directories event handlers. It has a basic start-up functionality to start the program whenever you Login, this can be easily disabled (instruction [below](https://github.com/Chefcury1/Filesystem-Monitoring#disable-startup-functionality)). 


## Supported Platforms
- Windows

A pull request will be appreciated for any other platform integration.

## Dependencies

This module depends on the [Watchdog](https://github.com/gorakhargosh/watchdog) Library to monitor the directories specified in the list and logs the events in a specified text file.
 
Install using `pip`:

```Python
pip install watchdog # Or pip3 install watchdog
```

Install from PyPI using `pip`:

```Python
python -m pip install -U watchdog
```


## Usage

To use this program, all you need to do is change the paths below in the "__`main.py`__" to the corresponding paths on your PC.

```Python
# NOTE: GENERAL FOLDER NAMING CONVENTION:
### NOTE -- Ensure to include "2 (TWO)" backslash in ALL PATHS BELOW 
### NOTE -- e.g "C:\Users\explo\Desktop" should be "C:\\Users\\explo\\Desktop"

# Include directory or directories you want to moitor within double quotes and square brackets: directories_to_watch = ["your_dir"]
# Seperate Multiple directories with comma ',' e.g directories_to_watch = ["C:\\your_dir_1", "F:\\your_dir_2"]
directories_to_watch = ["C:\\your_dir_1", "C:\\your_dir_2", "F:\\your_dir_3", "F:\\your_dir_4"]
path_to_write = "C:\\your_dir_5" # Ensure this path is not included in watched directory above
file_name = "filesystem_monitoring.txt" # The filename you want to use to store the event log
storage_path = path_to_write + '\\' + file_name
# Replace path to this "main.py" file with your systems path to "main.py" to start program when you Login
start_file_on_login_path = "C:\\Users\\username\\path_to_main.py_file_on_your_pc\\filesystem_monitoring\\src\\main.py"
# Replace with your startup folder path -> press WinKey + R, then type shell:startup and hit enter to get path.
startup_path = 'C:\\Users\\username\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
```




