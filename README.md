# Filesystem-Monitoring
A basic Filesystem or Directory Event Monitoring tool for Windows built using Python's API Library "[Watchdog](https://github.com/gorakhargosh/watchdog)".

Works on Python 3+.

This program uses Tkinter as the control center interface to help start and stop the observers. It also uses multiprocessing to process multiple directories event handlers. It has a basic start-up functionality to start the program whenever you Login, this can be easily disabled (instruction [below](https://github.com/Chefcury1/Filesystem-Monitoring#disable-startup-functionality)). 


## Supported Platforms
- Windows

A pull request will be appreciated for any other platform integration.

## Installation

This module depends on the [Watchdog](https://github.com/gorakhargosh/watchdog) Library to monitor the directories specified in the list and logs the events in a specified text file. 
Install using `pip`:

```Python
pip install watchdog # Or pip3 install watchdog
```

Install from PyPI using `pip`:

```Python
python -m pip install -U watchdog
```





