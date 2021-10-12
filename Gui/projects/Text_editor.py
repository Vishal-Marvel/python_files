from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser
import threading, os, sys, time
import win32api
from tkinter import messagebox

root = Tk()
root.title("Text Editor")
root.geometry("450x400")

open_status_name, save_status = False, False

my_frame = Frame(root)
my_frame.place(relx=0.01, rely=0.00001, relheight=0.95, relwidth=0.98)


class Find(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.e = Entry(top)
        self.e.focus()
        self.e.pack()
        self.b = Button(top, text='Search', command=self.cleanup)
        self.b.bind_all("<Return>", self.cleanup)
        self.b.pack()

    def cleanup(self, event=None):
        self.value = self.e.get()
        self.top.destroy()


class Find_and_replace(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.e = Entry(top)
        self.e.pack()
        self.f = Entry(top)
        self.b = Button(top, text='Search', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()


def new_file(event=None):
    global save_status, open_status_name
    if save_status:
        ans = messagebox.askyesnocancel("Save File", "You have unsaved changes.\nDo you want to save the file?")
        if ans:
            save_file()
            my_text.delete("1.0", END)
            root.title("New File")
            status_bar.config(text="New File        ")
            my_text.edit_modified(False)
            save_status = False
            open_status_name = False
        elif ans is False:
            my_text.delete("1.0", END)
            root.title("New File")
            status_bar.config(text="New File        ")
            my_text.edit_modified(False)
            save_status = False
            open_status_name = False
        elif ans is None:
            pass


def open_file(event=None):
    while True:
        global open_status_name, save_status
        try:
            if save_status:
                ans = messagebox.askyesnocancel("Save File", "You have unsaved changes.\nDo you want to save the file?")
                if ans:
                    save_file()
                    text_file = filedialog.askopenfilename(title="Open File", filetypes=(
                    ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
                    if text_file:
                        file = open(text_file, 'r')
                        stuff = file.read()
                        my_text.delete("1.0", END)

                        open_status_name = text_file
                        name = text_file
                        status_bar.config(text=f'{name}      ')
                        name = name.split('/')[len(name.split('/')) - 1]
                        root.title(f'{name}')
                        my_text.insert(END, stuff)
                        file.close()
                        my_text.edit_modified(False)
                        save_status = False
                        break
                elif ans is False:
                    text_file = filedialog.askopenfilename(title="Open File", filetypes=(
                    ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
                    if text_file:
                        file = open(text_file, 'r')
                        stuff = file.read()
                        my_text.delete("1.0", END)

                        open_status_name = text_file
                        name = text_file
                        status_bar.config(text=f'{name}      ')
                        name = name.split('/')[len(name.split('/')) - 1]
                        root.title(f'{name}')
                        my_text.insert(END, stuff)
                        file.close()
                        my_text.edit_modified(False)
                        save_status = False
                        break
                elif ans is None:
                    pass

            break
        except UnicodeDecodeError:
            messagebox.showerror("Text Editor", "Unsupported file format")


def save_as_file(event=None):
    global open_status_name, save_status
    text_file = filedialog.asksaveasfilename(title="Save As", defaultextension="*.", filetypes=(
    ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        name = text_file
        status_bar.config(text=f'Saved: {name}      ')
        name = name.split('/')[len(name.split('/')) - 1]
        root.title(f'{name}')
        my_text.edit_modified(False)
        save_status = False
        open_status_name = text_file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()


def save_file(event=None):
    global open_status_name, save_status
    if open_status_name:
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        text_file.close()
        name = open_status_name
        name = name.split('/')[len(name.split('/')) - 1]
        root.title(f'{name}')
        my_text.edit_modified(False)
        save_status = False
        status_bar.config(text=f'Saved: {open_status_name}      ')
    else:
        save_as_file()


def print_file(event=None):
    # printer_name = win32print.GetDefaultPrinter()
    # status_bar.config(text=printer_name)
    global open_status_name, save_status
    if save_status:
        ans = messagebox.askyesnocancel("Save File", "You have unsaved changes.\nDo you want to save the file?")
        if ans:
            save_file()
            if open_status_name:
                win32api.ShellExecute(0, "print", open_status_name, None, ".", 0)
            else:
                ans = messagebox.askyesnocancel("Printer", "No file specified\nDo you want to choose a file")
                if ans:
                    text_file = filedialog.askopenfilename(title="Choose File", filetypes=(
                    ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
                    if text_file:
                        win32api.ShellExecute(0, "print", text_file, None, ".", 0)
        elif ans is False:
            if open_status_name:
                win32api.ShellExecute(0, "print", open_status_name, None, ".", 0)
            else:
                ans = messagebox.askyesnocancel("Printer", "No file specified\nDo you want to choose a file")
                if ans:
                    text_file = filedialog.askopenfilename(title="Choose File", filetypes=(
                    ("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
                    if text_file:
                        win32api.ShellExecute(0, "print", text_file, None, ".", 0)
        elif ans is None:
            pass


def bold_it(event=None):
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")

    my_text.tag_configure("bold", font=bold_font)
    try:
        current_tags = my_text.tag_names("sel.first")

        if "bold" in current_tags:
            my_text.tag_remove("bold", "sel.first", "sel.last")
        else:
            my_text.tag_add("bold", "sel.first", "sel.last")

    except Exception:
        pass


def italic_it(event=None):
    italic_font = font.Font(my_text, my_text.cget("font"))
    italic_font.configure(slant="italic")

    my_text.tag_configure("italic", font=italic_font)
    try:
        current_tags = my_text.tag_names("sel.first")

        if "italic" in current_tags:
            my_text.tag_remove("italic", "sel.first", "sel.last")
        else:
            my_text.tag_add("italic", "sel.first", "sel.last")
    except Exception:
        pass


def underline_it(event=None):
    underline_font = font.Font(my_text, my_text.cget("font"))
    underline_font.configure(underline=True)

    my_text.tag_configure("underline", font=underline_font)

    try:
        current_tags = my_text.tag_names("sel.first")

        if "underline" in current_tags:
            my_text.tag_remove("underline", "sel.first", "sel.last")
        else:
            my_text.tag_add("underline", "sel.first", "sel.last")
    except Exception:
        pass


def text_colour():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        color_font = font.Font(my_text, my_text.cget("font"))

        my_text.tag_configure("colored", font=color_font, foreground=my_color)
        try:
            current_tags = my_text.tag_names("sel.first")
            if "colored" in current_tags:
                my_text.tag_remove("colored", "sel.first", "sel.last")
            else:
                my_text.tag_add("colored", "sel.first", "sel.last")
        except Exception:
            pass


def select_all():
    my_text.tag_add('sel', '1.0', 'end')


def clear_all():
    my_text.delete(1.0, END)


def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(bg=my_color)


def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        my_text.config(fg=my_color)


def check_saved():
    global save_status, open_status_name
    while True:
        try:
            if my_text.edit_modified() and open_status_name:
                name = open_status_name
                name = name.split('/')[len(name.split('/')) - 1]
                root.title(f'*{name}')
                status_bar.config(text=f'Unsaved: {open_status_name}      ')
                save_status = True
                my_text.edit_modified(False)

            elif my_text.edit_modified():
                root.title('*New File')
                status_bar.config(text='Unsaved        ')
                save_status = True
                my_text.edit_modified(False)
            time.sleep(0.5)
        except RuntimeError:
            break


def night_on():
    main_color = "#000000"
    second_color = "#373737"
    text_color = "green"

    root.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_color)
    my_text.config(bg=second_color)

    file_menu.config(bg=main_color, fg=text_color)
    edit_menu.config(bg=main_color, fg=text_color)
    color_menu.config(bg=main_color, fg=text_color)
    options_menu.config(bg=main_color, fg=text_color)
    find_menu.config(bg=main_color, fg=text_color)


def night_off():
    main_color = "SystemButtonFace"
    second_color = "SystemButtonFace"
    text_color = "SystemFace"

    root.config(bg=main_color)
    status_bar.config(bg=main_color, fg=text_color)
    my_text.config(bg=second_color)

    file_menu.config(bg=main_color, fg=text_color)
    edit_menu.config(bg=main_color, fg=text_color)
    color_menu.config(bg=main_color, fg=text_color)
    options_menu.config(bg=main_color, fg=text_color)
    find_menu.config(bg=main_color, fg=text_color)


def on_closing(event=None):
    global save_status
    if save_status:
        ans = messagebox.askyesnocancel("Save File", "You have unsaved changes.\nDo you want to save the file?")
        if ans:
            save_file()
            root.destroy()
        elif ans is False:
            root.destroy()
    else:
        root.destroy()


def disable():
    while True:
        if "sel" not in my_text.tag_names(INSERT):
            edit_menu.entryconfig("Cut", state="disabled")
            edit_menu.entryconfig("Copy", state="disabled")
            edit_menu.entryconfig("Bold", state="disabled")
            edit_menu.entryconfig("Underline", state="disabled")
            edit_menu.entryconfig("Italic", state="disabled")
            color_menu.entryconfig("Selected Text", state="disabled")
            break
        time.sleep(0.5)
    try:
        enable()
    except RuntimeError:
        pass


def enable():
    while True:
        if "sel" in my_text.tag_names(INSERT):
            edit_menu.entryconfig("Cut", state="normal")
            edit_menu.entryconfig("Copy", state="normal")
            edit_menu.entryconfig("Bold", state="normal")
            edit_menu.entryconfig("Underline", state="normal")
            edit_menu.entryconfig("Italic", state="normal")
            color_menu.entryconfig("Selected Text", state="normal")
            disable()
        time.sleep(0.5)


def find(event=None):
    w = Find(root)
    root.wait_window(w.top)
    print(w.value)


# ScrollBar

text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)
# Text Box

my_text = Text(my_frame, font=("Arial", 11), selectbackground="light blue", selectforeground="black", undo=True,
               yscrollcommand=text_scroll.set, wrap="none", xscrollcommand=hor_scroll.set)
my_text.place(relheight=0.95, relwidth=0.95)

threading.Thread(target=check_saved).start()

text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)
# Menu Bar

my_menu = Menu(root)
root.config(menu=my_menu)

# File menu

file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="(Ctrl+N)")
file_menu.bind_all("<Control-n>", new_file)
file_menu.add_command(label="Open", command=open_file, accelerator="(Ctrl+O)")
file_menu.bind_all("<Control-o>", open_file)
file_menu.add_command(label="Save", command=save_file, accelerator="(Ctrl+S)")
file_menu.bind_all("<Control-s>", save_file)
file_menu.add_command(label="Save As", command=save_as_file, accelerator="(Ctrl+Shift+S)")
file_menu.bind_all("<Control-Shift-S>", save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Print", command=print_file, accelerator="(Ctrl+P)")
file_menu.bind_all("<Control-p>", print_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit, accelerator="(Ctrl+Q)")
file_menu.bind_all("<Control-q>", on_closing)

# Edit menu

edit_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: my_text.event_generate("<<Cut>>"), accelerator="(Ctrl+X)",
                      state="disabled")
edit_menu.add_command(label="Copy", command=lambda: my_text.event_generate("<<Copy>>"), accelerator="(Ctrl+C)",
                      state="disabled")
edit_menu.add_command(label="Paste", command=lambda: my_text.event_generate("<<Paste>>"), accelerator="(Ctrl+V)")
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="(Ctrl+Z)")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="(Ctrl+Y)")
edit_menu.add_separator()
edit_menu.add_command(label="Bold", accelerator="(Ctrl+B)", command=bold_it, state="disabled")
edit_menu.bind_all("<Control-b>", bold_it)
edit_menu.add_command(label="Italic", accelerator="(Ctrl+G)", command=italic_it, state="disabled")
edit_menu.bind_all("<Control-g>", italic_it)
edit_menu.add_command(label="Underline", accelerator="(Ctrl+U)", command=underline_it, state="disabled")
edit_menu.bind_all("<Control-u>", underline_it)
edit_menu.add_separator()
edit_menu.add_command(label="Selct All", command=select_all, accelerator="(Ctrl+A)")
edit_menu.add_command(label="Clear All", command=clear_all)

# color_menu
color_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Color", menu=color_menu)
color_menu.add_command(label="Selected Text", command=text_colour, state="disabled")
color_menu.add_command(label="All Text", command=all_text_color)
color_menu.add_command(label="Background", command=bg_color)

# Find_menu
find_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Find", menu=find_menu)
find_menu.add_command(label="Find", accelerator="(Ctrl+F)", command=find)
find_menu.bind_all("<Control-f>", find)
find_menu.add_command(label="Find All", accelerator="(Ctrl+Shift+F)")
find_menu.add_command(label="Find and Replace")

threading.Thread(target=disable).start()

# Options_menu
options_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Night_mode on", command=night_on)
options_menu.add_command(label="Night mode off", command=night_off)
# Status bar

status_bar = Label(root, text='Ready      ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
