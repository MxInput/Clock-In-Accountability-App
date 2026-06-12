## Clock In: An Accountability App

An accountability app that asks the user to check in every hour with what they did.

<img width="662" height="388" alt="clock_in_capture" src="https://github.com/user-attachments/assets/1e1c996c-826f-4b32-aaa6-85c3ef3e5146" />

### Video Demonstration
https://github.com/user-attachments/assets/e619de67-2d15-4f46-ac66-a25b2b6bfcd6

### Features
- Acts as a diary to write in what you've done for the past hour.
- Stores the acitvities that were done that day in one tab.
- View activities done on past days from another tab.
- Saves all entries and the last time you "clocked in".

### Downloading

Get it here: https://github.com/MxInput/Clock-In-Accountability-App/releases

### How to Build
Can be built by installing python and cloning the repository.
Then running the following in Powershell as an administrator. 

(Windows 10 instructions, I cannot confirm whether it works for other platforms)

```
pip install pyinstaller
Set-Location -Path "C:\Users\Path\to\folder\with\python\file"
pyinstaller --onefile -- windowed main.py
```
