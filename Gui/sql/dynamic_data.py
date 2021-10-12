from tkinter import *
import mysql.connector
import sqlite3
from tkinter import messagebox

# my_sql = sqlite3.connect('Data_collector.db')

my_sql = mysql.connector.connect(host='localhost', user='root', passwd='vishal@sql@123', database='data_collector')

my_cursor = my_sql.cursor()

root = Tk()
root.title("Dynamic Data collector sql")
root.geometry("360x350")
sql_command = """create table if not exists dynamic(id int primary key AUTO_INCREMENT,
			  entry_0 VARCHAR(45) NULL,
			  entry_1 VARCHAR(45) NULL,
			  entry_2 VARCHAR(45) NULL,
			  entry_3 VARCHAR(45) NULL,
			  entry_4 VARCHAR(45) NULL,
			  entry_5 VARCHAR(45) NULL,
			  entry_par_0 VARCHAR(45) NULL,
			  entry_par_1 VARCHAR(45) NULL,
			  entry_par_2 VARCHAR(45) NULL,
			  entry_par_3 VARCHAR(45) NULL,
			  entry_par_4 VARCHAR(45) NULL,
			  entry_par_5 VARCHAR(45) NULL);"""

my_cursor.execute(sql_command)
entries = {}


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


def add():
	global num, entries, minus, submit_but, frame, add_but
	num += 0.13		

	entry = CEntry(frame, font=('ariel', 15))
	entry.place(relx=0.05, rely=num, relheight=0.1, relwidth=0.3)

	label = Label(frame, text=':',font=('bold', 15), bg="#80c1ff")
	label.place(relx=0.37, rely=num, relheight=0.1, relwidth=0.01)

	entry_par  = CEntry(frame, font=('ariel', 15))
	entry_par.place(relx=0.4, rely=num, relheight=0.1, relwidth=0.35)
	
	entries[entry] = (entry_par, label)
	if not num == 0.75:
		add_but.place(relx=0.775, rely=num, relwidth=0.08, relheight=0.1)
		minus.place(relx=0.89, rely=num, relwidth=0.08, relheight=0.1)
	else:
		add_but.place_forget()
		minus.place(relx=0.775, rely=num, relwidth=0.08, relheight=0.1)
	submit_but.place(relx=0.3, rely=num+0.13, relwidth=0.2, relheight=0.1)
		
def submit():

	if len(entries) == 1:
		i = list(entries.keys())[0]
		field_1, field_2 = 'entry_0' , 'entry_par_0'
		if i.get():
			my_cursor.execute("insert into dynamic (%s, %s) values('%s', '%s')"%(field_1, field_2, i.get(), entries[i][0].get()))
			my_sql.commit()
			main()
		else:
			messagebox.showerror("Dynamic Data_collector", "Field Name Values are compulsory")
		

	elif len(entries) == 2:
		val, field_val, fields = [], [], []
		for i in range(2):
			field_val.append(list(entries.keys())[i].get())
			val.append(list(entries.values())[i][0].get())
			fields.append('entry_'+str(i))
			fields.append('entry_par_'+str(i))
		if not '' in field_val:
			my_cursor.execute("insert into dynamic (%s,%s,%s,%s) values('%s','%s','%s','%s')"%(fields[0], fields[1], fields[2], fields[3], field_val[0], val[0], field_val[1], val[1]))
			my_sql.commit()
			main()
		else:
			messagebox.showerror("Dynamic Data_collector", "Field Name Values are compulsory")

	elif len(entries) == 3:
		val, field_val, fields = [], [], []
		for i in range(3):
			field_val.append(list(entries.keys())[i].get())
			val.append(list(entries.values())[i][0].get())
			fields.append('entry_'+str(i))
			fields.append('entry_par_'+str(i))
		if not '' in field_val:
			my_cursor.execute("insert into dynamic (%s,%s,%s,%s,%s,%s) values('%s','%s','%s','%s','%s','%s')"%(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], field_val[0], val[0], field_val[1], val[1], field_val[2], val[2]))
			my_sql.commit()
			main()
		else:
			messagebox.showerror("Dynamic Data_collector", "Field Name Values are compulsory")
		

	elif len(entries) == 4:
		val, field_val, fields = [], [], []
		for i in range(4):
			field_val.append(list(entries.keys())[i].get())
			val.append(list(entries.values())[i][0].get())
			fields.append('entry_'+str(i))
			fields.append('entry_par_'+str(i))
		if not '' in field_val:
			my_cursor.execute("insert into dynamic (%s,%s,%s,%s,%s,%s,%s,%s) values('%s','%s','%s','%s','%s','%s','%s','%s')"%(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], field_val[0], val[0], field_val[1], val[1], field_val[2], val[2], field_val[3], val[3]))
			my_sql.commit()
			main()
		else:
			messagebox.showerror("Dynamic Data_collector", "Field Name Values are compulsory")
		

	elif len(entries) == 5:
		val, field_val, fields = [], [], []
		for i in range(5):
			field_val.append(list(entries.keys())[i].get())
			val.append(list(entries.values())[i][0].get())
			fields.append('entry_'+str(i))
			fields.append('entry_par_'+str(i))
		if not '' in field_val:
			my_cursor.execute("insert into dynamic (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8], fields[9], field_val[0], val[0], field_val[1], val[1], field_val[2], val[2], field_val[3], val[3], field_val[4], val[4]))
			my_sql.commit()
			main()
		else:
			messagebox.showerror("Dynamic Data_collector", "Field Name Values are compulsory")
		

	elif len(entries) == 6:
		val, field_val, fields = [], [], []
		for i in range(6):
			field_val.append(list(entries.keys())[i].get())
			val.append(list(entries.values())[i][0].get())
			fields.append('entry_'+str(i))
			fields.append('entry_par_'+str(i))
		if not '' in field_val:
			my_cursor.execute("insert into dynamic (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8], fields[9], fields[10], fields[11], field_val[0], val[0], field_val[1], val[1], field_val[2], val[2], field_val[3], val[3], field_val[4], val[4], field_val[5], val[5]))
			my_sql.commit()
			main()
		else:
			messagebox.showerror("Dynamic Data_collector", "Field Name Values are compulsory")
		
def minuser():
	global num, entries
	if num > 0.23:
		# print('1',num)
		i = len(entries) - 1
		list(entries.keys())[i].destroy()
		list(entries.values())[i][0].destroy()
		list(entries.values())[i][1].destroy()
		key = list(entries.keys())[i]
		del entries[key]
		num -= 0.13
		num = round(num, 2)
		# print(num)
		add_but.place(relx=0.775, rely=num, relwidth=0.08, relheight=0.1)
		submit_but.place(relx=0.3, rely=num+0.13, relwidth=0.2, relheight=0.1)
		minus.place(relx=0.89, rely=num, relwidth=0.08, relheight=0.1)
	elif num == 0.23:
		# print('2',num)
		i = len(entries) - 1
		list(entries.keys())[i].destroy()
		list(entries.values())[i][0].destroy()
		list(entries.values())[i][1].destroy()
		key = list(entries.keys())[i]
		del entries[key]
		num -= 0.13
		minus.place_forget()
		add_but.place(relx=0.775, rely=num, relwidth=0.08, relheight=0.1)
		submit_but.place(relx=0.3, rely=num+0.13, relwidth=0.2, relheight=0.1)

def main():
	global num, entries, minus, submit_but, frame, add_but
	num = 0.1
	try:
		frame.destroy()
		entries = {}
	except NameError:
		pass

		
	frame = Frame(root, bg="#80c1ff")
	frame.place(relx=0.001, relheight=1, relwidth=1)

	Label(frame, text='Field Name', font=('bold',10), bg="#80c1ff").place(relx=0.035, rely=0.01, relwidth=0.3, relheight=0.07)
	Label(frame, text='Field Value', font=('bold',10), bg="#80c1ff").place(relx=0.43, rely=0.01, relwidth=0.3, relheight=0.07)

	entry = CEntry(frame, font=('ariel', 15))
	entry.place(relx=0.05, rely=num, relheight=0.1, relwidth=0.3)

	label = Label(frame, text=':', font=('bold', 15), bg="#80c1ff")
	label.place(relx=0.37, rely=num, relheight=0.1, relwidth=0.01)

	entry_par  = CEntry(frame, font=('ariel', 15))
	entry_par.place(relx=0.4, rely=num, relheight=0.1, relwidth=0.35)

	entries[entry] = (entry_par, label)

	minus = Button(frame, text="-", font=('ariel', 14), command=minuser)

	add_but = Button(frame, text="+", font=('bold', 14), command=add)
	add_but.place(relx=0.775, rely=num, relwidth=0.08, relheight=0.1)

	submit_but = Button(frame, text="Submit", font=('bold', 15), command=submit)
	submit_but.place(relx=0.3, rely=num+0.13, relwidth=0.2, relheight=0.1)

if __name__ == '__main__':
	main()

root.mainloop()