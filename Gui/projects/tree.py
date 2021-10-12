from tkinter import *
from tkinter import ttk

root = Tk()
root.title("TreeView")
root.geometry("450x550")

style = ttk.Style()

# style.theme_use("default")

style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white")

style.map('Treeview',
          background=[('selected', 'blue')])

tree_frame = Frame(root)
tree_frame.pack(pady=20)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='browse')
my_tree.pack()

tree_scroll.config(command=my_tree.yview)

my_tree['columns'] = ("Name", "ID")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Name", anchor=W, width=120)
my_tree.column("ID", anchor=E, width=100)
# my_tree.column("Favorite Item", anchor=W, width=120)

my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("ID", text="ID", anchor=E)
# my_tree.heading("Favorite Item", text="Favorite Item", anchor=W)

data = [("Vishal", 1, "Bread"),
        ("John", 2, "Jam"),
        ("Naveen", 3, "Butter"),
        ("Ram", 4, "Cake")
        ]


my_tree.tag_configure("oddrow", background="white")
my_tree.tag_configure("evenrow", background="lightblue")

count = 0
for record in data:
    if count % 2 == 0:
        my_tree.insert(parent='', index='end', iid=record[0], text="", values=(record[0], record[1], record[2]), tags=('evenrow',))
    else:
        my_tree.insert(parent='', index='end', iid=record[0], text="", values=(record[0], record[1], record[2]), tags=('oddrpw',))

    count += 1

# Add Data
# my_tree.insert(parent='', index='end', iid=0, text="", values=("Vishal", 1, "Bread"))
# my_tree.insert(parent='', index='end', iid=1, text="", values=("John", 2, "Jam"))
# my_tree.insert(parent='', index='end', iid=2, text="", values=("Naveen", 3, "Butter"))
# my_tree.insert(parent='', index='end', iid=3, text="", values=("Ram", 4, "Cake"))

# my_tree.insert(parent='0', index='end', iid=6, text="Child", values=("Ravi", 1.2, "Pizza"))
my_tree.pack(pady=10)

def show():
	selected = my_tree.focus()
	# value = my_tree.item(selected, 'iid')
	nl.config(text=selected)

add_frame = Frame(root)
add_frame.pack(pady=10)
#
nl = Label(add_frame, text="")
nl.grid(row=0, column=0)
#
# il = Label(add_frame, text="ID")
# nl.grid(row=0, column=1)
#
# tl = Label(add_frame, text="Item")
# tl.grid(row=0, column=2)
#
# name_box = Entry(add_frame)
# name_box.grid(row=1, column=0)
#
# id_box = Entry(add_frame)
# id_box.grid(row=1, column=1)
#
# item_box = Entry(add_frame)
# item_box.grid(row=1, column=2)

# add_record = Button(root, text="Add Record", )

select = Button(add_frame, text="Select", command=show)
select.grid(row=1, column=0)

root.mainloop()
