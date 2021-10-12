from tkinter import *
from tkinter.font import Font
from tkinter import filedialog
import os, pickle

root = Tk()
root.title("To Do List!")
root.geometry("430x460")

# Font
my_font = Font(
    family="Brush Script Mt",
    size=30,
    weight="bold")

my_frame = Frame(root)
my_frame.pack(pady=10)

my_list = Listbox(my_frame,
                  font=my_font,
                  width=20,
                  height=5,
                  bg="SystemButtonFace",
                  bd=0,
                  fg="#464646",
                  highlightthickness=0,
                  selectbackground="#a6a6a6",
                  activestyle="none")

# my_list.place(side=LEFT, relheight=0.5)
my_list.pack(side=LEFT, fill=BOTH)

# stuff = ["Learn tkinter", "Do python", "apple", "banana", "cherry", "apple", "cherry"]

# for item in stuff:
#     my_list.insert(END, item)

my_scrollbar = Scrollbar(my_frame)
my_scrollbar.pack(side=RIGHT, fill=BOTH)

my_list.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_list.yview())

my_entry = Entry(root, font=30)
my_entry.pack(pady=15, padx=15, fill=X)

button_frame = Frame(root)
button_frame.pack(pady=20)


def delete_item():
    my_list.delete(ANCHOR)


def add_item():
    if my_entry.get():
        my_list.insert(END, my_entry.get())
        my_entry.delete(0,END)


def cross_off_item():
    my_list.itemconfig(
        my_list.curselection(),
        fg="#dedede")

    my_list.selection_clear(0,END)


def uncross_item():
    my_list.itemconfig(
        my_list.curselection(),
        fg="#464646")

    my_list.selection_clear(0,END)


def delete_crossed_item():
    count = 0
    while count < my_list.size():
        if my_list.itemcget(count, "fg") == "#dedede":
            my_list.delete(my_list.index(count))

        else:
            count += 1
        
def open_list():
    file_name = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Open File",
        filetypes=(
            ("Dat Files", "*.dat"),
            ("All Files", "*.*"))
        )

    if file_name:
        my_list.delete(0,END)

        input_file = open(file_name, 'rb')

        stuff = pickle.load(input_file)

        for item in stuff:
           my_list.insert(END, item) 
            
def save_list():
    file_name = filedialog.asksaveasfilename(
        initialdir=os.getcwd(),
        title="Save File",
        filetypes=(
            ("Dat Files", "*.dat"),))
    if file_name:
        if file_name.endswith(".dat"):
            pass
        else:
            file_name = f'{file_name}.dat'
    
    delete_crossed_item()

    stuff = my_list.get(0,END)

    output_file = open(file_name, 'wb')

    pickle.dump(stuff, output_file)

            
def clear_list():
    my_list.delete(0,END)


my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Save List", command=save_list)
file_menu.add_command(label="Open List", command=open_list)
file_menu.add_separator()
file_menu.add_command(label="Clear List", command=clear_list)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.destroy)

delete_button = Button(button_frame, text="Delete Item", command=delete_item)
add_button = Button(button_frame, text="Add Item", command=add_item)
cross_button = Button(button_frame, text="Cross Off Item", command=cross_off_item)
uncross_button = Button(button_frame, text="Uncross Item", command=uncross_item)
delete_crossed_button = Button(button_frame, text="Delete Crossed One", command=delete_crossed_item)

delete_button.grid(row=1, column=0, pady=10, padx=10)
add_button.grid(row=0, column=0, padx=10)
cross_button.grid(row=0, column=1)
uncross_button.grid(row=0, column=2, padx=10)
delete_crossed_button.grid(row=1, column=2)
root.mainloop()
