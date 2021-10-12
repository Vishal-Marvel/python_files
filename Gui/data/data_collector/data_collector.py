import tkinter as tk
from tkinter import ttk
import pickle
import sys
import os
from cryptography.fernet import Fernet
import datetime
import random
from tkcalendar import DateEntry


try:
    os.mkdir("data")
    f_path = os.getcwd() + "\data"
    with open(f_path + "\data.usr", "w"):
        pass
except FileExistsError:
    pass

root = tk.Tk()
root.title("data collector")
root.geometry("350x350")


def key():
    file_path = os.getcwd() + "\\data\\"
    if os.path.exists(file_path + "key.key"):
        return open(file_path + "key.key", "rb").read()
    else:
        key = Fernet.generate_key()
        with open(file_path + "key.key", "wb") as key_file:
            key_file.write(key)
        return open(file_path + "key.key", "rb").read()


def encrypt(filename):
    f = Fernet(key())
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt(filename):
    f = Fernet(key())
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)


def write_file(path, content):
    file_path = os.getcwd() + "\\data\\"
    if os.path.exists(file_path + path + ".details"):
        a_file = open(file_path + path + ".details", "wb")
        pickle.dump(content, a_file)
        a_file.close()
        encrypt(file_path + path + ".details")
    else:
        file = open(file_path + "data.usr", "a+")
        file.write("\n" + path)
        file.close()
        a_file = open(file_path + path + ".details", "wb")
        pickle.dump(content, a_file)
        a_file.close()
        encrypt(file_path + path + ".details")


def read_file(path):
    file_path = os.getcwd() + "\\data\\" + path + ".details"
    decrypt(file_path)
    a_file = open(file_path, "rb")
    output = pickle.load(a_file)
    a_file.close()
    encrypt(file_path)
    return output


def colour():
    color = ['light yellow', 'grey70', 'light green', 'light blue', 'gold', 'orange', 'DarkOliveGreen1']
    return random.choice(color)


class User_Pass:
    def __init__(self):
        self.add_user = Add_user()
        self.show = Show_details()
        self.details = Reader()

    def chk_user_pass(self, user, password):
        try:
            if user == '' or password == '':
                self.display("Enter all the fields", colour())
            else:
                content_dict = read_file(user)
                if content_dict["pass"] == password:
                    self.show.screen(user)
                else:
                    self.display("Incorrect Password", 'red')
        except FileNotFoundError:
            self.display("No such user exists", colour())

    def display(self, value, clr):
        msg_label_top = tk.Label(self.frame, borderwidth=3, bg=clr, text=value, relief="groove", font=('bold', 15))
        msg_label_top.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)

    def screen(self):

        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="DATA COLLECTOR")
        title.place(relwidth=1, relheight=0.16)

        label = tk.Label(self.frame, text='Enter the required fields', borderwidth=3, relief="groove", font=10)
        label.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)

        email_label = tk.Label(self.frame, text='UserName:', font=15)
        email_label.place(rely=0.4, relwidth=0.257, relheight=0.08)

        self.email_entry = tk.Entry(self.frame, font=14)
        self.email_entry.place(rely=0.4, relx=0.3, relwidth=0.665, relheight=0.08)
        self.email_entry.focus()

        pass_label = tk.Label(self.frame, text='Password:', font=5)
        pass_label.place(rely=0.55, relwidth=0.257, relheight=0.08)

        self.pass_entry = tk.Entry(self.frame, show='*', font=14)
        self.pass_entry.place(rely=0.55, relx=0.3, relwidth=0.665, relheight=0.08)

        submit = tk.Button(self.frame, text='Submit', font=5,
                           command=lambda: self.chk_user_pass(self.email_entry.get(), self.pass_entry.get()))
        submit.place(rely=0.75, relx=0.5, relwidth=0.19, relheight=0.08)

        new_user = tk.Button(self.frame, text='Add User', font=5, command=lambda: self.add_user.screen())
        new_user.place(rely=0.75, relx=0.2, relwidth=0.25, relheight=0.08)

        go_to_reader = tk.Button(self.frame, text='User Details', font=5, command=lambda: self.details.screen())
        go_to_reader.place(rely=0.89, relx=0.35, relwidth=0.3, relheight=0.08)


class Add_user:
    def __init__(self):
        global user_p

    def display(self, value, clr):
        msg_label_top = tk.Label(self.main_frame, borderwidth=3, bg=clr, text=value, relief="groove", font=('bold', 12))
        msg_label_top.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.13)

    def write_data(self):
        if self.pass_entry.get() and self.email_entry.get() and self.dob_entry.get_date() \
                and self.confirm_pass_entry.get() and self.qual_entry.get() \
                and self.occu_entry.get() and self.ph_no.get():
            file_path = os.getcwd() + "\\data\\"
            if os.path.exists(file_path + self.email_entry.get() + ".details"):
                self.display("User already exists", colour())
                self.email_entry.focus()
            else:
                if self.pass_entry.get() == self.confirm_pass_entry.get():
                    if len(self.pass_entry.get()) >= 8:
                        if self.dob_entry.get_date() <= datetime.date.today():
                            if self.ph_no.get().isdigit():
                                if len(self.ph_no.get()) == 10:
                                    content = {'user': self.email_entry.get(), 'pass': self.pass_entry.get(), 'dob': self.dob_entry.get(),
                                               'qual': self.qual_entry.get(), 'occu': self.occu_entry.get(), 'ph_no': self.ph_no.get()}
                                    write_file(self.email_entry.get(), content)
                                    self.display("User created, \nclick Return to LOG IN", colour())
                                    self.email_entry.delete(0, tk.END)
                                    self.pass_entry.delete(0, tk.END)
                                    self.confirm_pass_entry.delete(0, tk.END)
                                    self.dob_entry.set_date(datetime.date.today())
                                    self.qual_entry.delete(0, tk.END)
                                    self.occu_entry.delete(0, tk.END)
                                    self.ph_no.delete(0, tk.END)
                                    self.email_entry.focus()
                                else:
                                    self.display("PHONE NO. MUST HAVE 10 DIGITS", colour())
                                    self.ph_no.focus()
                            else:
                                self.display("PHONE NO. SHD NOT HAVE ALPHABETS", colour())
                                self.ph_no.focus()
                        else:
                            self.display("DOB MUST BE LESS THAN TODAY", colour())
                    else:
                        self.display("Password length must be\nminimum 8", colour())
                        self.pass_entry.focus()
                else:
                    self.display("Password is not matched", colour())
                    self.pass_entry.focus()
        else:
            self.display("ALL FIELDS ARE REQUIRED", colour())
            self.email_entry.focus()

    def screen(self):

        self.main_frame = tk.Frame(root, bg="#80c1ff", bd=5)
        self.main_frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.main_frame, bg="light green", font=('bold', 15), text="ADDING USER")
        title.place(relwidth=1, relheight=0.13)

        label = tk.Label(self.main_frame, text='Enter all the fields', relief="groove", font=('bold', 12))
        label.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.1)

        frame = tk.Frame(root, bg='#80c1ff')
        frame.place(relx=0.001, rely=0.3, relheight=0.58, relwidth=1)

        scroll_bar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(frame, yscrollcommand=scroll_bar.set, height=195, width=326, bg="#80c1ff", bd=0,
                           highlightthickness=0)
        canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        scroll_bar.configure(command=canvas.yview)

        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        second_frame = tk.Frame(canvas, bg="#80c1ff")
        second_frame.place(relx=0.001, rely=0.001, relheight=1, relwidth=1)

        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        canvas.create_window((0, 0), window=second_frame, anchor='nw')

        tk.Label(second_frame, text='UserName:', font=15).grid(row=0, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.email_entry = tk.Entry(second_frame, font=15, justify='center')
        self.email_entry.grid(row=0, column=1, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)
        self.email_entry.focus()

        tk.Label(second_frame, text='Password:', font=5).grid(row=1, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.pass_entry = tk.Entry(second_frame, font=14, justify='center', show='*')
        self.pass_entry.grid(row=1, column=1, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Label(second_frame, text='Confirm\nPassword:', font=5).grid(row=2, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.confirm_pass_entry = tk.Entry(second_frame, font=(14), justify='center', show='*')
        self.confirm_pass_entry.grid(row=2, column=1, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Label(second_frame, text='Qualification', font=3).grid(row=4, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.qual_entry = tk.Entry(second_frame, font=14, justify='center')
        self.qual_entry.grid(row=4, column=1, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Label(second_frame, text='Occupation', font=3).grid(row=5, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.occu_entry = tk.Entry(second_frame, font=14, justify='center')
        self.occu_entry.grid(row=5, column=1, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Label(second_frame, text='DOB:', font=('bold', 13)).grid(row=3, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        tk.Label(second_frame, text='Phone No.:', font=3).grid(row=6, column=0, padx=10, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.ph_no = tk.Entry(second_frame, font=14, justify='center')
        self.ph_no.grid(row=6, column=1, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        self.dob_entry = DateEntry(second_frame, width=25,justify='center',date_pattern='dd/mm/yyyy', background='darkblue', foreground='white', borderwidth=2)
        self.dob_entry.grid(row=3, column=1, pady=10, sticky=tk.N+tk.S+tk.E+tk.W)

        for x in range(2):
            tk.Grid.columnconfigure(canvas, x, weight=1)

        for y in range(7):
            tk.Grid.rowconfigure(canvas, y, weight=1)

        submit = tk.Button(self.main_frame, text='Submit', font=('bold', 15), command=lambda: self.write_data())
        submit.place(rely=0.9, relx=0.48, relwidth=0.2, relheight=0.1)

        return_to = tk.Button(self.main_frame, text='Return', font=('bold', 15), command=lambda: user_p.screen())
        return_to.place(rely=0.9, relx=0.25, relwidth=0.2, relheight=0.1)

    pass


class Show_details:

    def __init__(self):
        global user_p

    def conform(self, email):
        confirm = tk.Button(self.main_frame, text='Confirm?', font=15, bg='red', command=lambda: delete(email))
        confirm.place(rely=0.875, relx=0.266, relwidth=0.2, relheight=0.12)

        change = tk.Label(self.main_frame, bg="#80c1ff", font=15)
        change.place(rely=0.875, relx=0.012, relwidth=0.22, relheight=0.12)

        reset_pass = tk.Label(self.main_frame, bg="#80c1ff", font=15)
        reset_pass.place(rely=0.875, relx=0.78, relwidth=0.2, relheight=0.12)

        return_to = tk.Button(self.main_frame, text='Return', font=15, command=lambda: self.screen(email))
        return_to.place(rely=0.875, relx=0.49, relwidth=0.26, relheight=0.12)

        def delete(file):
            f = ''
            file_path = os.getcwd() + "\\data\\"
            a_file = open(file_path + "data.usr", "r")
            files = a_file.read()
            a_file.close()
            for i in files.split("\n"):
                if i == file:
                    continue
                f += "\n" + i
            os.remove(file_path + "data.usr")
            r_file = open(file_path + "data.usr", "w")
            r_file.write(f)
            r_file.close()
            os.remove(file_path + file + ".details")
            user_p.screen()

    def display(self, value, clr):
        msg_label_top = tk.Label(self.main_frame, borderwidth=3, text=value, bg=clr,
                                 relief="groove", font=('bold', 13))
        msg_label_top.place(relx=0.165, rely=0.16, relheight=0.1, relwidth=0.7)

    def display_(self, value, clr):
        msg_label_top = tk.Label(self.frame1, borderwidth=3, text=value, bg=clr,
                                 relief="groove", font=('bold', 12))
        msg_label_top.place(relx=0.1, rely=0.0001, relwidth=0.7, relheight=0.13)

    def write_data(self, email, passw):
        if self.dob_entry_.get_date() and self.qual_entry_.get() and self.occu_entry_.get() and self.ph_no_.get():
            if self.dob_entry_.get_date() <= datetime.date.today():
                if self.ph_no_.get().isdigit():
                    if len(self.ph_no_.get()) == 10:
                        content = {'user': email, 'pass': passw, 'dob': self.dob_entry_.get(),
                                   'qual': self.qual_entry_.get(), 'occu': self.occu_entry_.get(), 'ph_no': self.ph_no_.get()}
                        write_file(email, content)
                        self.screen(email)
                    else:
                        self.display("PHONE NO. MUST HAVE 10 DIGITS", colour())
                else:
                    self.display("PHONE NO. SHD NOT HAVE ALPHABETS", colour())
            else:
                self.display("DOB MUST BE LESS THAN TODAY", colour())
                self.dob_entry_.focus()
        else:
            self.display("ALL FIELDS ARE REQUIRED", colour())

    def write_data_pass(self, email, dob, passw, qual, occu, ph_no):
        if self.old_pass.get():
            if self.old_pass.get() == passw:
                if self.reset_pass_entry.get() != passw:
                    if self.reset_pass_entry.get() == self.reset_confirm_pass_entry.get():
                        if len(self.reset_pass_entry.get()) >= 8:
                            content = {'user': email, 'pass': self.reset_pass_entry.get(), 'dob': dob, 'qual': qual,
                                       'occu': occu, 'ph_no': ph_no}
                            write_file(email, content)
                            empty = tk.Label(self.frame1, bg="#80c1ff")
                            empty.place(relheight=0.85, relwidth=1)
                            save = tk.Label(self.main_frame, bg="#80c1ff", font=15)
                            save.place(rely=0.85, relx=0.15, relwidth=0.35, relheight=0.1)
                            self.display_('Password changed\nclick return to continue', colour())
                            return_to = tk.Button(self.main_frame, text='Return', font=15,
                                                  command=lambda: user_p.screen())
                            return_to.place(rely=0.85, relx=0.6, relwidth=0.2, relheight=0.1)
                        else:
                            self.display_("Password length must be\nminimum 8", colour())
                            self.reset_pass_entry.focus()
                    else:
                        self.display_('Password is not matched', colour())
                        self.reset_pass_entry.focus()
                else:
                    self.display_('New password should be different\nfrom the old password', colour())
                    self.reset_pass_entry.focus()
            else:
                self.display_('Old password is incorrect', 'red')
                self.old_pass.focus()
        else:
            self.display_('Please enter the password', colour())
            self.old_pass.focus()

    def reset_password(self, email, dob, passw, qual, occu, ph_no):
        self.frame1 = tk.Frame(self.main_frame, bg="#80c1ff")
        self.frame1.place(relx=0.55, rely=0.17, relwidth=1.123, relheight=0.9, anchor='n')
        self.old_pass = tk.Entry(self.frame1, show='*')
        self.reset_pass_entry = tk.Entry(self.frame1, show='*')
        self.reset_confirm_pass_entry = tk.Entry(self.frame1, show='*')

        old_pass = tk.Label(self.frame1, text='Old\nPassword:', font=5)
        old_pass.place(relx=0.03, rely=0.18, relwidth=0.257, relheight=0.12)

        self.old_pass.place(rely=0.18, relx=0.3, relwidth=0.56, relheight=0.1)
        self.old_pass.focus()

        pass_label = tk.Label(self.frame1, text='New\nPassword:', font=5)
        pass_label.place(relx=0.03, rely=0.35, relwidth=0.257, relheight=0.15)

        self.reset_pass_entry.place(rely=0.38, relx=0.3, relwidth=0.56, relheight=0.1)

        confirm_pass_label = tk.Label(self.frame1, text='Confirm\nPassword:', font=5)
        confirm_pass_label.place(relx=0.03, rely=0.53, relwidth=0.257, relheight=0.15)

        self.reset_confirm_pass_entry.place(rely=0.555, relx=0.3, relwidth=0.56, relheight=0.1)

        save = tk.Button(self.main_frame, text='Save Password', font=15,
                         command=lambda: self.write_data_pass(email, dob, passw, qual, occu, ph_no))
        save.place(rely=0.85, relx=0.15, relwidth=0.35, relheight=0.1)

        return_to = tk.Button(self.main_frame, text='Return', font=15, command=lambda: self.screen(email))
        return_to.place(rely=0.85, relx=0.6, relwidth=0.2, relheight=0.1)

    def change(self, email, dob, passw, qual, occu, ph_no):
        self.dob.destroy()
        self.qual.destroy()
        self.occu.destroy()
        self.ph_no.destroy()
        dob = str(dob)
        day = dob.split('-')[2]
        month = dob.split('-')[1]
        year = dob.split('-')[0]
        self.qual_entry_ = tk.Entry(self.second_frame, font=('bold', 13), justify='left')
        self.qual_entry_.grid(row=2, column=1, pady=10)
        self.occu_entry_ = tk.Entry(self.second_frame, font=('bold', 13), justify='left')
        self.occu_entry_.grid(row=3, column=1, pady=10)
        self.ph_no_ = tk.Entry(self.second_frame, font=('bold', 13), justify='left')
        self.ph_no_.grid(row=4, column=1, pady=10)
        self.dob_entry_ = DateEntry(self.second_frame, height=10, width=25, date_pattern="dd/mm/yyyy", justify='center', bg='darkblue', fg='white', borderwidth=2, year=int(year), month=int(month), day=int(day))
        self.dob_entry_.grid(row=1, column=1, pady=10)

        self.ph_no_.insert(0, ph_no)
        self.qual_entry_.insert(0, qual)
        self.occu_entry_.insert(0, occu)

        delete = tk.Label(self.main_frame, bg="#80c1ff", font=15)
        delete.place(rely=0.875, relx=0.012, relwidth=0.22, relheight=0.12)

        reset_pass = tk.Label(self.main_frame, bg="#80c1ff", font=15)
        reset_pass.place(rely=0.875, relx=0.78, relwidth=0.2, relheight=0.12)

        save = tk.Button(self.main_frame, text='Save\nDetails', font=15,
                         command=lambda: self.write_data(email, passw))
        save.place(rely=0.875, relx=0.266, relwidth=0.2, relheight=0.12)

        return_to = tk.Button(self.main_frame, text='Return', font=15, command=lambda: self.screen(email))
        return_to.place(rely=0.875, relx=0.49, relwidth=0.26, relheight=0.12)

    def screen(self, user):
        output = read_file(user)
        email, dob, qual, occu, passw, ph_no = output['user'], output['dob'], output['qual'], output['occu'], output['pass'], output['ph_no']
        self.main_frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.main_frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.main_frame, bg="light green", font=('bold', 15), text="USER DETAILS", borderwidth=3,
                         relief="groove")
        title.place(relwidth=1, relheight=0.13)

        frame = tk.Frame(self.main_frame)
        frame.place(relx=0.001, rely=0.255)

        canvas = tk.Canvas(frame, height=180, width=326, bg="#80c1ff")
        canvas.pack(side=tk.LEFT, expand=1)

        scroll_bar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        canvas.configure(yscrollcommand=scroll_bar.set, bd=0, highlightthickness=0)

        self.second_frame = tk.Frame(canvas, bg="#80c1ff")
        self.second_frame.place(relheight=1, relwidth=1)

        canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        return_to = tk.Button(self.main_frame, text='Return', font=15,
                              command=lambda: user_p.screen())
        return_to.place(rely=0.875, relx=0.78, relwidth=0.2, relheight=0.12)

        delete = tk.Button(self.main_frame, text='Delete\ndetails', font=15,
                           command=lambda: self.conform(email))
        delete.place(rely=0.875, relx=0.266, relwidth=0.2, relheight=0.12)

        change = tk.Button(self.main_frame, text='Change\nDetails', font=15,
                           command=lambda: self.change(email, dob, passw, qual, occu, ph_no))
        change.place(rely=0.875, relx=0.012, relwidth=0.22, relheight=0.12)

        reset_pass = tk.Button(self.main_frame, text='Reset\nPassword', font=15,
                               command=lambda: self.reset_password(email, dob, passw, qual, occu, ph_no))
        reset_pass.place(rely=0.875, relx=0.49, relwidth=0.26, relheight=0.12)

        tk.Label(self.second_frame, text=' UserName: ', font=10, borderwidth=3).grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text=email, borderwidth=3, font=15).grid(row=0, column=1, pady=10)

        tk.Label(self.second_frame, text='      DOB:      ', font=10, borderwidth=3).grid(row=1, column=0, padx=10,
                                                                                          pady=10)

        self.dob = tk.Label(self.second_frame, text=dob, borderwidth=3, font=15)
        self.dob.grid(row=1, column=1, pady=10)

        tk.Label(self.second_frame, text=' Qualification: ', font=10).grid(row=2, column=0, padx=10, pady=10)

        self.qual = tk.Label(self.second_frame, text=qual, borderwidth=3, font=15)
        self.qual.grid(row=2, column=1, pady=10)

        tk.Label(self.second_frame, text=' Occupation: ', font=10).grid(row=3, column=0, padx=10, pady=10)

        self.occu = tk.Label(self.second_frame, text=occu, borderwidth=3, font=15)
        self.occu.grid(row=3, column=1, pady=10)

        tk.Label(self.second_frame, text=' Phone No.: ', font=10).grid(row=4, column=0, padx=10, pady=10)

        self.ph_no = tk.Label(self.second_frame, text=ph_no, borderwidth=3, font=15)
        self.ph_no.grid(row=4, column=1, pady=10)

    pass


class Reader:

    def word_list(self):
        path = os.getcwd() + "\data\data.usr"
        word = []
        try:
            with open(path, "r") as file:
                for line in file:
                    line = line.rstrip()
                    if line:
                        word.append(line)
        except FileNotFoundError:
            head = tk.Label(self.frame, bg="yellow", text="NO ENTRIES FOUND")
            head.place(relx=0.25, rely=0.475, relheight=0.07, relwidth=0.45)
        return word

    def output(self, user_name):
        user_p.screen()
        user_p.email_entry.insert(0, user_name)
        user_p.pass_entry.focus()

    def search(self, start=0, end=5):
        name_list = self.word_list()
        search_list = []
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.42, relwidth=1, relheight=0.58)
        if self.search_field.get():
            for i in name_list:
                if self.search_field.get().lower() in i:
                    search_list.append(i)
            k = start
            j = 0
            word = search_list
            if len(search_list) > 0:
                for i in word[start:end]:
                    try:
                        details = read_file(i)
                        s = tk.Label(frame, text=str(k + 1))
                        s.place(relx=0.23, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
                        name = tk.Button(frame, text=details['user'], command=lambda id=details['user']: self.show_details(id))
                        name.place(relx=0.45, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.35)
                        j += 1
                        k += 1
                    except FileNotFoundError:
                        pass
            else:
                no_data = tk.Label(frame, text="NO DATA FOUND", font=15)
                no_data.place(rely=0.25, relx=0.3, relwidth=0.4, relheight=0.2)
        else:
            no_data = tk.Label(frame, text="SEARCH FIELD IS EMPTY", font=('bold', 11))
            no_data.place(rely=0.25, relx=0.22, relwidth=0.55, relheight=0.2)
        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(search_list) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.search(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.search(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def show_details(self, user_name):
        output = read_file(user_name)
        try:
            email, dob, qual, occu, passw, ph_no = output['user'], output['dob'], output['qual'], output['occu'], output['pass'], output['ph_no']
        except KeyError:
            email, dob, qual, occu, passw, ph_no = output['user'], output['dob'], output['qual'], output['occu'], \
                                                   output['pass'], "1234567890"
            
        self.main_frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.main_frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.main_frame, bg="light green", font=('bold', 15), text="USER DETAILS", borderwidth=3,
                         relief="groove")
        title.place(relwidth=1, relheight=0.13)

        frame = tk.Frame(self.main_frame)
        frame.place(relx=0.001, rely=0.255)

        canvas = tk.Canvas(frame, height=180, width=326, bg="#80c1ff")
        canvas.pack(side=tk.LEFT, expand=1)

        scroll_bar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        canvas.configure(yscrollcommand=scroll_bar.set, bd=0, highlightthickness=0)

        self.second_frame = tk.Frame(canvas, bg="#80c1ff")
        self.second_frame.place(relheight=1, relwidth=1)

        canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        return_to = tk.Button(self.main_frame, text='Return', font=15,
                              command=lambda: self.screen())
        return_to.place(rely=0.875, relx=0.78, relwidth=0.2, relheight=0.12)

        login = tk.Button(self.main_frame, text='Login', font=15,
                               command=lambda: self.output(email))
        login.place(rely=0.875, relx=0.49, relwidth=0.26, relheight=0.12)

        tk.Label(self.second_frame, text=' UserName: ', font=10, borderwidth=3).grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text=email, borderwidth=3, font=15).grid(row=0, column=1, pady=10)

        tk.Label(self.second_frame, text='      DOB:      ', font=10, borderwidth=3).grid(row=1, column=0, padx=10,
                                                                                          pady=10)

        tk.Label(self.second_frame, text=dob.strftime('%d/%m/%Y'), borderwidth=3, font=15).grid(row=1, column=1, pady=10)

        tk.Label(self.second_frame, text=' Qualification: ', font=10).grid(row=2, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text=qual, borderwidth=3, font=15).grid(row=2, column=1,  pady=10)

        tk.Label(self.second_frame, text=' Occupation: ', font=10).grid(row=3, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text=occu, borderwidth=3, font=15).grid(row=3, column=1, pady=10)

        tk.Label(self.second_frame, text=' Phone No.: ', font=10).grid(row=4, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text=ph_no, borderwidth=3, font=15).grid(row=4, column=1, pady=10)

    def output_name(self, start=0, end=5):
        k = start
        j = 0
        word = self.word_list()
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.42, relwidth=1, relheight=0.58)
        for i in word[start:end]:
            try:
                details = read_file(i)
                s = tk.Label(frame, text=str(k + 1))
                s.place(relx=0.23, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
                name = tk.Button(frame, text=details['user'], command=lambda id=details['user']: self.show_details(id))
                name.place(relx=0.45, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.35)
                j += 1
                k += 1
            except FileNotFoundError:
                pass

        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: user_p.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(word) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.output_name(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.output_name(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def screen(self):
        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="DATA READER")
        title.place(relwidth=1, relheight=0.12)

        title_1 = tk.Label(self.frame, bg="light green", font=('bold', 15), text="USER NAME Details")
        title_1.place(rely=0.135, relx=0.1, relwidth=0.8, relheight=0.1)

        self.search_field = tk.Entry(self.frame, font=15)
        self.search_field.place(relx=0.07, rely=0.26, relheight=0.08, relwidth=0.65)
        self.search_field.focus()

        search = tk.Button(self.frame, text="search", command= lambda : self.search())
        search.place(relx=0.8, rely=0.26, relheight=0.08, relwidth=0.15)

        head = tk.Label(self.frame, bg="#80c1ff", text="S.No.")
        head.place(relx=0.23, rely=0.35, relheight=0.07, relwidth=0.1)

        head_1 = tk.Label(self.frame, bg="#80c1ff", text="Name")
        head_1.place(relx=0.5, rely=0.35, relheight=0.07, relwidth=0.25)

        self.output_name()

    pass


user_p = User_Pass()
user_p.screen()
root.mainloop()
