# Convert-system-information-to-CSV-and-send-email-notification-Schedule

This is Python version 3.X

![License](https://img.shields.io/pypi/pyversions/3)


🚀Using Python
====
Installable Python kits, and information about using Python, are available at [python.org](https://www.python.org/)。

✏️project instruction
====

📦Install
pip automatic download & update
-------
This segment of code has already used several third-party libraries, but there is one more, the smtplib library, which is used to display progress bars within loops. If you don't have it installed on your system, you'll need to use pip to install it.
```
pip install secure-smtplib
```
```
pip install  schedule
```
warning!!

'secure-smtplib'' is a Windows-specific library used for file locking, which may cause issues if your program runs on other platforms.

Additionally, if you intend to use file locking on Windows, smtplib library is an option, but on other platforms, you may need to employ different methods to achieve file locking.

📦Pack
pip automatic download & update
-------
```
pip install pyinstaller
```
```
Convert-system-information-to-CSV-and-send-email-notification.py
```
This will generate a folder named dist in the current directory containing the packaged executable file.
