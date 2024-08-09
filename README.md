# WifiJammer

WifiJammer works on python3. It use the different library of python like threading, subprocess, time, tkinter etc. It also use Aircrack-ng tool.

Aircrack-ng is a complete suite of tools to assess WiFi network security. We can use it for scanning and sending different type of packets wirelessly. https://www.aircrack-ng.org/

Video demonstration Link: https://www.linkedin.com/posts/pranav-gajjar_python-ethicalhacking-wifijammer-activity-6688490914454753280-dqGQ

## Requirement 
* Wifi Adapter (Support Monitor Mode)
* python3
* Library of python: os, sys, subprocess, time, threading, random, csv, tkinter, time

## How to run WifiJammer:
* python3 WifiJammer.py (For automatic Command Line script)
* python3 WifiJammerGUI.py (For Graphical User Interface)

## How it works!!

For Command Line INterface:
* run the above code and then enter the interface name. It will automatically start disconnecting near by devices.

For GRaphical User Interface:
* First enter your wifi adapter name and click on start scan button. It will use airodump-ng tool to scan near by router and near by devices.
* It will show near by router and nearby devices in tabular form and in every row there is a button. If you click on that button it will disconnect that device using aireplay-ng tool.
* You can again click on start scan button for rescanning near by router and devices.

## Note: This is only for education purpose if you misuse then you are responsible for any cause.
