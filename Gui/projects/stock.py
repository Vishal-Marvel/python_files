from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import requests
import socket
import smtplib
import datetime, time
from bs4 import BeautifulSoup
import os
import pickle

root = Tk()
root.title('Stocks')
root.geometry('400x400')

frame = Frame(root, bg="#80c1ff", bd=7)
frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

title = Label(frame, bg="light green", font=('bold', 15), text='STOCKS')
title.place(relwidth=1, relheight=0.12)
lis = []
com = []
price = []
urls = []
mail = ''


def save_mail():
    global mail
    if email.get():
        mail = email.get()
        send_mail(lis, mail)
    else:
        messagebox.showerror('Mail Function', 'Mail box is empty')


my_tree = ttk.Treeview()
entry_box = Entry(frame, bd=1, relief='groove', font=('Ariel', 15))
search = Button(frame, text='search', font=('Ariel', 15), command=lambda: searcher(entry_box.get()))
confirm = Button(frame, text='mail', font=('Ariel', 15), command=save_mail)
email = Entry(frame, bd=1, relief='groove', font=('Ariel', 15))


def save():
    global mail
    f_name = filedialog.asksaveasfilename(title='Save', initialdir='F:/vishal/python files/PycharmProjects/stock_data',
                                          defaultextension='.dat')
    if f_name:
        file = open(f_name, 'wb')
        lis.append(mail)
        pickle.dump(lis, file)
    content = str(
        len(os.listdir(path='F:/vishal/python files/PycharmProjects/stock_data'))) + ' Stock Data Set Available'
    status_bar.config(text=content)
    send_mail(lis[:-1], lis[-1])


def opener():
    global lis, entry_box, search, email, confirm, mail
    f_name = filedialog.askopenfilename(title='Open', initialdir='F:/vishal/python files/PycharmProjects/stock_data')
    if f_name and f_name.endswith('.dat'):
        input_file = open(f_name, 'rb')
        lis = pickle.load(input_file)
    mail = lis[-1]
    entry_box.place(relx=0.08, rely=0.18, relheight=0.1, relwidth=0.68)
    search.place(relx=0.8, rely=0.18, relwidth=0.18, relheight=0.1)
    email.place(relx=0.08, rely=0.82, relheigh=0.1, relwidth=0.7)
    confirm.place(relx=0.8, rely=0.82, relwidth=0.18, relheight=0.1)
    email.insert(0, mail)
    clear_and_create()
    count = 0
    for i in lis[:-1]:
        c, p = Price(i)
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=i, text="",
                           values=(count + 1, c, p),
                           tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=i, text="",
                           values=(count + 1, c, p),
                           tags=('oddrow',))
        count += 1

    def OnDoubleClick(event):
        item = my_tree.focus()
        show_details(item)

    my_tree.bind("<Double-1>", OnDoubleClick)


def clear_and_create():
    global my_label, add_but, view_but
    my_label.place_forget()
    add_but.place_forget()
    view_but.place_forget()

    style = ttk.Style()

    # style.theme_use("default")

    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="white")

    style.map('Treeview',
              background=[('selected', 'blue')])

    tree_frame = Frame(frame, bg="black", bd=1)
    tree_frame.place(relx=0.08, rely=0.32, relwidth=0.85, relheight=0.48)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    global my_tree
    my_tree = ttk.Treeview(tree_frame, style="Treeview", yscrollcommand=tree_scroll.set, selectmode='browse')
    my_tree.pack(fill=X)

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ("SNo", "Name", "Stock Price")

    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("SNo", anchor=CENTER, width=40, minwidth=40)
    my_tree.column("Name", anchor=CENTER, width=150, minwidth=150)
    my_tree.column("Stock Price", anchor=CENTER, width=75, minwidth=75)

    my_tree.tag_configure("oddrow", background="white")
    my_tree.tag_configure("evenrow", background="lightblue")

    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("SNo", text="S.No.", anchor=CENTER)
    my_tree.heading("Name", text="Name", anchor=CENTER)
    my_tree.heading("Stock Price", text="Price", anchor=CENTER)

    my_tree.tag_configure("oddrow", background="white")
    my_tree.tag_configure("evenrow", background="lightblue")


def show_details(item):
    root_1 = Tk()
    c, _ = Price(item)
    root_1.title(c)
    root_1.geometry('300x300')
    frame = Frame(root_1, bg="#80c1ff")
    frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')
    link = 'https://finance.yahoo.com/quote/{}?p={}'.format(item, item)
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    details = {}
    details['name'] = soup.find('h1', {'data-reactid': '7'}).text
    details['price'] = soup.find('span', {'data-reactid': '32'}).text
    details['other price details'] = soup.find('span', {'data-reactid': '33'}).text
    details['close time'] = soup.find('div', {
        'class': 'C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm'}).find('span').text
    details['prev close'] = soup.find('span', {'data-reactid': '44'}).text
    details['open'] = soup.find('span', {'data-reactid': '49'}).text
    for i in details:
        print(i, details[i])
    root_1.mainloop()


def searcher(name):
    global my_tree
    r = requests.get('https://finance.yahoo.com/lookup?s=' + str(name).upper())
    s = BeautifulSoup(r.text, 'lxml')
    id = s.find_all('td', {'class': 'data-col0 Ta(start) Pstart(6px) Pend(15px)'})
    c_name = s.find_all('td', {'class': 'data-col1 Ta(start) Pstart(10px) Miw(80px)'})
    price = s.find_all('td', {'class': 'data-col2 Ta(end) Pstart(20px) Pend(15px)'})

    count = 0
    for i in my_tree.get_children():
        my_tree.delete(i)
    for index, i in enumerate(c_name):
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=id[index].text, text="",
                           values=(count + 1, i.text, price[index].text),
                           tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=id[index].text, text="",
                           values=(count + 1, i.text, price[index].text),
                           tags=('oddrow',))
        count += 1

    def OnDoubleClick(event):
        item = my_tree.focus()
        lis.append(item)
        adder()

    my_tree.bind("<Double-1>", OnDoubleClick)


def adder():
    global my_tree, lis, entry_box
    entry_box.delete(0, END)
    for i in my_tree.get_children():
        my_tree.delete(i)
    count = 0
    for i in lis:
        c, p = Price(i)
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=i, text="",
                           values=(count + 1, c, p),
                           tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=i, text="",
                           values=(count + 1, c, p),
                           tags=('oddrow',))
        count += 1

    def OnDoubleClick(event):
        item = my_tree.focus()
        show_details(item)

    my_tree.bind("<Double-1>", OnDoubleClick)


def add():
    global my_tree, lis, entry_box, search, email, confirm, mail
    lis, mail = [], ''

    entry_box.place(relx=0.08, rely=0.18, relheight=0.1, relwidth=0.68)

    search.place(relx=0.8, rely=0.18, relwidth=0.18, relheight=0.1)
    search.bind_all("<Return>", lambda e: searcher(entry_box.get()))

    text = Label(frame, text='mail id')

    email.place(relx=0.08, rely=0.82, relheigh=0.1, relwidth=0.7)

    confirm.place(relx=0.8, rely=0.82, relwidth=0.18, relheight=0.1)

    clear_and_create()


def send_mail(list_, to_mail):
    message = '\n\n'
    for i in list_:
        link = 'https://finance.yahoo.com/quote/{}?p={}'.format(i, i)
        url = link
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "lxml")
        price = soup.find('span', {'data-reactid': '32'}).text
        c_name = soup.find('h1', {'data-reactid': '7'}).text.split('(')[0]
        message += c_name + '\t-->\t' + price + '\t-->\t' + url + '\n\n'

    email = 'autostock2021@gmail.com'
    now = datetime.datetime.now().strftime('%I:%M')
    subject = "This is the automated stock details at {} designed by Vishal".format(now)
    message = "Subject:" + subject + "\n\n" + message
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, 'autostock@123')
        server.sendmail(email, to_mail, message)
        server.quit()
        messagebox.showinfo('Mail Function', 'Mail sent')

    except socket.gaierror:
        pass
    except smtplib.SMTPRecipientsRefused:
        messagebox.showerror('Mail Function', 'mail id invalid')


def Price(name):
    link = 'https://finance.yahoo.com/quote/{}?p={}'.format(name, name)
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    price = soup.find('span', {'data-reactid': '32'}).text
    c_name = soup.find('h1', {'data-reactid': '7'}).text.split('(')[0]
    return c_name, price


def home():
    global my_label, add_but, view_but
    my_label = Label(frame, bg="#80c1ff", font=('Aerial', 15))
    my_label.place(relx=0.15, rely=0.25, relheight=0.2, relwidth=0.75)
    my_label.config(text='Welcome to Stocks Viewer App\nClick Add button to start or\n Click Open button to view')

    add_but = Button(frame, text='Add', font=('Aerial', 15), command=add)
    view_but = Button(frame, text='Open', font=('Aerial', 15), command=opener)
    add_but.place(relx=0.3, rely=0.5, relheight=0.1, relwidth=0.15)
    view_but.place(relx=0.55, rely=0.5, relheight=0.1, relwidth=0.15)


home()

menu = Menu(root)
root.config(menu=menu)
file = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=file)
file.add_command(label='Save', command=save)
file.add_command(label='Open', command=opener)
file.add_command(label='Add', command=add)

status_bar = Label(root, anchor=E)
status_bar.pack(fill=X, side=BOTTOM)
content = str(len(os.listdir(path='F:/vishal/python files/PycharmProjects/stock_data'))) + ' Stock Data Set Available'
status_bar.config(text=content)
root.mainloop()
