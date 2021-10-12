import time
import tkinter as tk
from tkinter import ttk
import sqlite3
import mysql.connector
import datetime, random
import threading, os
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from tkinter import *

try:
    my_sql = mysql.connector.connect(host='localhost', user='root', passwd='vishal@sql@123', database='data_collector')
except mysql.connector.errors.DatabaseError:
    my_sql = sqlite3.connect('Data_collector.db')

my_cursor = my_sql.cursor()

root = tk.Tk()
root.title("Data collector sql")
root.geometry("350x350")
sql_command = """create table if not exists user_details(login_id varchar(30) primary key, user_name varchar(30), password varchar(30) , dob char(10), age integer default 0, qual varchar(30), occu varchar(30),
                ph_no integer, filename varchar(50), data longblob);"""
my_cursor.execute(sql_command)


def calculate_age(dob):
    date = dob.split('/')[0]
    month = dob.split('/')[1]
    year = dob.split('/')[2]
    try:
        n = datetime.date(int(year), int(month), int(date))
        today = datetime.date.today()
        if not n > today:
            year = today.year - n.year - ((today.month, today.day) < (n.month, n.day))
            return year
        else:
            return 0
    except ValueError:
        pass


def read_file(l_id):
    read_command = "select * from user_details where login_id = '{}'".format(l_id)
    my_cursor.execute(read_command)
    result = my_cursor.fetchone()
    if result is not None:
        content = dict()
        content['l_id'], content['u_name'], content['pass'], content['dob'], content['age'], content['qual'], content[
            'occu'], content[
            'ph_no'], content['filename'], content['data'] = result[0], result[1], result[2], result[3], result[4], \
                                                             result[5], result[6], result[7], result[8], result[9]
        return content
    else:
        user_p.display("No such user exists", colour())


def write_file(content):
    l_id, u_name, passw, d_o_b, age, qual_, occu_, ph__no, file_name, data = content['l_id'], content['u_name'], \
                                                                             content['pass'], content[
                                                                                 'dob'], content['age'], content[
                                                                                 'qual'], content['occu'], content[
                                                                                 'ph_no'], content['filename'], content[
                                                                                 'data']

    values = (l_id, u_name, passw, d_o_b, age, qual_, occu_, ph__no, file_name, data)
    try:
        write_command = 'insert into user_details values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        my_cursor.execute(write_command, values)
    except sqlite3.OperationalError:
        write_command = 'insert into user_details values(?,?,?,?,?,?,?,?,?,?);'
        my_cursor.execute(write_command, values)
    my_sql.commit()


def colour():
    color = ['light yellow', 'grey70', 'light green', 'light blue', 'gold', 'orange', 'DarkOliveGreen1']
    return random.choice(color)


class CEntry(Entry):
    def __init__(self, parent, *args, **kwargs):
        Entry.__init__(self, parent, *args, **kwargs)
        self.changes = [""]
        self.steps = int()

        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut")
        self.context_menu.add_command(label="Copy")
        self.context_menu.add_command(label="Paste")
        self.context_menu.add_command(label="Redo", command=lambda: self.redo())
        self.context_menu.add_command(label="Undo", command=lambda: self.undo())

        self.bind("<Button-3>", self.popup)
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)

        self.bind("<Key>", self.add_changes)

    def focus_out(self):
        root.focus_force()

    def popup(self, event):
        self.context_menu.post(event.x_root, event.y_root)
        self.context_menu.entryconfigure("Cut", command=lambda: self.event_generate("<<Cut>>"))
        self.context_menu.entryconfigure("Copy", command=lambda: self.event_generate("<<Copy>>"))
        self.context_menu.entryconfigure("Paste", command=lambda: self.event_generate("<<Paste>>"))

    def undo(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            self.delete(0, END)
            self.insert(END, self.changes[self.steps])

    def redo(self, event=None):
        if self.steps < len(self.changes):
            self.delete(0, END)
            self.insert(END, self.changes[self.steps])
            self.steps += 1

    def add_changes(self, event=None):
        if self.get() != self.changes[-1]:
            self.changes.append(self.get())
            self.steps += 1


class Add_menu_bar:
    def __init__(self):
        global user_p
        self.create_menu()
        self.changes = [""]
        self.steps = int()

    def create_menu(self):
        self.my_menu = tk.Menu(root)
        root.config(menu=self.my_menu)
        self.file_menu_create()
        # self.edit_menu_create()

    def file_menu_create(self):
        self.file_menu = tk.Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Login Page", command=lambda: self.create_new())
        self.file_menu.add_command(label="Add User", command=lambda: user_p.add_user.screen())
        self.file_menu.add_command(label="User Details", command=lambda: user_p.details.screen())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy, accelerator="(Ctrl+Q)")
        self.file_menu.bind_all("<Control-q>", lambda e: root.destroy())

    def edit_menu_create(self):
        self.edit_menu = tk.Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut")
        self.edit_menu.add_command(label="Copy")
        self.edit_menu.add_command(label="Paste")
        self.edit_menu.add_command(label="Redo", command=lambda: self.redo())
        self.edit_menu.add_command(label="Undo", command=lambda: self.undo())
        self.edit_menu.entryconfigure("Cut", command=lambda: root.focus_get().event_generate("<<Cut>>"))
        self.edit_menu.entryconfigure("Copy", command=lambda: root.focus_get().event_generate("<<Copy>>"))
        self.edit_menu.entryconfigure("Paste", command=lambda: root.focus_get().event_generate("<<Paste>>"))

    def undo(self, event=None):
        if self.steps != 0:
            self.steps -= 1
            root.focus_get().delete(0, END)
            root.focus_get().insert(END, self.changes[self.steps])

    def redo(self, event=None):
        if self.steps < len(self.changes):
            root.focus_get().delete(0, END)
            root.focus_get().insert(END, self.changes[self.steps])
            self.steps += 1

    def add_changes(self, event=None):
        if root.focus_get().get() != self.changes[-1]:
            self.changes.append(self.get())
            self.steps += 1

    def create_new(self, event=None):
        global root, user_p
        user_p.screen()


class User_Pass:
    def __init__(self):

        self.add_user = Add_user()
        self.show = Show_details()
        self.details = Searcher()
        self.stopper = False

    def chk_user_pass(self, event='event'):
        user, password = self.login_id.get(), self.pass_entry.get()
        if user == '' or password == '' or user == 'Login ID' or password == 'Password':
            self.display("Enter all the fields", colour())
        else:
            read_command = "select login_id, password from user_details where login_id = '{}'".format(user)
            my_cursor.execute(read_command)
            result = my_cursor.fetchone()
            if result is not None:
                l_id, password_key = result[0], result[1]
                if password_key == password:
                    self.show.screen(l_id)
                    self.stopper = True
                else:
                    self.display("Incorrect Password", 'red')
            else:
                self.display("No such User Exists", colour())

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

        def entry2_focus(event):
            self.stopper = False
            threading.Thread(target=hide).start()

        def hide():
            while True:
                if self.pass_entry.get():
                    tk.Label(self.frame, bg="#80c1ff").place(rely=0.75, relx=0.2, relwidth=0.25, relheight=0.08)
                    tk.Label(self.frame, bg="#80c1ff").place(rely=0.89, relx=0.35, relwidth=0.3, relheight=0.08)
                    break
                time.sleep(0.1)
            try:
                show()
            except RuntimeError:
                pass

        def show():
            while True:
                if self.pass_entry.get() == "":
                    new_user = tk.Button(self.frame, text='Add User', font=5, command=lambda: self.add_user.screen())
                    new_user.place(rely=0.75, relx=0.2, relwidth=0.25, relheight=0.08)
                    go_to_reader = tk.Button(self.frame, text='User Details', font=5,
                                             command=lambda: self.details.screen())
                    go_to_reader.place(rely=0.89, relx=0.35, relwidth=0.3, relheight=0.08)
                    hide()

                if self.stopper:
                    break
                time.sleep(0.1)

        email_label = tk.Label(self.frame, text='Login Id:', font=15)
        email_label.place(rely=0.4, relwidth=0.257, relheight=0.08)

        self.login_id = CEntry(self.frame, font=14)
        self.login_id.place(rely=0.4, relx=0.3, relwidth=0.665, relheight=0.08)
        self.login_id.focus_set()

        pass_label = tk.Label(self.frame, text='Password:', font=5)
        pass_label.place(rely=0.55, relwidth=0.257, relheight=0.08)

        self.pass_entry = CEntry(self.frame, font=14, show='*')
        self.pass_entry.place(rely=0.55, relx=0.3, relwidth=0.665, relheight=0.08)
        self.pass_entry.bind("<FocusIn>", entry2_focus)

        submit = tk.Button(self.frame, text='Submit', font=5, command=lambda: self.chk_user_pass())
        submit.place(rely=0.75, relx=0.5, relwidth=0.19, relheight=0.08)
        submit.bind_all("<Return>", self.chk_user_pass)

        new_user = tk.Button(self.frame, text='Add User', font=5, command=lambda: self.add_user.screen())
        new_user.place(rely=0.75, relx=0.2, relwidth=0.25, relheight=0.08)

        go_to_reader = tk.Button(self.frame, text='User Details', font=5, command=lambda: self.details.screen())
        go_to_reader.place(rely=0.89, relx=0.35, relwidth=0.3, relheight=0.08)

    pass


class Add_user:
    def __init__(self):
        global user_p
        self.stopper = False

    def display(self, value, clr):
        msg_label_top = tk.Label(self.main_frame, borderwidth=3, bg=clr, text=value, relief="groove", font=('bold', 12))
        msg_label_top.place(relx=0.1, rely=0.15, relwidth=0.8, relheight=0.13)

    def write_data(self, event='event'):
        if self.login_id.get() and self.pass_entry.get() and self.user_name.get() \
                and self.confirm_pass_entry.get() and self.qual_entry.get() \
                and self.occu_entry.get() and self.ph_no.get() \
                and self.filename != "" and self.data != "":
            if self.pass_entry.get() == self.confirm_pass_entry.get():
                if len(self.pass_entry.get()) >= 8:
                    if not (
                            self.date_box.get() == 'DD' or self.month_box.get() == 'MM' or self.year_box.get() == 'YYYY'):
                        self.dob_entry = self.date_box.get() + '/' + self.month_box.get() + '/' + self.year_box.get()
                        if self.ph_no.get().isdigit():
                            if len(self.ph_no.get()) == 10:
                                content = {'u_name': self.user_name.get(),
                                           'l_id': self.login_id.get(),
                                           'pass': self.pass_entry.get(),
                                           'dob': self.dob_entry,
                                           'age': calculate_age(self.dob_entry),
                                           'qual': self.qual_entry.get(), 'occu': self.occu_entry.get(),
                                           'ph_no': self.ph_no.get(),
                                           'filename': self.filename,
                                           'data': self.data}
                                try:
                                    write_file(content)
                                    self.display("User created, \nclick Return to LOG IN", colour())
                                    self.login_id.delete(0, tk.END)
                                    self.user_name.delete(0, tk.END)
                                    self.pass_entry.delete(0, tk.END)
                                    self.confirm_pass_entry.delete(0, tk.END)
                                    self.date_box.current(0)
                                    self.month_box.current(0)
                                    self.year_box.current(0)
                                    self.qual_entry.delete(0, tk.END)
                                    self.occu_entry.delete(0, tk.END)
                                    self.ph_no.delete(0, tk.END)
                                    self.destroy()
                                    self.stopper = False
                                # except sqlite3.IntegrityError:
                                except mysql.connector.IntegrityError:
                                    self.display("Login ID already exists", colour())
                            else:
                                self.display("PH NO. Must Have 10 Digits", colour())
                                self.ph_no.focus()
                        else:
                            self.display("PH NO. shd not have alphabets", colour())
                            self.ph_no.focus()
                    else:
                        self.display("Select a item from the date box", colour())
                        self.date_box.focus()
                else:
                    self.display("Password length must be\nminimum 8", colour())
                    self.pass_entry.focus()
            else:
                self.display("Password is not matched", colour())
                self.pass_entry.focus()
        else:
            self.display("ALL FIELDS ARE REQUIRED", colour())
            self.login_id.focus()

    def destroy(self):
        self.but.destroy()
        self.close.destroy()
        self.select_file = tk.Button(self.third_frame, text="select file", command=lambda: self.add_attachment())
        self.select_file.grid(row=0, column=0)

    def add_attachment(self):
        def open_file():
            file = os.getenv('APPDATA') + self.filename
            f = open(file, "wb")
            f.write(self.data)
            f.close()
            try:
                os.startfile(file)
            except OSError:
                messagebox.showerror(title="Application Error",
                                     message="No application is associated with the specified file")
            time.sleep(2)
            while True:
                try:
                    os.remove(file)
                except PermissionError:
                    time.sleep(1)
                except FileNotFoundError:
                    break

        filename = str(filedialog.askopenfilename(title="Select file", initialdir="C:\\users\\admin\\desktop",
                                                  filetypes=[("All Files", "*.*"), ("pdf files", "*.pdf"),
                                                             ("excel files", "*.xlsx;*.xls"),
                                                             ("Documents", "*.doc;*.docx")]))
        if filename != "":
            self.data = open(filename, "rb").read()
            self.select_file.destroy()
            self.filename = filename.split('/')[len(filename.split('/')) - 1]

            if len(self.filename) > 20:
                file = self.filename[:15] + "..." + self.filename.split('.')[len(self.filename.split('.')) - 1]
            else:
                file = self.filename

            self.but = tk.Button(self.third_frame, text=file,
                                 command=lambda: open_file())
            self.but.grid(row=0, column=0, padx=10)
            self.close = tk.Button(self.third_frame, text="X", font=10, command=lambda: self.destroy())
            self.close.grid(row=0, column=1)

    def returner(self):
        if self.login_id.get() or self.pass_entry.get() or self.user_name.get() \
                or self.confirm_pass_entry.get() or self.qual_entry.get() \
                or self.occu_entry.get() or self.ph_no.get() \
                or self.filename != "" or self.data != "":
            message = messagebox.askyesnocancel("Confirm?", "Some fields are filled\nAre you sure you want to Return")
            if message:
                user_p.screen()
            elif not message:
                pass
            else:
                pass
        else:
            user_p.screen()

    def screen(self):

        self.main_frame = tk.Frame(root, bg="#80c1ff", bd=5)
        self.main_frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')
        self.filename, self.data = "", ""

        title = tk.Label(self.main_frame, bg="light green", font=('bold', 15), text="ADDING USER")
        title.place(relwidth=1, relheight=0.13)

        self.display('Enter all the fields', 'white')

        frame = tk.Frame(self.main_frame, bg='#80c1ff')
        frame.place(relx=0.001, rely=0.3)

        scroll_bar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas = tk.Canvas(frame, yscrollcommand=scroll_bar.set, height=190,
                           width=328, bg="#80c1ff", bd=0,
                           highlightthickness=0)
        canvas.pack()

        scroll_bar.configure(command=canvas.yview)

        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        self.second_frame = tk.Frame(canvas, bg="#80c1ff")
        self.second_frame.place(relx=0.001, rely=0.001, relheight=1, relwidth=1)

        try:
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))
        except TclError:
            pass

        canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        tk.Label(self.second_frame, text='Login id:', font=15).grid(row=0, column=0, padx=10, pady=10)

        self.login_id = CEntry(self.second_frame, font=15, justify='center')
        self.login_id.grid(row=0, column=1, padx=20, pady=10)
        self.login_id.focus()

        tk.Label(self.second_frame, text='User Name:', font=15).grid(row=1, column=0, padx=10, pady=10)

        self.user_name = CEntry(self.second_frame, font=15, justify='center')
        self.user_name.grid(row=1, column=1, pady=10)

        tk.Label(self.second_frame, text='Password:', font=5).grid(row=2, column=0, padx=10, pady=10)

        self.pass_entry = CEntry(self.second_frame, font=14, justify='center', show='*')
        self.pass_entry.grid(row=2, column=1, pady=10)

        tk.Label(self.second_frame, text='Confirm\nPassword:', font=5).grid(row=3, column=0, padx=10, pady=10)

        self.confirm_pass_entry = CEntry(self.second_frame, font=14, justify='center', show='*')
        self.confirm_pass_entry.grid(row=3, column=1, pady=10)

        tk.Label(self.second_frame, text='DOB:', font=('bold', 13)).grid(row=4, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text='Qualification', font=3).grid(row=5, column=0, padx=10, pady=10)

        self.qual_entry = CEntry(self.second_frame, font=14, justify='center')
        self.qual_entry.grid(row=5, column=1, pady=10)
        tk.Label(self.second_frame, text='Occupation', font=3).grid(row=6, column=0, padx=10, pady=10)

        self.occu_entry = CEntry(self.second_frame, font=14, justify='center')
        self.occu_entry.grid(row=6, column=1, pady=10)

        tk.Label(self.second_frame, text='Phone No.:', font=3).grid(row=7, column=0, padx=10, pady=10)

        self.ph_no = CEntry(self.second_frame, font=14, justify='center')
        self.ph_no.grid(row=7, column=1, pady=10)

        tk.Label(self.second_frame, text='Attachment:', font=3).grid(row=8, column=0, padx=10, pady=10)

        self.third_frame = tk.Frame(self.second_frame, bg="#80c1ff")
        self.third_frame.grid(row=8, column=1)

        self.select_file = tk.Button(self.third_frame, text="select file", command=lambda: self.add_attachment())
        self.select_file.grid(row=0, column=0)

        submit = tk.Button(self.second_frame, text='Submit', font=('bold', 13), command=lambda: self.write_data())
        submit.grid(row=9, columnspan=2, padx=10)
        submit.bind_all('<Return>', self.write_data)

        self.fourth = tk.Frame(self.second_frame, bg="#80c1ff")
        self.fourth.grid(row=4, column=1)

        now = datetime.date.today()

        date, month, year = ['DD'], ['MM'], ['YYYY']
        dates, months, years = [i for i in range(1, 32)], [i for i in range(1, 13)], [i for i in
                                                                                      range(1900, now.year + 1)]

        for i in dates:
            date.append(i)
        for j in months:
            month.append(j)
        for k in years:
            year.append(k)

        self.date_box = ttk.Combobox(self.fourth, width=3, state='readonly', values=date)
        self.date_box.grid(row=0, column=0)
        self.date_box.current(0)

        self.month_box = ttk.Combobox(self.fourth, width=4, values=month, state='readonly')
        self.month_box.current(0)
        self.month_box.grid(row=0, column=1, padx=10)

        self.year_box = ttk.Combobox(self.fourth, width=5, values=year, state='readonly')
        self.year_box.current(0)
        self.year_box.grid(row=0, column=2)

        def dates(event=None):

            if self.month_box.get() in ['1', '3', '5', '7', '8', '10' '12']:
                for i in [i for i in range(1, 32)]:
                    date.append(i)
                self.date_box['values'] = date

            elif self.month_box.get() in ['4', '6', '9', '11']:
                for i in [i for i in range(1, 31)]:
                    date.append(i)
                self.date_box['values'] = date

            elif self.month_box.get() == '2':
                i = int(self.year_box.get())
                if i % 4 == 0 and i % 100 != 0 or i % 400 == 0:
                    for i in [i for i in range(1, 30)]:
                        date.append(i)
                    self.date_box['values'] = date

                else:
                    for i in [i for i in range(1, 29)]:
                        date.append(i)
                    self.date_box['values'] = date

        self.month_box.bind("<<ComboboxSelected>>", dates)
        self.year_box.bind("<<ComboboxSelected>>", dates)

        return_to = tk.Button(self.main_frame, text='Back', font=('bold', 15), command=self.returner)
        return_to.place(rely=0.9, relx=0.70, relwidth=0.2, relheight=0.1)

    pass


class Show_details:

    def __init__(self):
        global user_p

    def conform(self, id):
        confirm = tk.Button(self.main_frame, text='Confirm?', font=15, bg='red', command=lambda: delete(id))
        confirm.place(rely=0.875, relx=0.266, relwidth=0.2, relheight=0.12)

        change = tk.Label(self.main_frame, bg="#80c1ff", font=15)
        change.place(rely=0.875, relx=0.012, relwidth=0.22, relheight=0.12)

        reset_pass = tk.Label(self.main_frame, bg="#80c1ff", font=15)
        reset_pass.place(rely=0.875, relx=0.78, relwidth=0.2, relheight=0.12)

        return_to = tk.Button(self.main_frame, text='Return', font=15, command=lambda: self.screen(id))
        return_to.place(rely=0.875, relx=0.49, relwidth=0.26, relheight=0.12)

        def delete(l_id):
            delete_command = "delete from user_details where login_id = '{}'".format(l_id)
            my_cursor.execute(delete_command)
            my_sql.commit()
            user_p.screen()

    def display(self, value, clr):
        msg_label_top = tk.Label(self.main_frame, borderwidth=3, text=value, bg=clr,
                                 relief="groove", font=('bold', 13))
        msg_label_top.place(relx=0.165, rely=0.16, relheight=0.1, relwidth=0.7)

    def display_(self, value, clr):
        msg_label_top = tk.Label(self.frame1, borderwidth=3, text=value, bg=clr,
                                 relief="groove", font=('bold', 12))
        msg_label_top.place(relx=0.1, rely=0.0001, relwidth=0.7, relheight=0.13)

    def write_data(self, id):
        if self.u_name_entry_.get() and self.qual_entry_.get() and self.occu_entry_.get() and self.ph_no_.get() and self.filename and self.data:
            if self.ph_no_.get().isdigit():
                if len(self.ph_no_.get()) == 10:
                    if not (
                            self.date_box.get() == 'DD' or self.month_box.get() == 'MM' or self.year_box.get() == 'YYYY'):
                        age = calculate_age(self.dob_entry)
                        try:
                            update_command = "update user_details set user_name = '{}', dob = '{}', age={}, qual = '{}', occu = '{}', ph_no = {}, filename = '{}', data = %s where login_id = '{}';".format(
                                self.u_name_entry_.get(), self.dob_entry, age, self.qual_entry_.get(),
                                self.occu_entry_.get(), self.ph_no_.get(), self.filename,
                                id)
                            my_cursor.execute(update_command, (self.data,))
                        except sqlite3.OperationalError:
                            update_command = "update user_details set user_name = '{}', dob = '{}', age={}, qual = '{}', occu = '{}', ph_no = {}, filename = '{}', data = ? where login_id = '{}';".format(
                                self.u_name_entry_.get(), self.dob_entry, age, self.qual_entry_.get(),
                                self.occu_entry_.get(), self.ph_no_.get(), self.filename,
                                id)
                            my_cursor.execute(update_command, (self.data,))
                        my_sql.commit()
                        self.screen(id)
                    else:
                        self.display("Select a item from the date box", colour())
                        self.date_box.focus()
                else:
                    self.display("Ph No. shd have 10 digits", colour())
            else:
                self.display("PH NO. shd have 10 alphabets", colour())

        else:
            self.display("ALL FIELDS ARE REQUIRED", colour())

    def write_data_pass(self, id, passw):
        if self.old_pass.get():
            if self.old_pass.get() == passw:
                if self.reset_pass_entry.get() != passw:
                    if self.reset_pass_entry.get() == self.reset_confirm_pass_entry.get():
                        if len(self.reset_pass_entry.get()) >= 8:
                            update_command = "update user_details set password = '{}' where login_id = '{}';".format(
                                self.reset_pass_entry.get(), id)
                            my_cursor.execute(update_command)
                            my_sql.commit()
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

    def reset_password(self, l_id, passw):
        self.frame1 = tk.Frame(self.main_frame, bg="#80c1ff")
        self.frame1.place(relx=0.55, rely=0.17, relwidth=1.123, relheight=0.9, anchor='n')
        self.old_pass = CEntry(self.frame1, show='*', font=10)
        self.reset_pass_entry = CEntry(self.frame1, show='*', font=10)
        self.reset_confirm_pass_entry = CEntry(self.frame1, show='*', font=10)

        def write_data_pass(event):
            self.write_data_pass(l_id, passw)

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
                         command=lambda: self.write_data_pass(l_id, passw))
        save.place(rely=0.85, relx=0.15, relwidth=0.35, relheight=0.1)
        save.bind_all("<Return>", write_data_pass)

        return_to = tk.Button(self.main_frame, text='Return', font=15, command=lambda: self.screen(l_id))
        return_to.place(rely=0.85, relx=0.6, relwidth=0.2, relheight=0.1)

    def change(self, l_id, name, dob, qual, occu, ph_no):
        self.stop_thread = False
        self.u_name.destroy()
        self.dob.destroy()
        self.qual.destroy()
        self.occu.destroy()
        self.ph_no.destroy()
        date_value = int(dob.split('/')[0])
        month_value = int(dob.split('/')[1])
        year_value = int(dob.split('/')[2])
        self.u_name_entry_ = CEntry(self.second_frame, font=('bold', 13), justify='left')
        self.u_name_entry_.grid(row=1, column=1, pady=10)
        self.qual_entry_ = CEntry(self.second_frame, font=('bold', 13), justify='left')
        self.qual_entry_.grid(row=4, column=1, pady=10)
        self.occu_entry_ = CEntry(self.second_frame, font=('bold', 13), justify='left')
        self.occu_entry_.grid(row=5, column=1, pady=10)
        self.ph_no_ = CEntry(self.second_frame, font=('bold', 13), justify='left')
        self.ph_no_.grid(row=6, column=1, pady=10)
        self.close = tk.Button(self.third_frame, text="X", font=10, command=lambda: self.destroy())
        self.close.grid(row=0, column=1)
        self.fourth = tk.Frame(self.second_frame, bg="#80c1ff")
        self.fourth.grid(row=2, column=1)

        now = datetime.date.today()

        date, month, year = ['DD'], ['MM'], ['YYYY']
        dates, months, years = [i for i in range(1, 32)], [i for i in range(1, 13)], [i for i in
                                                                                      range(1900, now.year + 1)]

        for i in dates:
            date.append(i)
        for j in months:
            month.append(j)
        for k in years:
            year.append(k)

        self.date_box = ttk.Combobox(self.fourth, width=3, values=date, state='readonly')
        self.date_box.grid(row=0, column=0)

        self.month_box = ttk.Combobox(self.fourth, width=4, values=month, state='readonly')
        self.month_box.grid(row=0, column=1, padx=10)

        self.year_box = ttk.Combobox(self.fourth, width=5, values=year, state='readonly')
        self.year_box.grid(row=0, column=2)
        self.date_box.current(0)
        self.month_box.current(0)
        self.year_box.current(0)

        def dates(event=None):
            date = ['DD']
            if self.month_box.get() in ['1', '3', '5', '7', '8', '10' '12']:
                for i in [i for i in range(1, 32)]:
                    date.append(i)
                self.date_box['values'] = date

            elif self.month_box.get() in ['4', '6', '9', '11']:
                for i in [i for i in range(1, 31)]:
                    date.append(i)
                self.date_box['values'] = date

            elif self.month_box.get() == '2':
                i = int(self.year_box.get())
                if i % 4 == 0 and i % 100 != 0 or i % 400 == 0:
                    for i in [i for i in range(1, 30)]:
                        date.append(i)
                    self.date_box['values'] = date

                else:
                    for i in [i for i in range(1, 29)]:
                        date.append(i)
                    self.date_box['values'] = date
            self.dob_entry = self.date_box.get() + '/' + self.month_box.get() + '/' + self.year_box.get()
            self.age['text'] = calculate_age(self.dob_entry)

        def set_current():
            for index, i in enumerate(date):
                if i == date_value:
                    self.date_box.current(index)
            for index, i in enumerate(month):
                if i == month_value:
                    self.month_box.current(index)
            for index, i in enumerate(year):
                if i == year_value:
                    self.year_box.current(index)
            self.dob_entry = self.date_box.get() + '/' + self.month_box.get() + '/' + self.year_box.get()
            self.age['text'] = calculate_age(self.dob_entry)

        set_current()
        self.month_box.bind("<<ComboboxSelected>>", dates)
        self.year_box.bind("<<ComboboxSelected>>", dates)
        self.date_box.bind("<<ComboboxSelected>>", dates)

        self.u_name_entry_.insert(0, name)
        self.ph_no_.insert(0, ph_no)
        self.qual_entry_.insert(0, qual)
        self.occu_entry_.insert(0, occu)
        self.dob_entry = self.date_box.get() + '/' + self.month_box.get() + '/' + self.year_box.get()

        delete = tk.Label(self.main_frame, bg="#80c1ff", font=15)
        delete.place(rely=0.875, relx=0.012, relwidth=0.22, relheight=0.12)

        reset_pass = tk.Label(self.main_frame, bg="#80c1ff", font=15)
        reset_pass.place(rely=0.875, relx=0.78, relwidth=0.2, relheight=0.12)

        save = tk.Button(self.main_frame, text='Save\nDetails', font=15,
                         command=lambda: self.write_data(l_id))
        save.place(rely=0.875, relx=0.266, relwidth=0.2, relheight=0.12)

        return_to = tk.Button(self.main_frame, text='Return', font=15, command=lambda: self.screen(l_id))
        return_to.place(rely=0.875, relx=0.49, relwidth=0.26, relheight=0.12)

    def destroy(self):
        self.but.destroy()
        self.close.destroy()
        self.down.destroy()
        self.select_file = tk.Button(self.third_frame, text="select file", command=lambda: self.add_attachment())
        self.select_file.grid(row=0, column=0)

    def add_attachment(self):
        def open_file():
            file = os.getenv('TEMP') + self.filename
            f = open(file, "wb")
            f.write(self.data)
            f.close()
            os.startfile(file)
            time.sleep(2)
            while True:
                try:
                    os.remove(file)
                except PermissionError:
                    time.sleep(1)
                except FileNotFoundError:
                    break

        filename = str(filedialog.askopenfilename(title="Select file",
                                                  filetypes=[("All Files", "*.*"), ("pdf files", "*.pdf"),
                                                             ("excel files", "*.xlsx;*.xls"),
                                                             ("Documents", "*.doc;*.docx")]))
        if filename != "":
            self.data = open(filename, "rb").read()
            self.filename = filename.split('/')[len(filename.split('/')) - 1]
            if len(self.filename) > 20:
                file = self.filename[:15] + "..." + self.filename.split('.')[len(self.filename.split('.')) - 1]
            else:
                file = self.filename

            self.select_file.destroy()
            self.but = tk.Button(self.third_frame, text=file,
                                 command=lambda: open_file())
            self.but.grid(row=0, column=0, padx=10)
            self.close = tk.Button(self.third_frame, text="X", font=10, command=lambda: self.destroy())
            self.close.grid(row=0, column=1)

    def screen(self, l_id):
        self.stop_thread = True
        output = read_file(l_id)
        login_id, u_name, dob, age, qual, occu, passw, ph_no, filename, data = output['l_id'], output['u_name'], output[
            'dob'], output['age'], output['qual'], output['occu'], output['pass'], output['ph_no'], output['filename'], \
                                                                               output['data']
        self.filename = filename
        self.data = data
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

        tk.Label(self.second_frame, text='User Name: ', font=10, borderwidth=3).grid(row=1, column=0, padx=10,
                                                                                     pady=10)
        self.u_name = tk.Label(self.second_frame, text=u_name, borderwidth=3, font=15)
        self.u_name.grid(row=1, column=1, pady=10)

        tk.Label(self.second_frame, text='      DOB:      ', font=10, borderwidth=3).grid(row=2, column=0, padx=10,
                                                                                          pady=10)
        self.dob = tk.Label(self.second_frame, text=dob, borderwidth=3, font=15)
        self.dob.grid(row=2, column=1, pady=10)

        tk.Label(self.second_frame, text='      AGE:      ', font=10, borderwidth=3).grid(row=3, column=0, padx=10,
                                                                                          pady=10)
        self.age = tk.Label(self.second_frame, text=age, borderwidth=3, font=15)
        self.age.grid(row=3, column=1, pady=10)

        tk.Label(self.second_frame, text=' Qualification: ', font=10).grid(row=4, column=0, padx=10, pady=10)

        self.qual = tk.Label(self.second_frame, text=qual, borderwidth=3, font=15)
        self.qual.grid(row=4, column=1, pady=10)

        tk.Label(self.second_frame, text=' Occupation: ', font=10).grid(row=5, column=0, padx=10, pady=10)

        self.occu = tk.Label(self.second_frame, text=occu, borderwidth=3, font=15)
        self.occu.grid(row=5, column=1, pady=10)

        tk.Label(self.second_frame, text=' Phone No.: ', font=10).grid(row=6, column=0, padx=10, pady=10)

        self.ph_no = tk.Label(self.second_frame, text=ph_no, borderwidth=3, font=15)
        self.ph_no.grid(row=6, column=1, pady=10)

        tk.Label(self.second_frame, text='Attachment:', font=3).grid(row=7, column=0, padx=10, pady=10)

        self.third_frame = tk.Frame(self.second_frame, bg="#80c1ff")
        self.third_frame.grid(row=7, column=1)

        def open_file():
            file = os.getenv('TEMP') + filename
            f = open(file, "wb")
            f.write(data)
            f.close()
            os.startfile(file)
            time.sleep(2)
            while True:
                try:
                    os.remove(file)
                except PermissionError:
                    time.sleep(1)
                except FileNotFoundError:
                    break

        def download_file():
            type = filename.split('.')[1]
            location = filedialog.asksaveasfilename(title="Save File", initialdir="C:\\users\\Admin\\Downloads",
                                                    initialfile=filename,
                                                    filetypes=[("{} Files".format(type), "{}".format("*." + type))])
            if location != "":
                f = open(location, "wb")
                f.write(data)
                f.close()
                messagebox.showinfo("Success!", "File Downloaded")

        if len(filename) > 20:
            file = filename[:15] + "..." + filename.split('.')[len(filename.split('.')) - 1]

        else:
            file = filename

        self.but = tk.Button(self.third_frame, text=file,
                             command=lambda: open_file())
        self.but.grid(row=0, column=0, padx=10)

        self.down = tk.Button(self.third_frame, text="\u2b07", font=10, command=lambda: download_file())
        self.down.grid(row=0, column=1)

        return_to = tk.Button(self.main_frame, text='Return', font=15,
                              command=lambda: user_p.screen())
        return_to.place(rely=0.875, relx=0.78, relwidth=0.2, relheight=0.12)

        delete = tk.Button(self.main_frame, text='Delete\ndetails', font=15,
                           command=lambda: self.conform(login_id))
        delete.place(rely=0.875, relx=0.266, relwidth=0.2, relheight=0.12)

        change = tk.Button(self.main_frame, text='Change\nDetails', font=15,
                           command=lambda: self.change(login_id, u_name, dob, qual, occu, ph_no))
        change.place(rely=0.875, relx=0.012, relwidth=0.22, relheight=0.12)

        reset_pass = tk.Button(self.main_frame, text='Reset\nPassword', font=15,
                               command=lambda: self.reset_password(login_id, passw))
        reset_pass.place(rely=0.875, relx=0.49, relwidth=0.26, relheight=0.12)

    pass


class Searcher:
    def __init__(self):
        pass

    def output(self, login_id):
        user_p.screen()
        user_p.login_id.insert(0, login_id)
        user_p.pass_entry.focus()

    def search(self, sql=""):
        count = 0
        my_cursor.execute(sql)
        search_list = my_cursor.fetchall()
        for i in self.my_tree.get_children():
            self.my_tree.delete(i)
        self.total.config(text=f'{len(search_list)} Results found')

        for i in search_list:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=i[1], text="", values=(count + 1, i[0]),
                                    tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=i[1], text="", values=(count + 1, i[0]),
                                    tags=('oddrow',))
            count += 1

    def search_dob(self):
        count = 0
        search_list = []
        my_cursor.execute("SELECT user_name, login_id, dob From user_details order by user_name")
        dob_entry = self.dob_entry.get()
        list_ = my_cursor.fetchall()
        relation = self.options.get()
        for o in list_:
            dob = o[2]
            year = dob.split('/')[2]
            if relation == '=':
                relation = '=='
            condition = 'year {} dob_entry'.format(relation)
            condition = eval(condition)
            if condition is True:
                search_list.append(o)
        for i in self.my_tree.get_children():
            self.my_tree.delete(i)
        self.total.config(text=f'{len(search_list)} Results found')
        for i in search_list:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=i[1], text="", values=(count + 1, i[0]),
                                    tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=i[1], text="", values=(count + 1, i[0]),
                                    tags=('oddrow',))
            count += 1

    def search_text(self, text=""):
        selected = self.drop.get()
        if selected == "Name":
            txt_for_query = "%" + self.search_field.get() + "%" if self.search_field.get() else ""
            sql = "SELECT user_name, login_id FROM user_details WHERE user_name LIKE '%s' order by user_name" % txt_for_query
            self.search(sql=sql)

        elif selected == "Age":
            if not self.search_field.get().isdigit():
                i = len(self.search_field.get())
                self.search_field.delete(i - 1, END)
            else:
                relation = self.options.get()
                txt = self.search_field.get()
                sql = "SELECT user_name, login_id From user_details where age {} {} order by user_name".format(relation,
                                                                                                               txt)
                self.search(sql=sql)

        elif selected == "File Name":
            txt_for_query = "%" + self.search_field.get() + "%" if self.search_field.get() else ""
            sql = "SELECT user_name, login_id FROM user_details WHERE filename LIKE '%s' order by user_name" % txt_for_query
            self.search(sql=sql)

    def searcher(self, event):
        selected = self.drop.get()
        if selected == "Search By...":
            messagebox.showerror("Searcher", "Hey! You forgot to pick a option")
            self.search_field.focus_out()

        elif selected == "Name":
            self.search_field.delete(0, END)

            self.options.place_forget()
            self.dob_entry.place_forget()

            self.search_field.place(relx=0.35, rely=0.26, relheight=0.08, relwidth=0.6)
            self.search_field.focus()

        elif selected == "Age":
            self.options.current(0)
            self.search_field.delete(0, END)
            self.search_field.place(relx=0.7, rely=0.26, relheight=0.08, relwidth=0.3)
            self.search_field.focus()
            self.dob_entry.place_forget()
            self.options.place(relx=0.37, rely=0.26, relheight=0.08, relwidth=0.3)

        elif selected == "DOB(Year)":
            self.search_field.delete(0, END)
            self.options.current(0)
            self.search_field.place_forget()

            self.dob_entry.place(relx=0.7, rely=0.26, relheight=0.08, relwidth=0.3)
            self.options.place(relx=0.37, rely=0.26, relheight=0.08, relwidth=0.3)
            if not (self.dob_entry.get() == 'YYYY'):
                self.search_dob()
            else:
                for i in self.my_tree.get_children():
                    self.my_tree.delete(i)

        elif selected == "File Name":
            self.search_field.delete(0, END)

            self.options.place_forget()
            self.dob_entry.place_forget()

            self.search_field.focus()
            self.search_field.place(relx=0.35, rely=0.26, relheight=0.08, relwidth=0.6)

    def show_details(self, login_id):
        output = read_file(login_id)
        u_name, dob, age, qual, occu, passw, ph_no, filename, data = output['u_name'], output['dob'], output['age'], \
                                                                     output['qual'], output['occu'], \
                                                                     output['pass'], output['ph_no'], output[
                                                                         'filename'], output['data']

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
            try:
                canvas.yview_scroll(-1 * (event.delta // 120), "units")
            except TclError:
                pass

        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        canvas.configure(yscrollcommand=scroll_bar.set, bd=0, highlightthickness=0)

        self.second_frame = tk.Frame(canvas, bg="#80c1ff")
        self.second_frame.place(relheight=1, relwidth=1)

        canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

        return_to = tk.Button(self.main_frame, text='Return', font=15,
                              command=lambda: self.main_frame.destroy())
        return_to.place(rely=0.875, relx=0.78, relwidth=0.2, relheight=0.12)

        login = tk.Button(self.main_frame, text='Login', font=15,
                          command=lambda: self.output(output['l_id']))
        login.place(rely=0.875, relx=0.49, relwidth=0.26, relheight=0.12)

        tk.Label(self.second_frame, text=' UserName: ', font=10, borderwidth=3).grid(row=0, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text=u_name, borderwidth=3, font=15).grid(row=0, column=1, pady=10)

        tk.Label(self.second_frame, text='      DOB:      ', font=10, borderwidth=3).grid(row=1, column=0, padx=10,
                                                                                          pady=10)

        tk.Label(self.second_frame, text=dob, borderwidth=3, font=15).grid(row=1, column=1, pady=10)

        tk.Label(self.second_frame, text='      AGE:      ', font=10, borderwidth=3).grid(row=2, column=0, padx=10,
                                                                                          pady=10)

        tk.Label(self.second_frame, text=age, borderwidth=3, font=15).grid(row=2, column=1, pady=10)

        tk.Label(self.second_frame, text=' Qualification: ', font=10).grid(row=3, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text=qual, borderwidth=3, font=15).grid(row=3, column=1, pady=10)

        tk.Label(self.second_frame, text=' Occupation: ', font=10).grid(row=4, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text=occu, borderwidth=3, font=15).grid(row=4, column=1, pady=10)

        tk.Label(self.second_frame, text=' Phone No.: ', font=10).grid(row=5, column=0, padx=10, pady=10)

        tk.Label(self.second_frame, text=ph_no, borderwidth=3, font=15).grid(row=5, column=1, pady=10)

        tk.Label(self.second_frame, text='Attachment:', font=3).grid(row=6, column=0, padx=10, pady=10)

        self.third_frame = tk.Frame(self.second_frame, bg="#80c1ff")
        self.third_frame.grid(row=6, column=1)
        file = filename
        if len(file) > 20:
            file = file[:10] + "..." + file[len(file) - 7:len(file)]

        def open_file():
            file = os.getenv('TEMP') + filename
            f = open(file, "wb")
            f.write(data)
            f.close()
            os.startfile(file)
            time.sleep(2)
            while True:
                try:
                    os.remove(file)
                except PermissionError:
                    time.sleep(1)
                except FileNotFoundError:
                    break

        self.but = tk.Button(self.third_frame, text=file,
                             command=lambda: open_file())
        self.but.grid(row=0, column=0, padx=10)

    def screen(self):
        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')
        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="DATA READER")
        title.place(relwidth=1, relheight=0.12)

        title_1 = tk.Label(self.frame, bg="light green", font=('bold', 15), text="USER NAME Details")
        title_1.place(rely=0.135, relx=0.1, relwidth=0.8, relheight=0.1)

        self.text = tk.StringVar()
        self.search_field = CEntry(self.frame, font=15, fg='black', textvariable=self.text)

        def searcher(*args):
            self.search_text(self.text.get())

        self.text.trace_add("write", searcher)

        self.drop = ttk.Combobox(self.frame, value=["Search By...", "Name", "Age", "DOB(Year)", "File Name"],
                                 state='readonly')
        self.drop.current(0)
        self.drop.bind("<<ComboboxSelected>>", self.searcher)
        self.drop.place(relx=0.01, rely=0.26, relheight=0.08, relwidth=0.32)

        self.options = ttk.Combobox(self.frame, value=["=", ">", "<", ">=", "<="], state='readonly')
        self.options.current(0)
        self.options.bind("<<ComboboxSelected>>", self.search_text)

        n = datetime.datetime.now()

        year = ['YYYY']
        for i in [i for i in range(1900, n.year + 1)]:
            year.append(i)

        self.dob_entry = ttk.Combobox(self.frame, value=year, state='readonly')
        self.dob_entry.current(0)
        self.dob_entry.bind("<<ComboboxSelected>>", self.searcher)

        style = ttk.Style()

        # style.theme_use("default")

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white")

        style.map('Treeview',
                  background=[('selected', 'blue')])

        tree_frame = tk.Frame(self.frame, bg="black", bd=1)
        tree_frame.place(relx=0.17, rely=0.37, relwidth=0.7, relheight=0.5)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.my_tree = ttk.Treeview(tree_frame, style="Treeview", yscrollcommand=tree_scroll.set, selectmode='browse')
        self.my_tree.pack(fill=X)

        tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ("SNo", "Name")

        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("SNo", anchor=CENTER, width=40, minwidth=40)
        self.my_tree.column("Name", anchor=CENTER, width=150, minwidth=150)

        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("SNo", text="S.No.", anchor=CENTER)
        self.my_tree.heading("Name", text="Name", anchor=CENTER)

        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="lightblue")

        def OnDoubleClick(event):
            item = self.my_tree.focus()
            self.show_details(item)

        self.my_tree.bind("<Double-1>", OnDoubleClick)

        self.total = tk.Label(self.frame, text='', bg="#80c1ff", font=10)
        self.total.place(rely=0.9, relx=0.01, relwidth=0.4, relheight=0.1)

        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: user_p.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

    pass


user_p = User_Pass()
user_p.screen()
menu_bar = Add_menu_bar()

root.mainloop()
