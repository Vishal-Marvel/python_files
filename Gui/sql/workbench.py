from tkinter import *
import tkinter as tk
from tkinter import ttk, tix
from tkinter import messagebox, filedialog
import mysql.connector
from datetime import datetime
import sqlite3
# import pandas as pd
import time, threading

class MyDialog:

    def __init__(self, parent, text):
        top = self.top = tk.Toplevel(parent)
        top.geometry("215x100")
        self.myLabel = tk.Label(top, text=text)
        self.myLabel.pack(padx=20, pady=5, anchor=CENTER)
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack(padx=10, pady=10)
        self.myEntryBox.focus()
        top.bind_all("<Return>", self.top_on_closing)
        self.mySubmitButton = tk.Button(top, text='Submit', command=self.top_on_closing)
        self.mySubmitButton.pack(padx=10, anchor=CENTER)
        top.protocol("WM_DELETE_WINDOW", self.top_on_closing)
        

    def top_on_closing(self, event=None):
        if self.myEntryBox.get() == '':
            messagebox.showerror('WorkBench', 'Datatype is compulsory')
            self.top.after(1, lambda: self.top.focus_force())
            self.myEntryBox.focus()
        else:
            self.input = self.myEntryBox.get()
            self.top.destroy()


class ScrollableFrame(Frame):
    """
    There is no way to scroll <tkinter.Frame> so we are
    going to create a canvas and place the frame there.
    Scrolling the canvas will give the illusion of scrolling
    the frame
    Partly taken from:
        https://blog.tecladocode.com/tkinter-scrollable-frames/
        https://stackoverflow.com/a/17457843/11106801
    master_frame---------------------------------------------------------
    | dummy_canvas-----------------------------------------  y_scroll--  |
    | | self---------------------------------------------  | |         | |
    | | |                                                | | |         | |
    | | |                                                | | |         | |
    | | |                                                | | |         | |
    | |  ------------------------------------------------  | |         | |
    |  ----------------------------------------------------   ---------  |
    | x_scroll---------------------------------------------              |
    | |                                                    |             |
    |  ----------------------------------------------------              |
     --------------------------------------------------------------------
    """
    def __init__(self, master=None, scroll_speed:int=2, hscroll:bool=False,
                 vscroll:bool=True, bd:int=0, scrollbar_kwargs={},
                 bg="#f0f0ed", **kwargs):
        assert isinstance(scroll_speed, int), "`scroll_speed` must be an int"
        self.scroll_speed = scroll_speed

        self.master_frame = tk.Frame(master, bd=bd, bg=bg)
        self.master_frame.grid_rowconfigure(0, weight=1)
        self.master_frame.grid_columnconfigure(0, weight=1)
        self.dummy_canvas = tk.Canvas(self.master_frame, highlightthickness=0,
                                      bd=0, bg=bg, **kwargs)
        super().__init__(self.dummy_canvas, bg=bg)

        # Create the 2 scrollbars
        if vscroll:
            self.v_scrollbar = tk.Scrollbar(self.master_frame,
                                            orient="vertical",
                                            command=self.dummy_canvas.yview,
                                            **scrollbar_kwargs)
            self.v_scrollbar.grid(row=0, column=1, sticky="news")
            self.dummy_canvas.configure(yscrollcommand=self.v_scrollbar.set)
        if hscroll:
            self.h_scrollbar = tk.Scrollbar(self.master_frame,
                                            orient="horizontal",
                                            command=self.dummy_canvas.xview,
                                            **scrollbar_kwargs)
            self.h_scrollbar.grid(row=1, column=0, sticky="news")
            self.dummy_canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Bind to the mousewheel scrolling
        self.dummy_canvas.bind_all("<MouseWheel>", self.scrolling_windows,
                                   add=True)
        self.dummy_canvas.bind_all("<Button-4>", self.scrolling_linux, add=True)
        self.dummy_canvas.bind_all("<Button-5>", self.scrolling_linux, add=True)
        self.bind("<Configure>", self.scrollbar_scrolling, add=True)

        # Place `self` inside `dummy_canvas`
        self.dummy_canvas.create_window((0, 0), window=self, anchor="nw")
        # Place `dummy_canvas` inside `master_frame`
        self.dummy_canvas.grid(row=0, column=0, sticky="news")

        self.pack = self.master_frame.pack
        self.grid = self.master_frame.grid
        self.place = self.master_frame.place
        self.pack_forget = self.master_frame.pack_forget
        self.grid_forget = self.master_frame.grid_forget
        self.place_forget = self.master_frame.place_forget

    def scrolling_windows(self, event:tk.Event) -> None:
        assert event.delta != 0, "On Windows, `event.delta` should never be 0"
        y_steps = int(-event.delta/abs(event.delta)*self.scroll_speed)
        self.dummy_canvas.yview_scroll(y_steps, "units")

    def scrolling_linux(self, event:tk.Event) -> None:
        y_steps = self.scroll_speed
        if event.num == 4:
            y_steps *= -1
        self.dummy_canvas.yview_scroll(y_steps, "units")

    def scrollbar_scrolling(self, event:tk.Event) -> None:
        region = list(self.dummy_canvas.bbox("all"))
        region[2] = max(self.dummy_canvas.winfo_width(), region[2])
        region[3] = max(self.dummy_canvas.winfo_height(), region[3])
        self.dummy_canvas.configure(scrollregion=region)

    def resize(self, fit:str=None, height:int=None, width:int=None) -> None:
        """
        Resizes the frame to fit the widgets inside. You must either
        specify (the `fit`) or (the `height` or/and the `width`) parameter.
        Parameters:
            fit:str       `fit` can be either `FIT_WIDTH` or `FIT_HEIGHT`.
                          `FIT_WIDTH` makes sure that the frame's width can
                           fit all of the widgets. `FIT_HEIGHT` is simmilar
            height:int     specifies the height of the frame in pixels
            width:int      specifies the width of the frame in pixels
        To do:
            ALWAYS_FIT_WIDTH
            ALWAYS_FIT_HEIGHT
        """
        if height is not None:
            self.dummy_canvas.config(height=height)
        if width is not None:
            self.dummy_canvas.config(width=width)
        # if fit == FIT_WIDTH:
        #     super().update()
        #     self.dummy_canvas.config(width=super().winfo_width())
        # elif fit == FIT_HEIGHT:
        #     super().update()
        #     self.dummy_canvas.config(height=super().winfo_height())
        else:
            raise ValueError("Unknow value for the `fit` parameter.")
    fit = resize


class Login:
    """
        Login Page which contains the entry fields for My SQL Server and file select option to pick a file
    """
    def __init__(self) -> None:
        self.database = Base()
    
    def initiate(self):
        self.login = Tk()
        self.login.title('WorkBench')
        self.login.geometry("500x460")
        # self.login.resizable(height=False, width=False)  
        login_frame = Frame(self.login)
        login_frame.pack(pady=20, padx=20, fill="both")


        Label(login_frame, text='Welcome the Python Workbench', font=('bold', 20)).pack(padx=20, pady=10, fill='x')
        frame = LabelFrame(login_frame, text='Via SQL Server', font=3)
        frame.pack(padx=10, pady=15, fill='x')

        Label(frame, text='Username:', font=15).grid(row=0, column=0, padx=20)
        self.uname = Entry(frame, font=20)
        self.uname.grid(row=0, column=1, padx=10, pady=20)

        Label(frame, text='Password:', font=15).grid(row=1, column=0, padx=20)
        self.passw = Entry(frame, font=20, show='*')
        self.passw.grid(row=1, column=1, padx=10)

        self.submit = Button(frame, text='Submit', font=15, command=self.validate_user)
        self.submit.grid(row=2, column=0, columnspan=10, padx=10, pady=10)
        
        self.frame_1 = LabelFrame(login_frame, text='Via A Database File', font=3)
        self.frame_1.pack(padx=10, pady=5, fill='x')
        
        Label(self.frame_1, text='Choosen File:', font=10).grid(row=0, column=0, padx=10, pady=10)
        
        self.text = StringVar()
        self.file_label = Label(self.frame_1, textvariable=self.text, font=('bold', 13))
        self.file_label.grid(row=0, column=1)
        self.login.bind_all('<Return>', self.validate_user)
        self.text.set('None')
        
        self.choose = Button(self.frame_1, text='Choose File', font=10, command=self.choose_file)
        self.choose.grid(row=0, column=2, pady=10, padx=10)
        
        def entry2_focus(event):
            self.stopper = False
            threading.Thread(target=hide).start()

        def hide():
            while True:
                if self.uname.get():
                    self.choose.config(state='disabled')
                    self.file_label.config(state='disabled')
                    break
                time.sleep(0.1)
            try:
                show()
            except RuntimeError:
                pass

        def show():
            while True:
                if self.stopper:
                    break
                if self.uname.get() == "":
                    self.choose.config(state='normal')
                    self.file_label.config(state='normal')
                    hide()
                
                time.sleep(0.1)
        self.uname.bind("<FocusIn>", entry2_focus)
        self.login.mainloop()
    
    def choose_file(self):
        self.uname.config(state='disabled')
        self.passw.config(state='disabled')
        self.submit.config(state='disabled')
        self.db_file = filedialog.askopenfilename(title='Open File', filetypes=(('Database, *.db'),))
        if self.db_file:
            filename = self.db_file.split('/')[-1]
            self.text.set(filename)
            
            def pass_through(event=None):
                self.login.destroy()
                self.database.table.initiate(self.db_file, sqlite=True)
            self.login.bind_all('<Return>', pass_through)  
            Button(self.frame_1, text='Open', font=10, command=pass_through).grid(row=1, column=0, columnspan=10, pady=5)
        else: 
            self.uname.config(state='normal')
            self.passw.config(state='normal')
            self.submit.config(state='normal')

    def validate_user(self, event=None):
        self.stopper = True
        try:
            mysql.connector.connect(host='localhost', user=self.uname.get(), passwd=self.passw.get())
        except mysql.connector.errors.ProgrammingError as e:
            messagebox.showerror("WorkBench", str(e))
        else:
            uname, passw = self.uname.get(), self.passw.get()
            self.login.destroy()
            self.database.initiate(uname, passw)
            

class Base:
    def __init__(self):
        self.table = Table()

    def initiate(self, uname, passw):
        self.uname = uname
        self.passw = passw
        self.base = Tk()
        self.base.title('Databases')
        self.base.geometry("300x300")
        self.base.resizable(height=False, width=False)
        # Create a Treeview Frame
        base_tree_frame = Frame(self.base)
        base_tree_frame.pack(pady=20,padx=20, fill="both")

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        # style.theme_use('default')

        # Configure the Treeview Colors
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white")

        # Change Selected Color
        style.map('Treeview',
                  background=[('selected', 'blue')])

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(base_tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        self.base_tree = ttk.Treeview(base_tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.base_tree.pack(fill="both")
        
        self.base_tree.tag_configure("oddrow", background="white")
        self.base_tree.tag_configure("evenrow", background="lightblue")

        # Configure the Scrollbar
        tree_scroll.config(command=self.base_tree.yview)

        self.base_tree['columns'] = ("S.No.", "DataBase Name")

        #Column sort func
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)

            # rearrange items in sorted positions
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            # reverse sort next time
            tv.heading(col, text=col, command=lambda _col=col: \
                        treeview_sort_column(tv, _col, not reverse))

        #Add Column
        self.base_tree.column("#0", width=0, stretch=NO)
        self.base_tree.column("S.No.", anchor=CENTER, width=40, minwidth=40)
        self.base_tree.column("DataBase Name", anchor=CENTER, width=140, minwidth=150)

        #Add Heading
        self.base_tree.heading("#0", text="", anchor=W)
        self.base_tree.heading("S.No.", text="S.No.", anchor=CENTER)
        self.base_tree.heading("DataBase Name",
         text="DataBase Name", anchor=CENTER, 
        command=lambda _col="DataBase Name": treeview_sort_column(self.base_tree, _col, False))

        self.add_items()
        self.create_menu()

        self.base.protocol("WM_DELETE_WINDOW", self.base_on_closing)
        self.base_tree.bind("<Double-1>", self.select_record)
        self.base.after(1, lambda: self.base.focus_force())
        self.base.mainloop()

    def add_items(self):
        
        my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw)
        self.cursor = my_sql.cursor()
        self.cursor.execute('SHOW DATABASES;')
        databases = self.cursor.fetchall()
        count = 1
        for record in databases:
            if count % 2 != 0:
                self.base_tree.insert(parent='', index='end', iid=count, text='', values=(count, record[0]), tags=('evenrow',))
            else:
                self.base_tree.insert(parent='', index='end', iid=count, text='', values=(count, record[0]), tags=('oddrow',))
            # increment counter
            count += 1
        my_sql.close()

    #Menu BAr
    def create_menu(self):
        self.my_menu = Menu(self.base)
        self.base.config(menu=self.my_menu)
        # self.file_mennu = Menu(self.my_menu, tearoff=0)
        self.my_menu.add_command(label='Log Out', command=lambda: logout())

        def logout():
            self.base_on_closing()
            l.initiate()

    #Close Function
    def base_on_closing(self, event=None):
        self.base.destroy()

    def select_record(self, event=None):
        selected = self.base_tree.focus()
        value = self.base_tree.item(selected, 'values')[1]
        self.base_on_closing()
        self.table.initiate(value, self.uname, self.passw)


class Table:
    def __init__(self):
        self.view = ViewTable()
        self.alter = Alter_Table()
        pass
    
    def initiate(self, database, uname=None, passw=None, sqlite=False):
        self.sqlite = sqlite
        self.uname = uname
        self.passw = passw
        self.create_table_box = False
        self.database = database
        self.table = Tk()
        self.table.resizable(height=False, width=False)
        self.table.title(f"Tables in '{database.split('/')[-1]}'")
        self.table.geometry("400x400")

        # Create a Treeview Frame
        table_tree_frame = Frame(self.table)
        table_tree_frame.pack(pady=20, padx=20, fill=X)

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        # style.theme_use('default')

        # Configure the Treeview Colors
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white")

        # Change Selected Color
        style.map('Treeview',
                  background=[('selected', 'blue')])

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(table_tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        self.table_tree = ttk.Treeview(table_tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.table_tree.pack(fill="both")
        
        self.table_tree.tag_configure("oddrow", background="white")
        self.table_tree.tag_configure("evenrow", background="lightblue")

        # Configure the Scrollbar
        tree_scroll.config(command=self.table_tree.yview)

        self.table_tree['columns'] = ("S.No.", "Table Name")
        
        #Column sort func
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)

            # rearrange items in sorted positions
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            # reverse sort next time
            tv.heading(col, text=col, command=lambda _col=col: \
                        treeview_sort_column(tv, _col, not reverse))

        #Add Column
        self.table_tree.column("#0", width=0, stretch=NO)
        self.table_tree.column("S.No.", anchor=CENTER, width=30, minwidth=30)
        self.table_tree.column("Table Name", anchor=W, width=140, minwidth=150)

        #Add Heading
        self.table_tree.heading("#0", text="", anchor=W)
        self.table_tree.heading("S.No.", text="S.No.", anchor=CENTER)
        self.table_tree.heading("Table Name", text="Table Name", anchor=CENTER,
        command=lambda _col="Table Name": treeview_sort_column(self.table_tree, _col, False))

        # self.table_tree.bind("<ButtonRelease-1>", self.select_record)
        self.table_tree.bind("<Double-1>", self.view_table)
        
        self.create_menu()
        self.add_items()

        # Add Buttons
        button_frame = LabelFrame(self.table, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        self.view_button = Button(button_frame, text="View Table", command=self.view_table)
        self.view_button.grid(row=0, column=0, padx=10, pady=10)

        self.alter_button = Button(button_frame, text="Alter Table", command=self.alter_table)
        self.alter_button.grid(row=0, column=1, padx=5, pady=10)

        self.truncate_button = Button(button_frame, text="Truncate Table", command=self.truncate_table)
        self.truncate_button.grid(row=0, column=2, padx=5, pady=10)

        self.drop_button = Button(button_frame, text="Drop Table", command=self.drop_table)
        self.drop_button.grid(row=0, column=3, padx=10, pady=10)

        self.table.protocol("WM_DELETE_WINDOW", self.table_on_closing)
        self.table.after(1, lambda: self.table.focus_force())
        self.table.mainloop()

    #View Table func
    def view_table(self, event=None):
        selected = self.table_tree.focus()
        if selected:
            value = self.table_tree.item(selected, 'values')[1]
            self.table_on_closing()
            self.view.initiate(self.database, value, self.uname, self.passw, self.sqlite)
        else:
            messagebox.showerror('Workbench', 'Select A Table To VIEW !')
            self.table.after(1, lambda: self.table.focus_force())

    #Alter Table func
    def alter_table(self):
        if not self.sqlite:
            selected = self.table_tree.focus()
            if selected:
                value = self.table_tree.item(selected, 'values')[1]
                self.table_on_closing()
                self.alter.initiate(self.database, value, self.uname, self.passw, self.sqlite)
            else:
                messagebox.showerror('Workbench', 'Select A Table To ALTER !')
                self.table.after(1, lambda: self.table.focus_force())
        else:
            messagebox.showinfo('Workbench', 'This feature is not available right now')
            self.table.after(1, lambda: self.table.focus_force())

    #Drop Table func
    def drop_table(self):
        selected = self.table_tree.focus()
        if selected:
            value = self.table_tree.item(selected, 'values')[1]
            if messagebox.askokcancel('Workbench', 'Confirm Drop Table?\nOnce Dropped Can\'t be brought back!'):
                if not self.sqlite:
                    my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
                else:
                    my_sql = sqlite3.connect(self.database)
                self.cursor = my_sql.cursor()
                self.cursor.execute(f'DROP TABLE `{value}`')
                my_sql.close()
                self.refresh()
                messagebox.showinfo('Workbench', 'Table Dropped successfully')
                self.table.after(1, lambda: self.table.focus_force())
        else:
            messagebox.showerror('Workbench', 'Select A Table To DROP !')
            self.table.after(1, lambda: self.table.focus_force())

    #Truncate Table func
    def truncate_table(self):
        selected = self.table_tree.focus()
        if selected:
            value = self.table_tree.item(selected, 'values')[1]
            if messagebox.askokcancel('Confirm', 'Confirm Truncate Table?'):
                if not self.sqlite:
                    my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
                else:
                    my_sql = sqlite3.connect(self.database)
                self.cursor = my_sql.cursor()
                self.cursor.execute(f'TRUNCATE `{value}`')
                my_sql.close()
                messagebox.showinfo('Workbench', 'Table Truncated successfully')
                self.table.after(1, lambda: self.table.focus_force())
        else:
            messagebox.showerror('Workbench', 'Select A Table To Truncate !')
            self.table.after(1, lambda: self.table.focus_force())

    def add_items(self):
        if not self.sqlite:
            my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
            self.cursor = my_sql.cursor()
            self.cursor.execute('SHOW TABLES;')
            tables = self.cursor.fetchall()
        else:
            my_sql = sqlite3.connect(self.database)
            self.cursor = my_sql.cursor()
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
        count = 1
        for record in tables:
            if count % 2 != 0:
                self.table_tree.insert(parent='', index='end', iid=count, text='', values=(count, record[0]), tags=('evenrow',))
            else:
                self.table_tree.insert(parent='', index='end', iid=count, text='', values=(count, record[0]), tags=('oddrow',))
            # increment counter
            count += 1
        my_sql.close()
    
    def refresh(self):
        for i in self.table_tree.get_children():
            self.table_tree.delete(i)
        # time.sleep(3)
        self.add_items()

    #Menu Bar
    def create_menu(self):
        self.my_menu = Menu(self.table)
        self.table.config(menu=self.my_menu)
        if not self.sqlite:
            self.my_menu.add_command(label="See Databases", command=lambda: self.view_databases())
        self.my_menu.add_command(label='Refresh', command=lambda: self.refresh())
        self.my_menu.add_command(label="Create Table", command=lambda: self.create_table_init())
        def logout():
            self.table_on_closing()
            l.initiate()

    def view_databases(self):
        self.table_on_closing()
        b.initiate(self.uname, self.passw)

    #Close Function
    def table_on_closing(self, event=None):
        if self.create_table_box:
            self.create_table_on_close()
        self.table.destroy()


    def create_table_init(self):
        if not self.create_table_box:
            self.create_table_box = True
            self.row_num = -1
            self.create_table = tix.Tk()
            self.create_table.resizable(height=False, width=False)
            self.create_table.title(f"Create Table in {self.database.split('/')[-1]}")
            self.create_table.geometry("570x410")

            main_frame = Frame(self.create_table)
            main_frame.pack(expand=1, fill='both', anchor=CENTER)

            frame = Frame(main_frame)
            frame.place(relx=0.001, rely=0.01, relwidth=1)

            first_frame = Frame(frame)
            first_frame.pack(padx=10, fill=X)

            Label(first_frame, text='Create Table', font=10).grid(padx=10, row=0, columnspan=10)

            table_name_frame = Frame(first_frame)
            table_name_frame.grid(row=1, columnspan=10)
            Label(table_name_frame, text='Table Name :', font=10).grid(row=0, column=0, padx=20)

            self.table_name_entry = Entry(table_name_frame, font=10, width=15)
            self.table_name_entry.grid(row=0, column=1, padx=10, pady=10)
            self.table_name_entry.focus()

            Label(first_frame, text='Column Name', font=10).grid(row=2, column=0, padx=20, pady=5)
            Label(first_frame, text='Data Type', font=10).grid(row=2, column=1, padx=25, pady=5)
            pk = Label(first_frame, text='PK', font=10)
            pk.grid(row=2, column=2, padx=15, pady=5)
            uq = Label(first_frame, text='UQ', font=10)
            uq.grid(row=2, column=3, padx=10, pady=5)
            nn = Label(first_frame, text='NN', font=10)
            nn.grid(row=2, column=4, padx=10, pady=5)
            ai = Label(first_frame, text='AI', font=10)
            ai.grid(row=2, column=5, padx=12, pady=5)

            self.tip = tix.Balloon(self.create_table)

            self.tip.bind_widget(pk, msg='Primary Key')
            self.tip.bind_widget(uq, msg='Unique Index')
            self.tip.bind_widget(nn, msg='Not Null')
            self.tip.bind_widget(ai, msg='Auto Increment')

            self.second_frame = ScrollableFrame(frame, vscroll=True)
            self.second_frame.pack(side=LEFT, fill=BOTH, expand=1, anchor=CENTER)

            self.add_but = Button(main_frame, text='Add Next Row', font=10, command=self.add_row)
            self.add_but.place(relx=0.3, rely=0.9)

            self.submit_but = Button(main_frame, text='Submit', font=10, command=self.check_changes)
            self.submit_but.place(relx=0.6, rely=0.9)

            self.minus_but = Button(self.second_frame, text='- Row', font=('bold', 12), command=self.minus_row)
            self.create_table.protocol("WM_DELETE_WINDOW", self.create_table_on_close)
            self.create_table.after(1, lambda: self.create_table.focus_force())

            self.create_rows()
            self.add_row()
            
            self.create_table.mainloop()
        else:
            messagebox.showerror('WorkBench', 'Close the existing create table dialog box to open another')
            self.create_table.after(1, lambda: self.create_table.focus_force())

    def create_table_destroy(self):
        # self.minus_but = None
        self.create_table.destroy()
        self.create_table_box = False

    #On close event
    def create_table_on_close(self):
        # print(f'self.table_name_entry.get()-{self.table_name_entry.get()}, self.column_names[0].get()-{self.column_names[0].get()},', self.table_name_entry.get() == '' and self.column_names[0].get() == '')
        if self.table_name_entry.get() != '' or self.column_names[0].get() != '':
            q = messagebox.askyesnocancel('WorkBench', 'Dont you want to save changes?')
            if q:
                self.submit()
            elif q is False:
                self.create_table_destroy()
                self.create_table_box = False
            elif q is None:
                self.create_table.after(1, lambda: self.create_table.focus_force()) 
        else:
            self.create_table_destroy()
            self.create_table_box = False


    def create_rows(self):
        
        types = ['Select', 'INT', 'VARCHAR(30)', 'VARCHAR(50)', 'VARCHAR(100)', 'DATETIME', 'DECIMAL', 'FLOAT', 'Others']
        
        cl_nm_1, dty_1, pk_1, uq_1, nn_1, ai_1 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_2, dty_2, pk_2, uq_2, nn_2, ai_2 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_3, dty_3, pk_3, uq_3, nn_3, ai_3 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_4, dty_4, pk_4, uq_4, nn_4, ai_4 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_5, dty_5, pk_5, uq_5, nn_5, ai_5 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_6, dty_6, pk_6, uq_6, nn_6, ai_6 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_7, dty_7, pk_7, uq_7, nn_7, ai_7 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_8, dty_8, pk_8, uq_8, nn_8, ai_8 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_9, dty_9, pk_9, uq_9, nn_9, ai_9 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_10, dty_10, pk_10, uq_10, nn_10, ai_10 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_11, dty_11, pk_11, uq_11, nn_11, ai_11 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_12, dty_12, pk_12, uq_12, nn_12, ai_12 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_13, dty_13, pk_13, uq_13, nn_13, ai_13 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_14, dty_14, pk_14, uq_14, nn_14, ai_14 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_15, dty_15, pk_15, uq_15, nn_15, ai_15 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)

        self.column_names = [cl_nm_1, cl_nm_2, cl_nm_3, cl_nm_4, cl_nm_5, cl_nm_6, cl_nm_7, cl_nm_8, cl_nm_9, cl_nm_10, cl_nm_11, cl_nm_12, cl_nm_13, cl_nm_14, cl_nm_15]
        self.datatypes = [dty_1, dty_2, dty_3, dty_4, dty_5, dty_6, dty_7, dty_8, dty_9, dty_10, dty_11, dty_12, dty_13, dty_14, dty_15]
        self.pks = [pk_1, pk_2, pk_3, pk_4, pk_5, pk_6, pk_7, pk_8, pk_9, pk_10, pk_11, pk_12, pk_13, pk_14, pk_15]
        self.uqs = [uq_1, uq_2, uq_3, uq_4, uq_5, uq_6, uq_7, uq_8, uq_9, uq_10, uq_11, uq_12, uq_13, uq_14, uq_15]
        self.nns = [nn_1, nn_2, nn_3, nn_4, nn_5, nn_6, nn_7, nn_8, nn_9, nn_10, nn_11, nn_12, nn_13, nn_14, nn_15]
        self.ais = [ai_1, ai_2, ai_3, ai_4, ai_5, ai_6, ai_7, ai_8, ai_9, ai_10, ai_11, ai_12, ai_13, ai_14, ai_15]

    #Event handler for combobox
    def event_combobox(self, ai, cb):
        types = ['INT', 'VARCHAR(30)', 'VARCHAR(50)', 'VARCHAR(100)', 'DATETIME', 'DECIMAL', 'FLOAT', 'Others']
        if cb['values'][0] == 'Select':
            cb['values'] = types
        
        if cb.get() == 'Others':
            inputdialog = MyDialog(self.table, 'Enter the datatype')
            self.table.wait_window(inputdialog.top)
            cb['values'] = [inputdialog.input] + types
            cb.current(0)
        
        if str(cb.get()).upper() == 'INT':
            ai.configure(state=NORMAL)
        else:
            if 'selected' in ai.state():
                ai.invoke()
            ai.configure(state=DISABLED)
        
    #Add Row Funtion
    def add_row(self):
        def auto_invoke_nn(row_num):
            if 'selected' in self.pks[row_num].state(): 
                if 'selected' not in self.nns[row_num].state():
                    self.nns[row_num].invoke()
        self.row_num += 1
        self.column_names[self.row_num].grid(row=self.row_num, column=0, pady=5, padx=20)
        self.column_names[self.row_num].focus()

        self.datatypes[self.row_num].current(0)
        self.datatypes[self.row_num].grid(row=self.row_num, column=1, padx=12)
        self.datatypes[self.row_num].bind("<<ComboboxSelected>>", lambda event, ai=self.ais[self.row_num], cb=self.datatypes[self.row_num]: self.event_combobox(ai, cb))

        self.pks[self.row_num].grid(row=self.row_num, column=2, padx=13)
        self.pks[self.row_num].invoke()
        self.pks[self.row_num].invoke()
        self.pks[self.row_num].config(command=lambda row_num = self.row_num: auto_invoke_nn(row_num))

        self.uqs[self.row_num].grid(row=self.row_num, column=3, padx=15)
        self.uqs[self.row_num].invoke()
        self.uqs[self.row_num].invoke()

        self.nns[self.row_num].grid(row=self.row_num, column=4, padx=15)
        self.nns[self.row_num].invoke()
        self.nns[self.row_num].invoke()

        self.ais[self.row_num].grid(row=self.row_num, column=5, padx=13)
        self.ais[self.row_num].invoke()
        self.ais[self.row_num].invoke()
        self.ais[self.row_num].configure(state=DISABLED)

        if self.row_num > 0:
            self.minus_but.grid(row=self.row_num, column=6)

        if self.row_num > 13:
            self.add_but.config(state='disabled')
        else:
            self.add_but.config(state='normal')

    #Minus Row Function
    def minus_row(self):
        types = ['Select', 'INT', 'VARCHAR(30)', 'VARCHAR(50)', 'VARCHAR(100)', 'DATETIME', 'DECIMAL', 'FLOAT', 'Others']

        if self.column_names[self.row_num].get() != '':
            if messagebox.askokcancel('Workbench', 'Removing row will also delete the data in it'):
                self.column_names[self.row_num].delete(0, END)
            else:
                return
        self.column_names[self.row_num].grid_forget()

        self.datatypes[self.row_num].grid_forget()
        self.datatypes[self.row_num]['values'] = types
        self.datatypes[self.row_num].current(0)

        self.pks[self.row_num].grid_forget()
        self.pks[self.row_num].config(command=None)
        self.pks[self.row_num].state(['!selected'])

        self.uqs[self.row_num].grid_forget()
        self.uqs[self.row_num].state(['!selected'])

        self.nns[self.row_num].grid_forget()
        self.nns[self.row_num].state(['!selected'])

        self.ais[self.row_num].grid_forget()
        self.ais[self.row_num].state(['!selected'])

        self.row_num -= 1
        if self.row_num > 0:
            self.minus_but.grid(row=self.row_num, column=6)
        else:
            self.minus_but.grid_forget()
        if self.row_num > 13:
            self.add_but.config(state='disabled')
        else:
            self.add_but.config(state='normal')
          
    def check_changes(self):
        table_name = self.table_name_entry.get()
        if table_name != '':
            if table_name.lower() != 'table':
                column_details = {}
                for i in range(self.row_num + 1):
                    if self.column_names[i].get() != '':
                        if self.column_names[i].get().lower() != 'column': 
                            if self.datatypes[i].get() != 'Select':
                                column_details[self.column_names[i].get()] = (self.datatypes[i].get(), True if 'selected' in self.pks[i].state() else False, True if 'selected' in self.uqs[i].state() else False, True if 'selected' in self.nns[i].state() else False, True if 'selected' in self.ais[i].state() else False)
                            else:
                                messagebox.showerror('WorkBench', 'Cant Submit,\nPlease Select one datatype.')
                                self.create_table.after(1, lambda: self.create_table.focus_force())
                                self.datatypes[i].focus()
                                return
                        else:
                            messagebox.showerror('WorkBench', f'Column Name cannot be {self.column_names[i].get()}')
                            self.create_table.after(1, lambda: self.create_table.focus_force())
                            self.column_names[i].focus()
                            return
                    else:
                        messagebox.showerror('WorkBench', 'Cant Submit,\nColumn name can\'t be empty.')
                        self.create_table.after(1, lambda: self.create_table.focus_force())
                        self.column_names[i].focus()
                        return
                
                self.statement = f'CREATE TABLE `{table_name}` ( '

                for index,i in enumerate(column_details):
                    nn = 'NOT NULL ' if column_details[i][3] else 'NULL '
                    ai = 'AUTO_INCREMENT ' if column_details[i][4] else ''
                    uq = 'UNIQUE ' if column_details[i][2] else ''
                    pk = 'PRIMARY KEY ' if column_details[i][1] else ''
                    c = ',' if (index + 1) != len(column_details) else ''
                    self.statement += f'`{i}` {column_details[i][0]} {pk}{nn}{uq}{ai}{c}'

                self.statement += ');'
                self.submit()
            else:
                messagebox.showerror('WorkBench', f'Table Name cannot be {table_name}')
                self.create_table.after(1, lambda: self.create_table.focus_force())
                self.table_name_entry.focus()
        else:
            messagebox.showerror('WorkBench', 'Table Name is compulsory')
            self.create_table.after(1, lambda: self.create_table.focus_force())
            self.table_name_entry.focus()

    #Submit
    def submit(self):
        if self.statement:
            
            if messagebox.askokcancel('Confirm Create Table with this statement', self.statement):
                
                if self.sqlite:
                    try:
                        my_sql = sqlite3.connect(self.database)
                        cursor = my_sql.cursor()
                        cursor.execute(self.statement)
                        my_sql.commit()
                        my_sql.close()
                        self.create_table.destroy()
                        self.create_table_box = False
                        self.refresh()
                    except sqlite3.OperationalError as e:
                        messagebox.showerror('WorkBench', e)
                        self.create_table.after(1, lambda: self.create_table.focus_force())
                else:
                    try:
                        my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
                        cursor = my_sql.cursor()
                        cursor.execute(self.statement)
                        my_sql.commit()
                        my_sql.close()
                        self.create_table.destroy()
                        self.create_table_box = False
                        self.refresh()
                    except mysql.connector.errors.ProgrammingError as e:
                        messagebox.showerror('WorkBench', e)
                        self.create_table.after(1, lambda: self.create_table.focus_force())

        
class ViewTable:
    def __init__(self) -> None:
        pass

    def initiate(self, database, table, uname=None, passw=None, sqlite=False):
        self.uname = uname
        self.passw = passw
        self.sqlite = sqlite
        self.edit_boxs = False
        self.new=False
        self.primary_key = []
        self.database = database
        self.table = table
        self.view_table = Tk()
        # self.view_table.resizable(height=False, width=False)
        self.view_table.title(f"Table '{table}'")
        self.view_table.geometry('800x400')
        
        # Create a Treeview Frame
        view_table_tree_frame = Frame(self.view_table)
        view_table_tree_frame.pack(pady=15, padx=20, fill=X)

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        # style.theme_use('default')

        # Configure the Treeview Colors
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white")

        # Change Selected Color
        style.map('Treeview',
                  background=[('selected', 'blue')])

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(view_table_tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)
        tree_scroll_down = Scrollbar(view_table_tree_frame, orient='horizontal')
        tree_scroll_down.pack(side=BOTTOM, fill=X)

        # Create The Treeview
        self.view_table_tree = ttk.Treeview(view_table_tree_frame, yscrollcommand=tree_scroll.set, xscrollcommand=tree_scroll_down.set, selectmode="extended")
        self.view_table_tree.pack(fill="both")
        
        self.view_table_tree.tag_configure("oddrow", background="white")
        self.view_table_tree.tag_configure("evenrow", background="lightblue")

        # Configure the Scrollbar
        tree_scroll.config(command=self.view_table_tree.yview)
        tree_scroll_down.config(command=self.view_table_tree.xview)

        # Add First Column
        self.view_table_tree.column("#0", width=0, stretch=NO)

        # Add First Heading
        self.view_table_tree.heading("#0", text="", anchor=W)
        

        self.text_variable = StringVar()
        self.text_time_variable = StringVar()

        l = LabelFrame(self.view_table, text='Message')
        l.pack(fill="x", expand="yes", padx=20)
        Label(l, justify='left', textvariable=self.text_variable, height=2).grid(padx=10, row=0, column=0)
        Label(l, justify='center', textvariable=self.text_time_variable, height=2).grid(padx=50, row=0, column=1, columnspan=10)
        
        self.set_table_columns()
        self.view_table.protocol("WM_DELETE_WINDOW", self.view_on_delete)
        self.view_table.after(1, lambda: self.view_table.focus_force())
        self.view_table.mainloop()

    # Get the table columm
    def set_table_columns(self):
        # Connect to mysql
        if not self.sqlite:
            my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
            cursor = my_sql.cursor()
            cursor.execute(f'DESC `{self.table}`;')
            self.table_details = cursor.fetchall()
            self.columns = []
            for i in self.table_details:
                if i[3] == 'PRI':
                    self.primary_key.append(i[0])
                self.columns.append(i[0])
        else:
            my_sql = sqlite3.connect(self.database)
            cursor = my_sql.cursor()
            cursor.execute(f'PRAGMA table_info(`{self.table}`);')
            self.table_details = cursor.fetchall()
            self.columns = []
            for i in self.table_details:
                if i[5]:
                    self.primary_key.append(i[1])
                self.columns.append(i[1])

        self.primary_key_index = [self.columns.index(i) for i in self.primary_key]
        # Set the columns of the treeview
        self.view_table_tree['columns'] = tuple(self.columns)

        #Column sort func
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)

            # rearrange items in sorted positions
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            # reverse sort next time
            tv.heading(col, text=col, command=lambda _col=col: \
                        treeview_sort_column(tv, _col, not reverse))

        for i in self.columns:
            if i in self.primary_key:
                self.view_table_tree.column(i)
                self.view_table_tree.heading(i, text=i+'(PK)', anchor=CENTER)
            else:
                self.view_table_tree.column(i)
                self.view_table_tree.heading(i, text=i, anchor=CENTER,
                command=lambda _col=i : treeview_sort_column(self.view_table_tree, _col, False))
                

        self.add_item()
        if self.primary_key:
            self.view_table_tree.bind('<Double-1>', self.edit_fields)
        self.create_menu()
        my_sql.close()

    #Add Items
    def add_item(self):
        if not self.sqlite:
            my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
        else:
            my_sql = sqlite3.connect(self.database)
        cursor = my_sql.cursor()
        cursor.execute(f'SELECT * from `{self.table}`;')
        records = cursor.fetchall()
        count = 1
        for record in records:
            # print(record)
            if count % 2 != 0:
                self.view_table_tree.insert(parent='', index='end', iid=count, text='', values=record, tags=('evenrow',))
            else:
                self.view_table_tree.insert(parent='', index='end', iid=count, text='', values=record, tags=('oddrow',))
            # increment counter
            count += 1
        my_sql.close()
        self.text_variable.set(f">> Returned {len(records)} rows!")
        self.text_time_variable.set(f"Time: {datetime.now().strftime('%H:%M:%S')}")

    def refresh(self):
        for i in self.view_table_tree.get_children():
            self.view_table_tree.delete(i)
        # time.sleep(3)
        self.add_item()

    #Menu Bar
    def create_menu(self):
        
        self.my_menu = Menu(self.view_table)
        self.view_table.config(menu=self.my_menu)
        self.my_menu.add_command(label="See Tables", command=lambda: see_table())
        self.sql_menu = Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label='SQL', menu=self.sql_menu)
        self.my_menu.add_command(label='Refresh', command=lambda: self.refresh())
        if self.primary_key:
            self.sql_menu.add_command(label='Add Record', command=lambda: add_record())
            self.sql_menu.add_command(label='Delete Record', command=lambda: self.delete_record())
            self.sql_menu.add_command(label='Update Record', command=lambda: update_record())
        else:
            self.sql_menu.add_command(label='Add Record', command=lambda: add_record(), state='disabled')
            self.sql_menu.add_command(label='Delete Record', command=lambda: self.delete_record(), state='disabled')
            self.sql_menu.add_command(label='Update Record', command=lambda: update_record(), state='disabled')


        def update_record():
            selected = self.view_table_tree.selection()
            if selected:
                self.edit_fields()
            else:
                messagebox.showerror("WorkBench", "Select a record to update")
                self.view_table.after(1, lambda: self.view_table.focus_force())

        def add_record():
            self.refresh()
            self.edit_fields()

        def see_databases():
            self.view_on_delete()
            l.database.initiate(self.uname, self.passw)

        def see_table():
            self.view_on_delete()
            l.database.table.initiate(self.database, self.uname, self.passw, self.sqlite)

        def logout():
            self.view_on_delete()
            l.initiate()

    # Delete Record 
    def delete_record(self):
        selected = self.view_table_tree.selection()
        if selected:
            value = self.view_table_tree.item(selected, 'values')
            if messagebox.askokcancel('Workbench', 'Confirm Delete Record?'):
                if not self.sqlite:
                    my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
                else:
                    my_sql = sqlite3.connect(self.database)
                cursor = my_sql.cursor()
                statement = f'DELETE from `{self.table}` where {self.columns[0]} = \'{value[0]}\';'
                # print(statement)
                cursor.execute(statement)
                my_sql.commit()
                my_sql.close()
                self.refresh()
                self.text_variable.set(f">> Record Deleted Successfully!")
                self.text_time_variable.set(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        else:
            messagebox.showerror("Delete Record", "Please Select a row to delete")       

    # Edit Field
    def edit_fields(self, event=None):
        if not self.edit_boxs:
            self.edit_boxs = True
            self.edit = tix.Tk()

            self.edit.title('Workbench')
            self.edit.geometry('475x350')
            self.edit.resizable(height=False, width=False)

            self.second_frame = ScrollableFrame(self.edit, bg="#80c1ff")
            self.second_frame.pack(side=LEFT, expand=1, fill=BOTH, anchor=CENTER)
            
            self.label = Label(self.second_frame, font=5)
            self.label.grid(row=0, column=0, columnspan=20, pady=10)
            Label(self.second_frame,font=('italic', '10'), text='*Place Your Mouse Pointer Over the input Field,\nTo get Information about the Field').grid(row=1, column=0, columnspan=20,pady=5, padx=20)
            
            self.tip = tix.Balloon(self.edit)

            l1 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l2 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l3 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l4 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l5 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l6 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l7 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l8 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l9 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l10 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l11 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l12 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l13 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l14 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")
            l15 = Label(self.second_frame, font=5, justify=RIGHT, bg="#80c1ff")

            cl1 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl2 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl3 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl4 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl5 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl6 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl7 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl8 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl9 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl10 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl11 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl12 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl13 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl14 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
            cl15 = Label(self.second_frame, font=('bold', 15), text=':', height=1, bg="#80c1ff")
        
            e1 = Entry(self.second_frame, font=5)
            e2 = Entry(self.second_frame, font=5)
            e3 = Entry(self.second_frame, font=5)
            e4 = Entry(self.second_frame, font=5)
            e5 = Entry(self.second_frame, font=5)
            e6 = Entry(self.second_frame, font=5)
            e7 = Entry(self.second_frame, font=5)
            e8 = Entry(self.second_frame, font=5)
            e9 = Entry(self.second_frame, font=5)
            e10 = Entry(self.second_frame, font=5)
            e11 = Entry(self.second_frame, font=5)
            e12 = Entry(self.second_frame, font=5)
            e13 = Entry(self.second_frame, font=5)
            e14 = Entry(self.second_frame, font=5)
            e15 = Entry(self.second_frame, font=5)

            self.submit = Button(self.second_frame, text='  Save  ', font=10, command=self.update_data)
            self.submit.grid(row=len(self.columns)+2, columnspan=20, pady=10)

            self.labels = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15]
            self.entries = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15]
            self.clabels = [cl1, cl2, cl3, cl4, cl5, cl6, cl7, cl8, cl9, cl10, cl11, cl12, cl13, cl14, cl15]

            # for index, i in enumerate(labels):
            #     i.grid(row=index, column=0, padx=5, pady=5)
            
            # for index, i in enumerate(entries):
            #     i.grid(row=index, column=2 ,padx=5, pady=5)

            self.set_edit_fields()  
            self.edit.protocol("WM_DELETE_WINDOW", self.edit_on_delete)
            self.edit.bind_all('<Return>', self.update_data)
            self.edit.lift()
            self.edit.after(1, lambda: self.edit.focus_force())
            self.edit.mainloop()
        
        else:
            messagebox.showerror('Edit Box', 'Close the existing edit box to open another')

    def check_record(self):
        new_Values = []
        for index, i in enumerate(self.columns):
            e = self.entries[index]
            new_Values.append(e.get())
        new_val = [i for i in new_Values if i != '']
        old_value = [i for i in self.value if i != 'None']
        return new_val != old_value

    def set_edit_fields(self):
        selected = self.view_table_tree.focus()
        self.value = self.view_table_tree.item(selected, 'values')
        if not self.sqlite:
            date_time_fields = [index for index, i in enumerate(self.columns) if b'datetime' in self.table_details[index][1]]
        else:
            date_time_fields = [index for index, i in enumerate(self.columns) if 'DATETIME' in self.table_details[index][2]]

        length = max([len(x) for x in self.columns])
        # print(f'\'{self.value}\'')
        if selected:
            self.label.config(text='Update record')
            # print(self.table_details)
            for index, i in enumerate(self.columns):
                l,e,c = self.labels[index], self.entries[index], self.clabels[index]
                # print(i, self.table_details[index][2])
                if not self.sqlite:
                    if self.table_details[index][2] == 'NO':
                        l.config(text=i+'*')
                    else:
                        l.config(text=i)
                else:
                    if self.table_details[index][3]:
                        l.config(text=i+'*')
                    else:
                        l.config(text=i)
                if not self.value[index] == 'None':
                    e.insert(0, self.value[index])
                
                if index in self.primary_key_index:
                    e.config(state='disabled')

                if length > 20:
                    l.grid(row=index+2, column=0, padx=5, pady=5)
                elif 10 < length <= 20:
                    l.grid(row=index+2, column=0, padx=15, pady=5)
                else:
                    l.grid(row=index+2, column=0, padx=20, pady=5)
                c.grid(row=index+2, column=1)
                e.grid(row=index+2, column=2 ,padx=5, pady=5)
                
                if not self.sqlite:
                    if index in date_time_fields:
                        self.tip.bind_widget(e, msg=f"Type: {str(self.table_details[index][1]).replace('b', '')}\nDate-Time Format: \"YYYY-MM-DD HH:MM:SS\"\nLeave Blank To have Null Value")
                    else:
                        self.tip.bind_widget(e, msg=f"Type: {str(self.table_details[index][1]).replace('b', '')}\nLeave Blank To have Null Value")
                else:
                    if index in date_time_fields:
                        self.tip.bind_widget(e, msg=f"Type: {str(self.table_details[index][2])}\nDate-Time Format: \"YYYY-MM-DD HH:MM:SS\"\nLeave Blank To have Null Value")
                    else:
                        self.tip.bind_widget(e, msg=f"Type: {str(self.table_details[index][2])}\nLeave Blank To have Null Value")
                

        else:
            self.label.config(text='New Record')
            for index, i in enumerate(self.columns):
                l,e,c = self.labels[index], self.entries[index], self.clabels[index]
                if not self.sqlite:
                    if self.table_details[index][2] == 'NO':
                        l.config(text=i+'*')
                    else:
                        l.config(text=i)
                else:
                    if self.table_details[index][3]:
                        l.config(text=i+'*')
                    else:
                        l.config(text=i)

                if length > 20:
                    l.grid(row=index+2, column=0, padx=5, pady=5)
                elif 10 < length <= 20:
                    l.grid(row=index+2, column=0, padx=15, pady=5)
                else:
                    l.grid(row=index+2, column=0, padx=20, pady=5)
                c.grid(row=index+2, column=1)
                e.grid(row=index+2, column=2 ,padx=5, pady=5)
                if not self.sqlite:
                    if index in date_time_fields:
                        self.tip.bind_widget(e, msg=f"Type: {str(self.table_details[index][1]).replace('b', '')}\nDate-Time Format: \"YYYY-MM-DD HH:MM:SS\"\nLeave Blank To have Null Value")
                    else:
                        self.tip.bind_widget(e, msg=f"Type: {str(self.table_details[index][1]).replace('b', '')}\nLeave Blank To have Null Value")
                else:
                    if index in date_time_fields:
                        self.tip.bind_widget(e, msg=f"Type: {str(self.table_details[index][2])}\nDate-Time Format: \"YYYY-MM-DD HH:MM:SS\"\nLeave Blank To have Null Value")
                    else:
                        self.tip.bind_widget(e, msg=f"Type: {str(self.table_details[index][2])}\nLeave Blank To have Null Value")
                
    def edit_on_delete(self):
        changes = self.check_record()
        if not changes:
            self.edit.destroy()
            self.edit_boxs = False
            self.refresh()
        else:
            
            if messagebox.askyesno("Update Record", "Do you want to save changes?"):
                self.update_data()
                
            else:
                self.edit.destroy()
                self.edit_boxs = False
                self.refresh()
    
    def update_data(self, event=None):
        self.null = False
        self.sql_statement = ''
        self.new_Values = []
        for index, i in enumerate(self.columns):
            e = self.entries[index]
            self.new_Values.append(e.get())
        if self.value:
            if self.check_record():
                try:
                    if messagebox.askyesno("Update Record", "Confirm Update Record?"):
                        self.new_val,self.new_column_val_index = [i for i in self.new_Values if i != ''], [index for index, i in enumerate(self.new_Values) if i != '']
                        self.new_columns = [self.columns[index] for index, i in enumerate(self.new_Values) if i != '']
                        self.new_columns_statement = ''
                        for index, i in enumerate(self.new_val):
                            if not index == len(self.new_val) -1 :
                                self.new_columns_statement += f'{self.new_columns[index]},'
                                if not self.sqlite:
                                    if b'datetime' in self.table_details[self.new_column_val_index[index]][1]:
                                        self.sql_statement += f'\'{datetime.strptime(i, "%Y-%m-%d %H:%M:%S")}\', '
                                    else:
                                        self.sql_statement += f'\'{i}\', '
                                else:
                                    if 'DATETIME' in self.table_details[self.new_column_val_index[index]][2]:
                                        self.sql_statement += f'\'{datetime.strptime(i, "%Y-%m-%d %H:%M:%S.%f")}\', '
                                    else:
                                        self.sql_statement += f'\'{i}\', '

                            else:
                                self.new_columns_statement += f'{self.new_columns[index]}'
                                if not self.sqlite:
                                    if b'datetime' in self.table_details[self.new_column_val_index[index]][1]:
                                        self.sql_statement += f'\'{datetime.strptime(i, "%Y-%m-%d %H:%M:%S")}\''
                                    else:
                                        self.sql_statement += f'\'{i}\''
                                else:
                                    if 'DATETIME' in self.table_details[self.new_column_val_index[index]][2]:
                                        self.sql_statement += f'\'{datetime.strptime(i, "%Y-%m-%d %H:%M:%S")}\''
                                    else:
                                        self.sql_statement += f'\'{i}\''
                        if not self.sqlite:
                            my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
                        else:
                            my_sql = sqlite3.connect(self.database)
                        cursor = my_sql.cursor()
                        if not self.sqlite:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
                        
                        my_sql.commit()
                        statement = f'DELETE from `{self.table}` where {self.columns[0]} = \'{self.value[0]}\';'
                        # print(statement)
                        cursor.execute(statement)
                        my_sql.commit()
                        my_sql.close()
                        # print(self.new_column_val, self.new_column_val_index, self.new_columns)
                        if not self.sqlite:
                            my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
                        else:
                            my_sql = sqlite3.connect(self.database)
                        cursor = my_sql.cursor()
                        statement = f'INSERT INTO `{self.table}` ({self.new_columns_statement}) VALUES({self.sql_statement});'
                        # print(statement)
                        cursor.execute(statement)
                        if not self.sqlite:
                            cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
                        my_sql.commit()
                        my_sql.close()
                        self.edit.destroy()
                        self.edit_boxs = False
                        self.refresh()
                        self.text_variable.set(f">> UPDATED Successfully")
                        self.text_time_variable.set(f"Time: {datetime.now().strftime('%H:%M:%S')}")
                    else:
                        self.edit.after(1, lambda: self.edit.focus_force())
                except ValueError as e:
                    if 'does not match format' in str(e):
                        messagebox.showerror("WorkBench", str(e).replace('%Y-%m-%d %H:%M:%S', 'YYYY-MM-DD HH:MM:SS'))
                        self.edit.after(1, lambda: self.edit.focus_force())
                except Exception as e:
                    print(e)
            else:
                messagebox.showinfo("WorkBench", "No Changes Dectected!!")
                self.edit.after(1, lambda: self.edit.focus_force())
        else:
            if messagebox.askyesno("WorkBench", "Confirm Add Record?"):
                self.new_val,self.new_column_val_index = [i for i in self.new_Values if i != ''], [index for index, i in enumerate(self.new_Values) if i != '']
                self.new_columns = [self.columns[index] for index, i in enumerate(self.new_Values) if i != '']
                # print(self.new_column_val, self.new_column_val_index, self.new_columns)
                self.new_columns_statement = ''
                for index, i in enumerate(self.new_val):
                    if not index == len(self.new_val) -1 :
                        self.new_columns_statement += f'{self.new_columns[index]},'
                        if not self.sqlite:
                            if b'datetime' in self.table_details[self.new_column_val_index[index]][1]:
                                self.sql_statement += f'\'{datetime.strptime(i, "%Y-%m-%d %H:%M:%S")}\', '
                            else:
                                self.sql_statement += f'\'{i}\', '
                        else:
                            if 'DATETIME' in self.table_details[self.new_column_val_index[index]][2]:
                                self.sql_statement += f'\'{datetime.strptime(i, "%Y-%m-%d %H:%M:%S")}\', '
                            else:
                                self.sql_statement += f'\'{i}\', '
                    else:
                        self.new_columns_statement += f'{self.new_columns[index]}'
                        if not self.sqlite:
                            if b'datetime' in self.table_details[self.new_column_val_index[index]][1]:
                                self.sql_statement += f'\'{datetime.strptime(i, "%Y-%m-%d %H:%M:%S")}\''
                            else:
                                self.sql_statement += f'\'{i}\''
                        else:
                            if 'DATETIME' in self.table_details[self.new_column_val_index[index]][2]:
                                self.sql_statement += f'\'{datetime.strptime(i, "%Y-%m-%d %H:%M:%S")}\''
                            else:
                                self.sql_statement += f'\'{i}\''
                try:
                    if not self.sqlite:
                        my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
                    else:
                        my_sql = sqlite3.connect(self.database)
                    cursor = my_sql.cursor()
                    statement = f'INSERT INTO `{self.table}` ({self.new_columns_statement}) VALUES({self.sql_statement});'
                    cursor.execute(statement)
                    my_sql.commit()
                    my_sql.close()
                    self.edit.destroy()
                    self.edit_boxs = False
                    self.refresh()
                    self.text_variable.set(f">> New Record Added Successfully!")
                    self.text_time_variable.set(f"Time: {datetime.now().strftime('%H:%M:%S')}")
                except mysql.connector.errors.IntegrityError as e:
                    messagebox.showerror('Integrity Error', str(e).replace('1062 (23000):', ''))
                    self.edit.after(1, lambda: self.edit.focus_force())
                except mysql.connector.errors.DatabaseError as e:
                    messagebox.showerror("WorkBench", str(e).replace('1364 (HY000):', ''))
                    self.edit.after(1, lambda: self.edit.focus_force())

    def view_on_delete(self, event=None):
        try:
            self.edit_on_delete()
        except TclError:
            pass
        except AttributeError:
            pass
        self.view_table.destroy()
        

class Alter_Table:
    def __init__(self) -> None:
        pass

    def initiate(self, database, table, uname=None, passw=None, sqlite=False):
        self.row_num = -1
        self.drop_col_index, self.new_col_index = [], []
        self.database = database
        self.table = table
        self.uname = uname
        self.passw = passw
        self.sqlite = sqlite

        self.alter_table = tix.Tk()
        self.alter_table.resizable(height=False, width=False)
        self.alter_table.title(f"Alter Table '{table}'")
        self.alter_table.geometry("570x410")

        main_frame = Frame(self.alter_table)
        main_frame.pack(expand=1, fill='both', anchor=CENTER)

        frame = Frame(main_frame)
        frame.place(relx=0.001, rely=0.01, relwidth=1)

        first_frame = Frame(frame)
        first_frame.pack(padx=10, fill=X)

        Label(first_frame, text='Alter Table', font=10).grid(padx=10, row=0, columnspan=10)

        table_name_frame = Frame(first_frame)
        table_name_frame.grid(row=1, columnspan=10)
        Label(table_name_frame, text='Table Name :', font=10).grid(row=0, column=0, padx=20)

        self.table_name_entry = Entry(table_name_frame, font=10, width=15)
        self.table_name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.table_name_entry.insert(0, self.table)

        Label(first_frame, text='Column Name', font=10).grid(row=2, column=0, padx=20, pady=5)
        Label(first_frame, text='Data Type', font=10).grid(row=2, column=1, padx=25, pady=5)
        pk = Label(first_frame, text='PK', font=10)
        pk.grid(row=2, column=2, padx=15, pady=5)
        uq = Label(first_frame, text='UQ', font=10)
        uq.grid(row=2, column=3, padx=10, pady=5)
        nn = Label(first_frame, text='NN', font=10)
        nn.grid(row=2, column=4, padx=10, pady=5)
        ai = Label(first_frame, text='AI', font=10)
        ai.grid(row=2, column=5, padx=12, pady=5)

        self.tip = tix.Balloon(self.alter_table)

        self.tip.bind_widget(pk, msg='Primary Key')
        self.tip.bind_widget(uq, msg='Unique Index')
        self.tip.bind_widget(nn, msg='Not Null')
        self.tip.bind_widget(ai, msg='Auto Increment')

        self.second_frame = ScrollableFrame(frame, vscroll=True)
        self.second_frame.pack(side=LEFT, fill=BOTH, expand=1, anchor=CENTER)

        self.add_but = Button(main_frame, text='Add Next Row', font=10, command=self.add_row)
        self.add_but.place(relx=0.19, rely=0.9)

        self.revert_but = Button(main_frame, text='Revert', font=20, command=self.revert)
        self.revert_but.place(relx=0.45, rely=0.9)

        self.submit_but = Button(main_frame, text='Submit', font=10, command=self.submit)
        self.submit_but.place(relx=0.6, rely=0.9)

        self.minus_but = Button(self.second_frame, text='- Row', font=('bold', 12), command=self.minus_row)
        self.alter_table.protocol("WM_DELETE_WINDOW", self.alter_table_on_close)
        self.alter_table.after(1, lambda: self.alter_table.focus_force())

        self.alter_table_menu()
        self.create_rows()
        self.set_rows()
        
        self.alter_table.mainloop()

    def alter_table_menu(self):
        my_menu = Menu(self.alter_table)
        self.alter_table.config(menu=my_menu)
        my_menu.add_command(label='Exit', command=self.alter_table_on_close)
    
    def create_rows(self):
        
        types = ['Select', 'INT', 'VARCHAR(30)', 'VARCHAR(50)', 'VARCHAR(100)', 'DATETIME', 'DECIMAL', 'FLOAT', 'Others']
        
        cl_nm_1, dty_1, pk_1, uq_1, nn_1, ai_1 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_2, dty_2, pk_2, uq_2, nn_2, ai_2 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_3, dty_3, pk_3, uq_3, nn_3, ai_3 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_4, dty_4, pk_4, uq_4, nn_4, ai_4 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_5, dty_5, pk_5, uq_5, nn_5, ai_5 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_6, dty_6, pk_6, uq_6, nn_6, ai_6 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_7, dty_7, pk_7, uq_7, nn_7, ai_7 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_8, dty_8, pk_8, uq_8, nn_8, ai_8 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_9, dty_9, pk_9, uq_9, nn_9, ai_9 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_10, dty_10, pk_10, uq_10, nn_10, ai_10 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_11, dty_11, pk_11, uq_11, nn_11, ai_11 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_12, dty_12, pk_12, uq_12, nn_12, ai_12 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_13, dty_13, pk_13, uq_13, nn_13, ai_13 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_14, dty_14, pk_14, uq_14, nn_14, ai_14 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)
        cl_nm_15, dty_15, pk_15, uq_15, nn_15, ai_15 = Entry(self.second_frame, width=13, font=10), ttk.Combobox(self.second_frame, width=13, state='readonly', values=types), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame), ttk.Checkbutton(self.second_frame)

        self.column_names = [cl_nm_1, cl_nm_2, cl_nm_3, cl_nm_4, cl_nm_5, cl_nm_6, cl_nm_7, cl_nm_8, cl_nm_9, cl_nm_10, cl_nm_11, cl_nm_12, cl_nm_13, cl_nm_14, cl_nm_15]
        self.datatypes = [dty_1, dty_2, dty_3, dty_4, dty_5, dty_6, dty_7, dty_8, dty_9, dty_10, dty_11, dty_12, dty_13, dty_14, dty_15]
        self.pks = [pk_1, pk_2, pk_3, pk_4, pk_5, pk_6, pk_7, pk_8, pk_9, pk_10, pk_11, pk_12, pk_13, pk_14, pk_15]
        self.uqs = [uq_1, uq_2, uq_3, uq_4, uq_5, uq_6, uq_7, uq_8, uq_9, uq_10, uq_11, uq_12, uq_13, uq_14, uq_15]
        self.nns = [nn_1, nn_2, nn_3, nn_4, nn_5, nn_6, nn_7, nn_8, nn_9, nn_10, nn_11, nn_12, nn_13, nn_14, nn_15]
        self.ais = [ai_1, ai_2, ai_3, ai_4, ai_5, ai_6, ai_7, ai_8, ai_9, ai_10, ai_11, ai_12, ai_13, ai_14, ai_15]

    #Event handler for combobox
    def event_combobox(self, ai, cb, rn):
        types = ['INT', 'VARCHAR(30)', 'VARCHAR(50)', 'VARCHAR(100)', 'DATETIME', 'DECIMAL', 'FLOAT', 'Others']
        if cb['values'][0] == 'Select':
            cb['values'] = types
        
        if cb.get() == 'Others':
            inputdialog = MyDialog(self.alter_table, 'Enter the datatype')
            self.alter_table.wait_window(inputdialog.top)
            cb['values'] = [inputdialog.input] + types
            cb.current(0)
        
        if str(cb.get()).upper() == 'INT' and rn == 0:
            ai.configure(state=NORMAL)
        else:
            if 'selected' in ai.state():
                ai.invoke()
            ai.configure(state=DISABLED)
    
    #Add Row Funtion
    def add_row(self):
        def auto_invoke_nn(row_num):

            if 'selected' in self.pks[row_num].state():
                if 'selected' not in self.nns[row_num].state():
                    self.nns[row_num].invoke()
        self.row_num += 1
        self.column_names[self.row_num].grid(row=self.row_num, column=0, pady=5, padx=20)

        self.datatypes[self.row_num].current(0)
        self.datatypes[self.row_num].grid(row=self.row_num, column=1, padx=12)
        self.datatypes[self.row_num].bind("<<ComboboxSelected>>", lambda event, ai=self.ais[self.row_num], cb=self.datatypes[self.row_num], rn=self.row_num: self.event_combobox(ai, cb, rn))

        self.pks[self.row_num].grid(row=self.row_num, column=2, padx=13)
        self.pks[self.row_num].invoke()
        self.pks[self.row_num].invoke()
        self.pks[self.row_num].config(command=lambda row_num = self.row_num: auto_invoke_nn(row_num))


        self.uqs[self.row_num].grid(row=self.row_num, column=3, padx=15)
        self.uqs[self.row_num].invoke()
        self.uqs[self.row_num].invoke()

        self.nns[self.row_num].grid(row=self.row_num, column=4, padx=15)
        self.nns[self.row_num].invoke()
        self.nns[self.row_num].invoke()

        self.ais[self.row_num].grid(row=self.row_num, column=5, padx=13)
        self.ais[self.row_num].invoke()
        self.ais[self.row_num].invoke()
        self.ais[self.row_num].configure(state=DISABLED)
        self.new_col_index.append(self.row_num)
        if self.row_num > 0:
            self.minus_but.grid(row=self.row_num, column=6)

        if self.row_num > 13:
            self.add_but.config(state='disabled')
        else:
            self.add_but.config(state='normal')

    def set_rows(self):
        types = ['INT', 'VARCHAR(30)', 'VARCHAR(50)', 'VARCHAR(100)', 'DATETIME', 'DECIMAL', 'FLOAT', 'Others']
        # Connect to mysql
        if not self.sqlite:
            my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
            cursor = my_sql.cursor()
            cursor.execute(f'DESC `{self.table}`;')
            self.table_details = cursor.fetchall()
            self.columns, self.types, self.notnull, self.p_key, self.auto, self.unique, self.unique_constraint = [], [], [], [], [], [], {}
            # print(self.table_details)
            cursor.execute(f'SHOW INDEX FROM {self.table};')
            unique_constraint = cursor.fetchall()
            for i in unique_constraint:
                if 'PRIMARY' not in i[2]:
                    self.unique_constraint[i[4]] = i[2]
                    
            for i in self.table_details:
                self.columns.append(i[0])
                _type = str(i[1]).replace('b','').replace("'", "").upper()
                self.types.append(types.index(_type) if _type in types else _type)
                self.notnull.append(True if 'NO' in i[2] else False)
                self.p_key.append(True if 'PRI' in i[3] else False)
                self.auto.append(True if 'auto_increment' in i[5] else False)
                self.unique.append(True if i[0] in self.unique_constraint else False)
                

        else:
            my_sql = sqlite3.connect(self.database)
            cursor = my_sql.cursor()
            cursor.execute(f'PRAGMA table_info(`{self.table}`);')
            self.table_details = cursor.fetchall()
            self.columns, self.types, self.null, self.key, self.auto = [], [], [], [], []
            
            for i in self.table_details:
                self.columns.append(i[1])
                # print(i)

        for i in self.columns:
            self.add_row()
            self.column_names[self.row_num].insert(0, i)
            if isinstance(self.types[self.row_num], int):
                self.datatypes[self.row_num]['values'] = types
                self.datatypes[self.row_num].current(self.types[self.row_num])

            else:
                new_type = [self.types[self.row_num]] + types
                self.datatypes[self.row_num]['values'] = new_type
                self.datatypes[self.row_num].current(0)
            if self.types[self.row_num] == 0 and self.row_num == 0:
                self.ais[self.row_num].configure(state=NORMAL)
            if self.notnull[self.row_num]:
                self.nns[self.row_num].invoke()
            if self.p_key[self.row_num]:
                self.pks[self.row_num].invoke()
            if self.auto[self.row_num]:
                self.ais[self.row_num].invoke()
            if self.unique[self.row_num]:
                self.uqs[self.row_num].invoke()
        
        self.new_col_index = []
            
    #Minus Row Function
    def minus_row(self):
        types = ['Select', 'INT', 'VARCHAR(30)', 'VARCHAR(50)', 'VARCHAR(100)', 'DATETIME', 'DECIMAL', 'FLOAT', 'Others']

        if self.column_names[self.row_num].get() != '':
            if messagebox.askokcancel('Workbench', 'Removing row will also delete the data in it'):
                self.column_names[self.row_num].delete(0, END)
            else:
                return
        self.column_names[self.row_num].grid_forget()

        self.datatypes[self.row_num].grid_forget()
        self.datatypes[self.row_num]['values'] = types
        self.datatypes[self.row_num].current(0)

        self.pks[self.row_num].grid_forget()
        self.pks[self.row_num].config(command=lambda:None)
        self.pks[self.row_num].state(['!selected'])

        self.uqs[self.row_num].grid_forget()
        self.uqs[self.row_num].state(['!selected'])

        self.nns[self.row_num].grid_forget()
        self.nns[self.row_num].state(['!selected'])

        self.ais[self.row_num].grid_forget()
        self.ais[self.row_num].state(['!selected'])
        self.drop_col_index.append(self.row_num)
        self.row_num -= 1
        if self.row_num > 0:
            self.minus_but.grid(row=self.row_num, column=6)
        else:
            self.minus_but.grid_forget()
        if self.row_num > 13:
            self.add_but.config(state='disabled')
        else:
            self.add_but.config(state='normal')
 
    def check_changes(self):
        base_types = ['INT', 'VARCHAR(30)', 'VARCHAR(50)', 'VARCHAR(100)', 'DATETIME', 'DECIMAL', 'FLOAT', 'Others']
        table_name = self.table_name_entry.get()
        if table_name != '':
            if table_name.lower() != 'table':
                columns, types, notnull, p_key, auto, unique = [], [], [], [], [], []
                for i in range(self.row_num + 1):
                    if self.column_names[i].get() != '':
                        if self.column_names[i].get().lower() != 'column': 
                            if self.datatypes[i].get() != 'Select':
                                columns.append(self.column_names[i].get())
                                _type = self.datatypes[i].get()
                                types.append(base_types.index(_type) if _type in base_types else _type)
                                p_key.append(True if 'selected' in self.pks[i].state() else False)
                                unique.append(True if 'selected' in self.uqs[i].state() else False)
                                auto.append(True if 'selected' in self.ais[i].state() else False)
                                notnull.append(True if 'selected' in self.nns[i].state() else False)
                            else:
                                messagebox.showerror('WorkBench', 'Cant Submit,\nPlease Select one datatype.')
                                self.alter_table.after(1, lambda: self.alter_table.focus_force())
                                self.datatypes[i].focus()
                                return
                        else:
                            messagebox.showerror('WorkBench', f'Column Name cannot be {self.column_names[i].get()}')
                            self.alter_table.after(1, lambda: self.alter_table.focus_force())
                            self.column_names[i].focus()
                            return
                    else:
                        messagebox.showerror('WorkBench', 'Cant Submit,\nColumn name can\'t be empty.')
                        self.alter_table.after(1, lambda: self.alter_table.focus_force())
                        self.column_names[i].focus()
                        return
                
                check_list = [columns == self.columns, types == self.types, notnull == self.notnull, self.p_key == p_key, unique == self.unique, self.auto == auto]
                
                if (not all(check_list)) or self.table != self.table_name_entry.get():
                    alter_statement, changed_index = f'ALTER TABLE `{self.table}` ', []
                    
                    if not check_list[0]:
                        change_col_statement = ''
                        for index, i in enumerate(columns):
                            if index < len(self.columns) and index not in self.drop_col_index:
                                if i != self.columns[index]:
                                    changed_index.append(index)

                        for index, i in enumerate(changed_index):
                            t = base_types[types[i]] if isinstance(types[i], int) else types[i]
                            nn = 'NOT NULL' if notnull[i] else 'NULL'
                            ai = ' AUTO_INCREMENT' if auto[i] else ''
                            u = ' UNIQUE' if unique[i] else ''
                            c = ',' if ((index + 1) != len(changed_index)) or (len(self.new_col_index) > 0) or (len(self.drop_col_index) > 0) else ''
                            change_col_statement += f"CHANGE COLUMN `{self.columns[i]}` `{columns[i]}` {t} {nn}{u}{ai}{c}"
                        
                        for index, i in enumerate(self.drop_col_index):
                            u = f'DROP INDEX `{self.unique_constraint[self.columns[i]]}`,' if self.unique[i] else ''
                            c = ',' if ((index + 1) != len(self.drop_col_index)) or (len(self.new_col_index) > 0) else ''
                            change_col_statement += f"{u} DROP COLUMN `{self.columns[i]}`{c}"
                        
                        for index, i in enumerate(self.new_col_index):
                            t = base_types[types[i]] if isinstance(types[i], int) else types[i]
                            nn = 'NOT NULL' if notnull[i] else 'NULL'
                            u = ' UNIQUE' if unique[i] else ''
                            ai = ' AUTO_INCREMENT' if auto[i] else ''
                            # print(index, index +1 , len(new_col_index)
                            c = ',' if ((index + 1) != len(self.new_col_index)) else ''
                            change_col_statement += f"ADD COLUMN `{columns[i]}` {t} {nn}{u}{ai}{c}"
                        
                        # print('col',change_col_statement)
                        alter_statement += change_col_statement

                    if not check_list[1]:
                        types_index = []
                        for index, i in enumerate(types):
                            if index < len(self.types):
                                if i != self.types[index] and index not in changed_index and index not in self.new_col_index:
                                    changed_index.append(index)
                                    types_index.append(index)
                        
                        changed_types_statement = ', ' if (len(types_index) > 0) and not all(check_list[:1]) else ''
                        
                        for index, i in enumerate(types_index):
                            t = base_types[types[i]] if isinstance(types[i], int) else types[i]
                            nn = 'NOT NULL' if notnull[i] else 'NULL'
                            c = ', ' if (index + 1) != len(types_index) else ''
                            u = ' UNIQUE' if unique[i] else ''
                            ai = ' AUTO_INCREMENT' if auto[i] else ''
                            changed_types_statement += f"CHANGE COLUMN `{columns[i]}` `{columns[i]}` {t} {nn}{u}{ai}{c}"

                        # print('type',changed_types_statement)
                        alter_statement += changed_types_statement

                    if not check_list[2]:
                        notnull_index = []
                        for index, i in enumerate(notnull):
                            if index < len(self.notnull):
                                if i != self.notnull[index] and index not in changed_index and index not in self.new_col_index:
                                    changed_index.append(index)
                                    notnull_index.append(index)
                        
                        changed_not_null_statement = ', ' if len(notnull_index) > 0 and not all(check_list[:2]) else ''
                        
                        for index, i in enumerate(notnull_index):
                            t = base_types[types[i]] if isinstance(types[i], int) else types[i]
                            nn = 'NOT NULL' if notnull[i] else 'NULL'
                            c = ', ' if (index + 1) != len(notnull_index) else ''
                            u = ' UNIQUE' if unique[i] else ''
                            ai = ' AUTO_INCREMENT' if auto[i] else ''
                            changed_not_null_statement += f"CHANGE COLUMN `{columns[i]}` `{columns[i]}` {t} {nn}{u}{ai}{c}"
                        
                        # print('notnull',changed_not_null_statement)
                        alter_statement += changed_not_null_statement

                    if not check_list[3]:
                        change_p_key_statement = f"{',' if not all(check_list[:3]) else ''}DROP PRIMARY KEY, ADD PRIMARY KEY ("
                        change_p_key_index = []
                        
                        for index, i in enumerate(p_key):
                            if i:
                                change_p_key_index.append(index)
                        for index, i in enumerate(change_p_key_index):
                            c = ', ' if (index + 1) != len(change_p_key_index) else ''
                            change_p_key_statement += f"`{columns[i]}`{c}"

                        alter_statement += change_p_key_statement + ')'
                    
                    if not check_list[4]:
                        unique_index = []
                        for index, i in enumerate(unique):
                            if index < len(self.unique):
                                if i != self.unique[index]:
                                    unique_index.append(index)
                        
                        changed_unique_statement = ''
                        
                        for index, i in enumerate(unique_index):

                            if unique[i] and i not in changed_index and i not in self.new_col_index:
                                t = base_types[types[i]] if isinstance(types[i], int) else types[i]
                                nn = 'NOT NULL' if notnull[i] else 'NULL'
                                u = ' UNIQUE' if unique[i] else ''
                                ai = ' AUTO_INCREMENT' if auto[i] else ''
                                c = ', ' if (index + 1) != len(unique_index) else ''
                                changed_unique_statement += f"{',' if not all(check_list[:4]) else ''} CHANGE COLUMN `{columns[i]}` `{columns[i]}` {t} {nn}{u}{ai}{c}"
                            elif not unique[i]:
                                c = ', ' if (index + 1) != len(unique_index) else ''
                                changed_unique_statement += f"{',' if not all(check_list[:4]) else ''} DROP INDEX `{self.unique_constraint[self.columns[i]]}`{c}"

                            if i not in changed_index:
                                changed_index.append(i)

                        # print('unique',changed_unique_statement)
                        alter_statement += changed_unique_statement

                    if not check_list[5]:
                        auto_index = []
                        for index, i in enumerate(auto):
                            if index < len(self.auto):
                                if i != self.auto[index] and index not in changed_index and index not in self.new_col_index:
                                    changed_index.append(index)
                                    auto_index.append(index)

                        changed_auto_statement = ', ' if len(auto_index) > 0 and not all(check_list[:5]) else ''

                        for index, i in enumerate(auto_index):
                            t = base_types[types[i]] if isinstance(types[i], int) else types[i]
                            nn = 'NOT NULL' if notnull[i] else 'NULL'
                            u = ' UNIQUE' if unique[i] else ''
                            ai = ' AUTO_INCREMENT' if auto[i] else ''
                            c = ', ' if (index + 1) != len(auto_index) else ''
                            changed_auto_statement += f"CHANGE COLUMN `{columns[i]}` `{columns[i]}` {t} {nn}{u}{ai}{c}"
                            
                        # print('ai',changed_auto_statement)
                        alter_statement += changed_auto_statement


                    if self.table != self.table_name_entry.get():
                        c = ', ' if not all(check_list) else ''
                        alter_statement += f"{c}RENAME TO `{self.table_name_entry.get()}`"
                    
                    return alter_statement + ';'
                else:
                    messagebox.showerror('Workbench', 'No changes detected !')
                    self.alter_table.after(1, lambda: self.alter_table.focus())
            else:
                messagebox.showerror('WorkBench', f'Table Name cannot be {table_name}')
                self.alter_table.after(1, lambda: self.alter_table.focus_force())
                self.table_name_entry.focus()
        else:
            messagebox.showerror('WorkBench', 'Table Name is compulsory')
            self.alter_table.after(1, lambda: self.alter_table.focus_force())
            self.table_name_entry.focus()

    def revert(self):
        types = ['Select', 'INT', 'VARCHAR(30)', 'VARCHAR(50)', 'VARCHAR(100)', 'DATETIME', 'DECIMAL', 'FLOAT', 'Others']

        for i in range(self.row_num +1):
            self.column_names[i].delete(0, END)
            self.column_names[i].grid_forget()

            self.datatypes[i].grid_forget()
            self.datatypes[i]['values'] = types
            self.datatypes[i].current(0)

            self.pks[i].grid_forget()
            self.pks[i].config(command=lambda:None)
            self.pks[i].state(['!selected'])

            self.uqs[i].grid_forget()
            self.uqs[i].state(['!selected'])

            self.nns[i].grid_forget()
            self.nns[i].state(['!selected'])

            self.ais[i].grid_forget()
            self.ais[i].state(['!selected'])
            self.drop_col_index.append(i)
            self.minus_but.grid_forget()
        self.row_num = -1
        self.drop_col_index = []
        self.set_rows()
                
    def submit(self):
        _return = self.check_changes()
        if _return:
            print(_return)
            if not self.sqlite:
                my_sql = mysql.connector.connect(host='localhost', user=self.uname, passwd=self.passw, database=self.database)
            else:
                my_sql = sqlite3(self.database)
            cursor = my_sql.cursor()
            if messagebox.askokcancel('WorkBench', f'Apply Changes with statement:\n\n{_return}'):
                try:
                    cursor.execute(_return)
                    my_sql.commit()
                    messagebox.showinfo('WorkBench', 'Successfully Changed')
                    self.alter_table_on_close()
                except Exception as e:
                    messagebox.showerror('WorkBench', str(e))
                    self.alter_table.after(1, lambda:self.alter_table.focus_force())
            else:
                self.alter_table.after(1, lambda:self.alter_table.focus_force())

    def alter_table_on_close(self, event=None):
        self.alter_table.destroy()
        l.database.table.initiate(self.database, self.uname, self.passw, self.sqlite)

    
l = Login()
b = Base()
t = Alter_Table()
# b.table.view.initiate('users', 'users')
# b.initiate('root', 'vishal@sql@123')
# t.initiate('virtual_users','table_2345', 'root', 'vishal@sql@123')
l.initiate()
