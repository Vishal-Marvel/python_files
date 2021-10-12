import tkinter as tk
import smtplib
import pynput.keyboard
import socket
import threading
import sys

root = tk.Tk()
root.title("mailer")
# file_name = sys._MEIPASS + "\mail.ico"
# root.wm_iconbitmap(file_name)
root.wm_iconbitmap("mail.ico")


def send_mail(email, to_mail, password, subject, message):
    message = "Subject:" + subject + "\n\n" + message
    display("Sending mail...")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, to_mail, message)
        server.quit()
        display("MAIL SENT")
        to_email_entry.delete(0, tk.END)
        subj_entry.delete(0, tk.END)
        msg_entry.delete(0, tk.END)
    except smtplib.SMTPAuthenticationError:
        display("**Username and Password incorrect**")
    except socket.gaierror:
        display("**No Internet**")
    except smtplib.SMTPRecipientsRefused:
        display("**To mail ID Required**")
    except TypeError:
        display("**Mail Field is required**")


def process_key(key):
    try:
        if key == key.enter:
            send_mail(email_entry.get(), to_email_entry.get(), pass_entry.get(), subj_entry.get(), msg_entry.get())
    except AttributeError:
        pass


def input_user():
    while True:
        try:
            key = pynput.keyboard.Listener(on_press=process_key)
            with key:
                key.join()
        except Exception:
            pass


def display(value):
    msg_label_top = tk.Label(frame, borderwidth=3, text=value, relief="groove", font=('bold', 15))
    msg_label_top.place(rely=0.14, relwidth=1, relheight=0.1)


canvas = tk.Canvas(root, height=400, width=400, bg='light green')
canvas.pack()

frame = tk.Frame(root, bg="#80c1ff", bd=7)
frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

title = tk.Label(frame, bg="light green", font=('bold', 15))
title.place(relwidth=1, relheight=0.12)
title['text'] = "MAILER"

label = tk.Label(frame, text='Enter the required fields', borderwidth=3, relief="groove", font=10)
label.place(rely=0.14, relwidth=1, relheight=0.1)

email_label = tk.Label(frame, text='Your mail ID:', font=15)
email_label.place(rely=0.275, relwidth=0.257, relheight=0.08)

email_entry = tk.Entry(frame)
email_entry.place(rely=0.275, relx=0.3, relwidth=0.7, relheight=0.08)

pass_label = tk.Label(frame, text='Password:', font=5)
pass_label.place(rely=0.375, relwidth=0.257, relheight=0.08)

pass_entry = tk.Entry(frame, show='*')
pass_entry.place(rely=0.375, relx=0.3, relwidth=0.7, relheight=0.08)

to_email_label = tk.Label(frame, text='To Email ID:', font=15)
to_email_label.place(rely=0.475, relwidth=0.257, relheight=0.08)

to_email_entry = tk.Entry(frame)
to_email_entry.place(rely=0.475, relx=0.3, relwidth=0.7, relheight=0.08)

subj_label = tk.Label(frame, text='Subject:', font=15)
subj_label.place(rely=0.575, relwidth=0.257, relheight=0.08)

subj_entry = tk.Entry(frame)
subj_entry.place(rely=0.575, relx=0.3, relwidth=0.7, relheight=0.08)

msg_label = tk.Label(frame, text='Message:', font=15)
msg_label.place(rely=0.75, relwidth=0.257, relheight=0.08)

msg_entry = tk.Entry(frame)
msg_entry.place(rely=0.675, relx=0.3, relwidth=0.7, relheight=0.24)

submit = tk.Button(frame, text='Submit', font=5,
                   command=lambda: send_mail(email_entry.get(), to_email_entry.get(), pass_entry.get(),
                                             subj_entry.get(), msg_entry.get()))
submit.place(rely=0.925, relx=0.45, relwidth=0.19, relheight=0.08)


threading.Thread(target=input_user).start()
root.mainloop()
