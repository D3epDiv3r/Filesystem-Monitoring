# Filesystem-Monitoring
A basic Filesystem or Directory Event Monitoring tool for Windows built using Python's API Library "[Watchdog](https://github.com/gorakhargosh/watchdog)".

Works on Python 3+.

This program uses Tkinter as the control center interface to help start and stop the observers. It also uses multiprocessing to process multiple directories event handlers.


## Dependencies

This module depends on the [Watchdog](https://github.com/gorakhargosh/watchdog) Library to monitor the directories specified in the list and logs the events in a specified text file. Install via pip:

```python
pip install watchdog
```

