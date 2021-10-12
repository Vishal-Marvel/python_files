import pickle
import tkinter as tk
import os
from cryptography.fernet import Fernet
import datetime

root = tk.Tk()
root.title("data reader")
# file_name = sys._MEIPASS + "\calculator.ico"
# root.wm_iconbitmap(file_name)
# root.wm_iconbitmap("data_collector.ico")
canvas = tk.Canvas(root, height=350, width=350)
canvas.pack()


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


def read_file(path):
    file_path = os.getcwd() + "\\data\\" + path + ".details"
    decrypt(file_path)
    a_file = open(file_path, "rb")
    output = pickle.load(a_file)
    a_file.close()
    encrypt(file_path)
    return output


class Show_Only_details:

    def __init__(self):
        pass

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
        if not word:
            head = tk.Label(self.frame, bg="yellow", text="NO ENTRIES FOUND")
            head.place(relx=0.25, rely=0.475, relheight=0.07, relwidth=0.45)
        return word

    def output_name(self, start=0, end=5):
        self.search_field_name.delete(0, tk.END)
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
                name = tk.Label(frame, text=details['user'])
                name.place(relx=0.45, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.35)
                j += 1
                k += 1
            except FileNotFoundError:
                pass

        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(word) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.output_name(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.output_name(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def output_dob(self, start=0, end=5):
        self.search_field_dob_month.delete(0, tk.END)
        self.search_field_dob_year.delete(0, tk.END)
        k = start
        j = 0
        word = self.word_list()
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.42, relwidth=1, relheight=0.58)
        for i in word[start:end]:
            try:
                details = read_file(i)
                s = tk.Label(frame, text=str(k + 1))
                s.place(relx=0.08, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
                name = tk.Label(frame, text=details['user'])
                name.place(relx=0.28, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.3)
                dob = tk.Label(frame, text=details['dob'])
                dob.place(relx=0.735, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.2)
                j += 1
                k += 1
            except FileNotFoundError:
                pass
        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(word) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.output_dob(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.output_dob(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def output_qual(self, start=0, end=5):
        k = start
        j = 0
        word = self.word_list()
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.42, relwidth=1, relheight=0.58)

        for i in word[start:end]:
            try:
                details = read_file(i)
                s = tk.Label(frame, text=str(k + 1))
                s.place(relx=0.08, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
                name = tk.Label(frame, text=details['user'])
                name.place(relx=0.28, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.3)
                qual = tk.Label(frame, text=details['qual'])
                qual.place(relx=0.735, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.2)
                j += 1
                k += 1
            except FileNotFoundError:
                pass
        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(word) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.output_qual(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.output_qual(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def output_occu(self, start=0, end=5):
        k = start
        j = 0
        word = self.word_list()
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.42, relwidth=1, relheight=0.58)
        for i in word[start:end]:
            try:
                details = read_file(i)
                s = tk.Label(frame, text=str(k + 1))
                s.place(relx=0.08, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
                name = tk.Label(frame, text=details['user'])
                name.place(relx=0.28, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.3)
                occu = tk.Label(frame, text=details['occu'])
                occu.place(relx=0.735, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.2)
                j += 1
                k += 1
            except FileNotFoundError:
                pass
        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(word) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.output_occu(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.output_occu(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def search_name(self, start=0, end=5):
        k = start
        j = 0
        word = self.word_list()
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.42, relwidth=1, relheight=0.58)
        search = []
        if self.search_field_name.get():
            for i in word:
                if self.search_field_name.get().lower() in i:
                    search.append(i)
            if len(search) == 0:
                tk.Label(frame, text="NO DATA FOUND").place(relx=0.2, rely=0.3, relheight=0.1, relwidth=0.5)
            else:
                for i in search[start:end]:
                    try:
                        details = read_file(i)
                        s = tk.Label(frame, text=str(k + 1))
                        s.place(relx=0.23, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
                        name = tk.Label(frame, text=details['user'])
                        name.place(relx=0.45, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.35)
                        j += 1
                        k += 1
                    except FileNotFoundError:
                        pass
        else:
            tk.Label(frame, text="SEARCH FIELD IS EMPTY", font=15).place(relx=0.2, rely=0.3, relheight=0.2, relwidth=0.3)

        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.output_name())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(search) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.search_name(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.search_name(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def search_dob(self, start=0, end=5):
        k = start
        j = 0
        word = self.word_list()
        search = []
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.42, relwidth=1, relheight=0.58)
        if self.search_field_dob_month.get() or self.search_field_dob_year.get():
            if (self.search_field_dob_month.get() and self.search_field_dob_month.get().isdigit() and 1 <= int(self.search_field_dob_month.get()) <= 12) or (self.search_field_dob_year.get() and self.search_field_dob_year.get().isdigit()):
                for i in word:
                    details = read_file(i)
                    dob = str(details['dob'])
                    month = dob.split('-')[1]
                    year = dob.split('-')[0]

                    if self.search_field_dob_month.get() and self.search_field_dob_year.get():
                        if str('%02d' % int(self.search_field_dob_month.get())) == month and self.search_field_dob_year.get() == year:
                            search.append(i)
                    elif self.search_field_dob_month.get():
                        if str('%02d' % int(self.search_field_dob_month.get())) == month:
                            search.append(i)
                    else:
                        if self.search_field_dob_year.get() == year:
                            search.append(i)
                if len(search) == 0:
                    tk.Label(frame, text="NO DATA FOUND", font=15).place(relx=0.2, rely=0.3, relheight=0.2, relwidth=0.5)
                else:
                    for i in search[start:end]:
                        try:
                            details = read_file(i)
                            s = tk.Label(frame, text=str(k + 1))
                            s.place(relx=0.08, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
                            name = tk.Label(frame, text=details['user'])
                            name.place(relx=0.28, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.3)
                            dob = tk.Label(frame, text=details['dob'])
                            dob.place(relx=0.735, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.2)
                            j += 1
                            k += 1
                        except FileNotFoundError:
                            pass
            else:
                tk.Label(frame, text="INVALID INPUT", font=15).place(relx=0.2, rely=0.3, relheight=0.2,relwidth=0.5)
        else:
            tk.Label(frame, text="SEARCH FIELD IS EMPTY", font=15).place(relx=0.2, rely=0.3, relheight=0.2, relwidth=0.5)

        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.output_dob())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(search) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.search_dob(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.search_dob(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def search_qual(self, start=0, end=5):
        k = start
        j = 0
        word = self.word_list()
        search = []
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.42, relwidth=1, relheight=0.58)
        if self.search_field_qual.get():
            for i in word:
                details = read_file(i)
                if self.search_field_qual.get().lower() in details['qual']:
                    search.append(i)
            if len(search) == 0:
                tk.Label(frame, text="NO DATA FOUND").place(relx=0.2, rely=0.3, relheight=0.1, relwidth=0.5)
            else:
                for i in search[start:end]:
                    try:
                        details = read_file(i)
                        s = tk.Label(frame, text=str(k + 1))
                        s.place(relx=0.08, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
                        name = tk.Label(frame, text=details['user'])
                        name.place(relx=0.28, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.3)
                        qual = tk.Label(frame, text=details['qual'])
                        qual.place(relx=0.735, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.2)
                        j += 1
                        k += 1
                    except FileNotFoundError:
                        pass
        else:
            tk.Label(frame, text="SEARCH FIELD IS EMPTY", font=10).place(relx=0.2, rely=0.3, relheight=0.1, relwidth=0.3)

        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.output_qual())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(search) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.search_qual(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.search_qual(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def search_occu(self, start=0, end=5):
        k = start
        j = 0
        word = self.word_list()
        search = []
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.42, relwidth=1, relheight=0.58)
        if self.search_field_occu.get():
            for i in word:
                details = read_file(i)
                if self.search_field_occu.get().lower() in details['occu']:
                    search.append(i)
            if len(search) == 0:
                tk.Label(frame, text="NO DATA FOUND").place(relx=0.2, rely=0.3, relheight=0.1, relwidth=0.5)
            else:
                for i in search[start:end]:
                    try:
                        details = read_file(i)
                        s = tk.Label(frame, text=str(k + 1))
                        s.place(relx=0.08, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
                        name = tk.Label(frame, text=details['user'])
                        name.place(relx=0.28, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.3)
                        occu = tk.Label(frame, text=details['occu'])
                        occu.place(relx=0.735, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.2)
                        j += 1
                        k += 1
                    except FileNotFoundError:
                        pass
        else:
            tk.Label(frame, text="SEARCH FIELD IS EMPTY", font=10).place(relx=0.2, rely=0.3, relheight=0.1, relwidth=0.3)

        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)
        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.output_occu())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        if len(search) > end:
            next_page = tk.Button(self.frame, text='Next', font=15,
                                  command=lambda: self.search_occu(start=end, end=end + 5))
            next_page.place(rely=0.9, relx=0.35, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = tk.Button(self.frame, text="Previous", font=15,
                                 command=lambda: self.search_occu(start=start - 5, end=start))
            previous.place(rely=0.9, relx=0.12, relwidth=0.2, relheight=0.1)

    def dob(self):
        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)

        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="DATA READER")
        title.place(relwidth=1, relheight=0.13)

        title_1 = tk.Label(self.frame, bg="light green", font=('bold', 15), text="DOB Details")
        title_1.place(rely=0.145, relx=0.1, relwidth=0.8, relheight=0.1)
        tk.Label(self.frame, text="Month:", bg="#80c1ff").place(relx=0.05, rely=0.26, relheight=0.1, relwidth=0.12)
        tk.Label(self.frame, text="Year:", bg="#80c1ff").place(relx=0.4, rely=0.26, relheight=0.1, relwidth=0.1)

        self.search_field_dob_month = tk.Entry(self.frame, font=15)
        self.search_field_dob_month.place(relx=0.18, rely=0.26, relheight=0.08, relwidth=0.18)
        self.search_field_dob_month.focus()

        self.search_field_dob_year = tk.Entry(self.frame, font=15)
        self.search_field_dob_year.place(relx=0.53, rely=0.26, relheight=0.08, relwidth=0.195)

        search = tk.Button(self.frame, text="search", command= lambda : self.search_dob())
        search.place(relx=0.8, rely=0.26, relheight=0.08, relwidth=0.15)

        s = tk.Label(self.frame, bg="#80c1ff", text="S.No.")
        s.place(relx=0.08, rely=0.35, relheight=0.06, relwidth=0.1)

        n = tk.Label(self.frame, bg="#80c1ff", text="Name")
        n.place(relx=0.32, rely=0.35, relheight=0.06, relwidth=0.25)

        d = tk.Label(self.frame, bg="#80c1ff", text="DOB")
        d.place(relx=0.735, rely=0.35, relheight=0.06, relwidth=0.2)

        self.output_dob()

    def qual(self):
        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)

        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="DATA READER")
        title.place(relwidth=1, relheight=0.13)

        title_1 = tk.Label(self.frame, bg="light green", font=('bold', 15), text="QUALIFICATION Details")
        title_1.place(rely=0.145, relx=0.1, relwidth=0.8, relheight=0.1)

        self.search_field_qual = tk.Entry(self.frame, font=15)
        self.search_field_qual.place(relx=0.07, rely=0.26, relheight=0.08, relwidth=0.65)
        self.search_field_qual.focus()

        search = tk.Button(self.frame, text="search", command= lambda : self.search_qual())
        search.place(relx=0.8, rely=0.26, relheight=0.08, relwidth=0.15)

        s = tk.Label(self.frame, bg="#80c1ff", text="S.No.")
        s.place(relx=0.08, rely=0.35, relheight=0.06, relwidth=0.1)

        n = tk.Label(self.frame, bg="#80c1ff", text="Name")
        n.place(relx=0.32, rely=0.35, relheight=0.06, relwidth=0.25)

        q = tk.Label(self.frame, bg="#80c1ff", text="Qualification")
        q.place(relx=0.735, rely=0.35, relheight=0.06, relwidth=0.2)

        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        self.output_qual()

    def occu(self):
        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)

        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="DATA READER")
        title.place(relwidth=1, relheight=0.13)

        title_1 = tk.Label(self.frame, bg="light green", font=('bold', 15), text="OCCUPATION Details")
        title_1.place(rely=0.145, relx=0.1, relwidth=0.8, relheight=0.1)

        self.search_field_occu = tk.Entry(self.frame, font=15)
        self.search_field_occu.place(relx=0.07, rely=0.26, relheight=0.08, relwidth=0.65)
        self.search_field_occu.focus()

        search = tk.Button(self.frame, text="search", command= lambda : self.search_occu())
        search.place(relx=0.8, rely=0.26, relheight=0.08, relwidth=0.15)

        s = tk.Label(self.frame, bg="#80c1ff", text="S.No.")
        s.place(relx=0.08, rely=0.35, relheight=0.06, relwidth=0.1)

        n = tk.Label(self.frame, bg="#80c1ff", text="Name")
        n.place(relx=0.32, rely=0.35, relheight=0.06, relwidth=0.25)

        o = tk.Label(self.frame, bg="#80c1ff", text="Occupation")
        o.place(relx=0.735, rely=0.35, relheight=0.06, relwidth=0.2)

        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        self.output_occu()

    def name(self):
        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="DATA READER")
        title.place(relwidth=1, relheight=0.13)

        title_1 = tk.Label(self.frame, bg="light green", font=('bold', 15), text="USER NAME Details")
        title_1.place(rely=0.145, relx=0.1, relwidth=0.8, relheight=0.1)

        self.search_field_name = tk.Entry(self.frame, font=15)
        self.search_field_name.place(relx=0.07, rely=0.26, relheight=0.08, relwidth=0.65)
        self.search_field_name.focus()

        search = tk.Button(self.frame, text="search", command= lambda : self.search_name())
        search.place(relx=0.8, rely=0.26, relheight=0.08, relwidth=0.15)

        head = tk.Label(self.frame, bg="#80c1ff", text="S.No.")
        head.place(relx=0.23, rely=0.35, relheight=0.07, relwidth=0.1)

        head = tk.Label(self.frame, bg="#80c1ff", text="Name")
        head.place(relx=0.45, rely=0.35, relheight=0.07, relwidth=0.25)

        return_to = tk.Button(self.frame, text='Return', font=15, command=lambda: self.screen())
        return_to.place(rely=0.9, relx=0.6, relwidth=0.2, relheight=0.1)

        self.output_name()

    def screen(self):
        frame = tk.Frame(root, bg="#80c1ff", bd=7)

        frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(frame, bg="light green", font=('bold', 15), text="DATA READER")
        title.place(relwidth=1, relheight=0.16)

        dob = tk.Button(frame, text="DOB", command=lambda: self.dob())
        dob.place(relx=0.25, rely=0.25, relheight=0.12, relwidth=0.15)

        name = tk.Button(frame, text="NAME", command=lambda: self.name())
        name.place(relx=0.45, rely=0.25, relheight=0.12, relwidth=0.15)

        qual = tk.Button(frame, text="QUALIFICATION", command=lambda: self.qual())
        qual.place(relx=0.1, rely=0.4, relheight=0.12, relwidth=0.3)

        occu = tk.Button(frame, text="OCCUPATION", command=lambda: self.occu())
        occu.place(relx=0.45, rely=0.4, relheight=0.12, relwidth=0.3)

    pass


display = Show_Only_details()
display.screen()
root.mainloop()
