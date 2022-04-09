from tkinter import *
import tkinter as tk
from tkinter import filedialog, Text, messagebox
import os

root = Tk()
root.geometry("400x463+900+0")
root.tk.call("source", "F:\codings\python files\Gui\Sun-Valley-ttk-theme\sun-valley.tcl")
root.tk.call("set_theme", "dark")
root.resizable(height=False, width=False)
root.title('RunApps')
root.wm_iconbitmap('F:\\codings\\python files\\Gui\\projects\\Images\\runapp.ico')
apps = []
filename = None

class ELabel(Label):
    def __init__(self, parent, *args, **kwargs):
        Label.__init__(self, parent, *args, **kwargs)

        self.context_menu = Menu(tearoff=0)
        # self.context_menu.add_command(label=self.cget("text"), state='disabled')
        # self.context_menu.add_separator()
        self.context_menu.add_command(label='Remove', command=lambda: self.remove())
        
        self.bind("<Button-3>", self.popup)

    def popup(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def remove(self):
        apps.remove(self.cget("text"))
        for widget in frame.winfo_children():
            widget.destroy()
        
        for app in apps:
            ELabel(frame, text=app, bg='grey').pack()

def addapp():
    appname = filedialog.askopenfilename(title="Select file", initialdir='C:',
                                            filetypes=(("executables", "*.exe"),('All types', '*.*')))
    if appname != '' and appname not in apps:
        apps.append(appname)
    for widget in frame.winfo_children():
        widget.destroy()
    for app in apps:
        ELabel(frame, text=app, bg='grey').pack()

def runapp():
    for app in apps:
        os.startfile(app)

def save():
    global filename
    if filename:
        with open(filename, 'w') as f:
            for app in apps:
                f.write(app + ',')
    else:
        if os.path.isdir('./save'):
            filename = filedialog.asksaveasfilename(title='Save File', initialdir='./save', filetypes=(('text', '*.txt'),), defaultextension='*.txt')
            if filename:
                with open(filename, 'w') as f:
                    for app in apps:
                        f.write(app + ',')
        else:
            os.mkdir('./save')
            filename = filedialog.asksaveasfilename(title='Save File', initialdir='./save', filetypes=(('text', '*.txt'),), defaultextension='*.txt')
            if filename:
                with open(filename, 'w') as f:
                    for app in apps:
                        f.write(app + ',')
    root.title(f'RunApps - {filename.split("/")[-1]}')
            
def open_file():
    global filename, apps
    if filename:
        with open(filename, 'r') as f:
            tempapps = f.read()
            ch_apps = tempapps.split(',')
            ch_apps = [x for x in ch_apps if x.strip()]
            if apps == ch_apps:
                pass
            else:
                if messagebox.askyesno('RunApps', 'Do you want to save?'):
                    save()
    elif len(apps):
        if messagebox.askyesno('RunApps', 'Do you want to save?'):
            save()
    if os.path.isdir('./save'):
        files = os.listdir('./save')
        if len(files):
            filename = filedialog.askopenfilename(title='Select File', initialdir='./save', filetypes=(('text', '*.txt'),('all','*.*')))
            if filename:
                for widget in frame.winfo_children():
                    widget.destroy()
                with open(filename, 'r') as f:
                    tempapps = f.read()
                    apps = tempapps.split(',')
                    apps = [x for x in apps if x.strip()]
                    for app in apps:
                        ELabel(frame, text=app, bg='grey').pack()
                root.title(f"RunApps - {filename.split('/')[-1]}")
    else:
        messagebox.showerror('RunApps', 'No Saved Files available,\nCreate New One!!')

def new():
    global filename, apps
    if filename:
        with open(filename, 'r') as f:
            tempapps = f.read()
            ch_apps = tempapps.split(',')
            ch_apps = [x for x in ch_apps if x.strip()]
            if apps == ch_apps:
                pass
            else:
                if messagebox.askyesno('RunApps', 'Do you want to save?'):
                    save()
    elif len(apps):
        if messagebox.askyesno('RunApps', 'Do you want to save?'):
            save()
    
    for widget in frame.winfo_children():
        widget.destroy()
    root.title('RunApps')
    apps = []
    filename = None
                

main_menu = Menu(tearoff=0)
root.config(menu=main_menu)
main_menu.add_command(label='Save', command=lambda: save())
main_menu.add_command(label='Open', command=lambda: open_file())
main_menu.add_command(label='New',command=lambda: new())

canvas = Canvas(root, height=350, width=400,bg="#80c1ff",highlightthickness=0)
canvas.pack(fill=BOTH)

frame = Frame(canvas, bg="white")
frame.place(relheight=0.8,relwidth=0.9, relx=0.05, rely=0.08)

frame_1 = Frame(root, bg="#80c1ff")
frame_1.pack(fill=X)

openfile = Button(frame_1, text="Add App", command=lambda: addapp())
openfile.pack(pady=10)

runapp_but = Button(frame_1, text="Run Apps", command=runapp)
runapp_but.pack(pady=10)

# if os.path.isdir('./save'):
#     files = os.listdir('./save')
#     if len(files):
#         filename = filedialog.askopenfilename(title='Select File', initialdir='./save', filetypes=(('text', '*.txt'),('all','*.*')))
#         if filename:
#             with open(filename, 'r') as f:
#                 tempapps = f.read()
#                 apps = tempapps.split(',')
#                 apps = [x for x in apps if x.strip()]
#             root.title(f"RunApps - {filename.split('/')[-1]}")

# for app in apps:
#     ELabel(frame, text=app, bg='grey').pack()

def on_closing(event=None):
    global filename
    if filename:
        with open(filename, 'r') as f:
            tempapps = f.read()
            ch_apps = tempapps.split(',')
            ch_apps = [x for x in ch_apps if x.strip()]
            if apps == ch_apps:
                root.destroy()
            else:
                if messagebox.askyesno('RunApps', 'Do you want to save?'):
                    save()
                    root.destroy()
                else:
                    root.destroy()
    elif len(apps):
        if messagebox.askyesno('RunApps', 'Do you want to save?'):
            save()
            root.destroy()
        else:
            root.destroy()
    else:
        root.destroy()



root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

