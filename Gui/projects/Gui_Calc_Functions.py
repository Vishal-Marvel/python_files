import tkinter as tk
import math, requests
import datetime
import tkinter.tix as tix
from tkinter import ttk
from tkinter import messagebox

global root, base_calc


class Add_menu_bar:
    def __init__(self):
        global base_calc
        self.create_menu()

    def create_menu(self):
        self.my_menu = tk.Menu(root)
        root.config(menu=self.my_menu)
        self.calculator_menu_create()
        self.convertor_menu_create()
        self.history_menu_create()

    def calculator_menu_create(self):
        self.calculator_menu = tk.Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="Calculators", menu=self.calculator_menu)
        self.calculator_menu.add_command(label="Standard", command=lambda: base_calc.base_calculator())
        self.calculator_menu.add_command(label="Scientific", command=lambda: base_calc.sci_calc.scientific_calculator())
        self.calculator_menu.add_command(label="Age Finder", command=lambda: base_calc.sci_calc.age.find_age())
        self.calculator_menu.bind_all("<Control-q>", lambda e: root.destroy())
        
    def convertor_menu_create(self):
        self.convertor_menu = tk.Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label="Convertors", menu=self.convertor_menu)
        self.convertor_menu.add_command(label="Currency", command=lambda: base_calc.sci_calc.currency.screen())
        self.convertor_menu.add_command(label="Volume", command=lambda: base_calc.sci_calc.volume.screen())
        self.convertor_menu.add_command(label="Length", command=lambda: base_calc.sci_calc.length.screen())
        self.convertor_menu.add_command(label="Weight", command=lambda: base_calc.sci_calc.weight.screen())
        self.convertor_menu.add_command(label="Temperature", command=lambda: base_calc.sci_calc.temp.screen())
        self.convertor_menu.add_command(label="Speed", command=lambda: base_calc.sci_calc.speed.screen())

    def history_menu_create(self):
        self.history_menu = tk.Menu(self.my_menu, tearoff=0)
        self.my_menu.add_cascade(label='History', menu=self.history_menu)
        self.history_menu.add_command(label="View History", command=lambda: base_calc.history.screen())
        self.history_menu.add_command(label="Clear History", command=lambda: base_calc.history.clear())
    

class Button(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = 'light blue'

    def on_leave(self, e):
        self['background'] = self.defaultBackground


class History:
    question = []

    def screen(self):
        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="HISTORY")
        title.place(relwidth=1, relheight=0.16)

        return_to = Button(self.frame, text='Return', font=15, command=lambda: base_calc.base_calculator())
        return_to.place(rely=0.9, relx=0.75, relwidth=0.2, relheight=0.1)

        if len(self.question) > 0:
            clear_all = Button(self.frame, text='clear all', font=15, command=lambda: self.clear())
            clear_all.place(rely=0.9, relx=0.5, relwidth=0.2, relheight=0.1)

            s = tk.Label(self.frame, bg="#80c1ff", text="S.No.")
            s.place(relx=0.23, rely=0.175, relheight=0.07, relwidth=0.1)

            i = tk.Label(self.frame, bg="#80c1ff", text="Input")
            i.place(relx=0.45, rely=0.175, relheight=0.07, relwidth=0.25)

            self.output_name()

        else:
            tk.Label(self.frame, text="No History created yet").place(relx=0.27, rely=0.3, relheight=0.1, relwidth=0.4)

    def clear(self):
        self.question.clear()
        base_calc.base_calculator()

    def output(self, value):
        global base_calc
        if '√' in value:
            base_calc.sci_calc.from_history(value)
        elif 'log' in value:
            base_calc.sci_calc.log.from_history(value)
        elif 'sin' in value or 'cos' in value or 'tan' in value or 'sec' in value or 'cot' in value:
            base_calc.sci_calc.trigo.from_history(value)
        else:
            base_calc.from_history(value)

    def output_name(self, start=0, end=7):
        k = start
        j = 0
        frame = tk.Frame(self.frame, bg="#80c1ff")
        frame.place(rely=0.245, relwidth=1, relheight=0.6)
        for i in self.question[start:end]:
            s = tk.Label(frame, text=str(k + 1))
            s.place(relx=0.23, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.1)
            name = Button(frame, text=i, command=lambda id=i: self.output(id))
            name.place(relx=0.45, rely=0.01 + j * 0.135, relheight=0.12, relwidth=0.4)
            j += 1
            k += 1

        empty = tk.Label(self.frame, bg="#80c1ff")
        empty.place(rely=0.9, relx=0.25, relwidth=0.2, relheight=0.1)
        empty_1 = tk.Label(self.frame, bg="#80c1ff")
        empty_1.place(rely=0.9, relwidth=0.2, relheight=0.1)

        if len(self.question) > end:
            next_page = Button(self.frame, text='Next', font=15,
                               command=lambda: self.output_name(start=end, end=end + 7))
            next_page.place(rely=0.9, relx=0.25, relwidth=0.2, relheight=0.1)

        if start != 0:
            previous = Button(self.frame, text="Previous", font=15,
                              command=lambda: self.output_name(start=start - 7, end=start))
            previous.place(rely=0.9, relwidth=0.2, relheight=0.1)

    pass


class Base_Calc:

    def __init__(self):

        self.sci_calc = Sci_Calc()
        self.history = History()
        self.f_history = False
        self.prev_val = ''
        self.calculated = False

    def clear(self):
        new_value = self.output.get()
        tot_value = ""
        for i in new_value[:len(new_value) - 1]:
            tot_value += i
        self.prev_val = tot_value
        self.display(tot_value)

    def all_clear(self):
        self.output.delete(0, tk.END)
        self.prev_val = ''

    def calculate(self):
        
        try:
            if self.output.get():
                question = self.output.get()
                tot_value = question
                try:
                    if '√' in tot_value:
                        rem = tot_value.split('√')[0]
                        if rem:
                            if rem[-1] not in '+-*/':
                                rem += '*'
                        value = tot_value.split('√')[1]
                        base_value = ''
                        for i in value:
                            if i in '+-*/':
                                break
                            elif i == '^':
                                base_value += '**'
                                continue
                            base_value += i
                        sq_rt_val = str(round(math.sqrt(float(eval(base_value))),3))
                        if '**' in base_value:
                            base_value = base_value.replace('**', '^')
                        rem_2 = tot_value.split('√' + base_value)[1]
                        tot_value = rem + sq_rt_val + rem_2
                    if '^' in tot_value:
                        tot_value = tot_value.replace('^', '**')

                    if '+' in tot_value or '-' in tot_value or '*' in tot_value or '/' in tot_value:
                        tot_value = str(eval(tot_value))
                        if tot_value.endswith('.0'):
                            tot_value = tot_value.replace(".0", "")
                        self.prev_val = tot_value
                        self.display(tot_value)
                        if question != tot_value:
                            self.calculated = True
                        if question not in self.history.question and question != tot_value:
                            self.history.question.append(question)
                    else:
                        if tot_value.endswith('.0'):
                            tot_value = tot_value.replace(".0", "")
                        self.prev_val = tot_value
                        self.display(tot_value)
                        if question != tot_value:
                            self.calculated = True
                        if question not in self.history.question and question != tot_value:
                            self.history.question.append(question)
                except SyntaxError:
                    messagebox.showerror("GUI_CALC", "INVALID INPUT")
                except ZeroDivisionError:
                    messagebox.showerror("GUI_CALC", "INFINITY")
            else:
                messagebox.showerror("GUI_CALC", "ENTER A VALUE")
        except tk.TclError:
            pass
        self.f_history = False

    def sq_rt(self):
        try:
            tot_value = self.output.get()
            base, base_value = "√", ""
            for i in tot_value[-1:-len(tot_value) - 1:-1]:
                if i in "+-*/":
                    break
                base += i
            for i in base[-1:-len(base) - 1:-1]:
                base_value += i
            tot_value += '√'
            rem = tot_value.split(base_value)[0]
            pert_val = str(round(math.sqrt(float(eval(base_value.replace('√', '')))),3))
            tot_value = rem + pert_val
            self.prev_val = tot_value
            self.display(tot_value)
        except ValueError:
            messagebox.showerror("GUI_CALC", "INVALID INPUT")
        finally:
            if base.replace('√','', 1) not in self.history.question:
                self.history.question.append(base.replace('√','', 1))

    def add_value(self, value):

        self.display(self.output.get() + value)

    def display(self, value):
        self.output.delete(0, tk.END)

        self.output.insert(0, value)

    def change_sign(self):
        value = self.output.get()
        self.calculated = False
        if value.startswith('-'):
            self.prev_val = value.replace('-', '')
            self.display(self.prev_val)
        else:
            self.prev_val = '-' + value
            self.display(self.prev_val)

    def from_history(self, value):
        self.base_calculator()
        self.f_history = True
        self.prev_val = value
        self.display(value)


    def callback(self, *args):
        if not self.f_history:
            try:
                key = self.output.get()[-1]
                if self.output.get().startswith('0') and self.output.get().isnumeric() and not self.output.get() == '0':
                    self.display(self.output.get().replace('0', ""))
                    self.prev_val = self.prev_val.replace('0', "")
                
                if not (key.isnumeric() or key in "/-+*.^√"):
                    i = len(self.output.get())
                    self.output.delete(i - 1, tk.END)

                if key == '√' and self.output.get() != '√':
                    self.sq_rt()

                if key == "." and self.output.get().startswith('.'):
                    self.prev_val = '0' + key
                    self.display(self.prev_val)

                if not self.output.get().startswith(self.prev_val):
                    self.display(self.prev_val)

                if key in "√/+*.^" or '---' in self.output.get():
                    try:
                        if key == self.prev_val[-1]:
                            self.display(self.prev_val)

                    except IndexError:
                        pass

                if self.calculated:
                    self.calculated = False

                    if key.isnumeric():
                        i = len(self.output.get()) - 1
                        self.output.delete(0, i)
                        self.prev_val = self.output.get()

                if key == '.':
                    if self.prev_val.endswith('.'):
                        i = len(self.output.get())
                        self.output.delete(i - 1, tk.END)
                    elif '.' in self.prev_val:
                        val = self.prev_val.split('.')[1]
                        for j in val:
                            if j not in '+-*/':
                                i = len(self.output.get())
                                self.output.delete(i - 1, tk.END)
                            break
                    

                if len(self.output.get()) < 20:
                    self.output.config(font=('arial', 15))
                elif 20 <= len(self.output.get()) < 25:
                    self.output.config(font=('arial', 13))
                elif 25 <= len(self.output.get()) < 30:
                    self.output.config(font=('arial', 11))
                elif 30 <= len(self.output.get()) < 35:
                    self.output.config(font=('arial', 9))
                elif 35 <= len(self.output.get()) < 50:
                    self.output.config(font=('arial', 7))
                # if len(self.output.get()) > 50:
                #     self.output.config(font=('arial', 5))
                self.prev_val = self.output.get()
                
            except IndexError:
                pass

    def base_calculator(self):
        try:
            self.sci_calc.frame.destroy()
            self.prev_val = '0'
        except AttributeError:
            pass
        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=0.3, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="PYTHON CALCULATOR")
        title.place(relwidth=1, relheight=0.45)

        result = Button(self.frame, text="=", font=('arial', 20), command=lambda: self.calculate(), bg='DarkOliveGreen1')
        result.place(rely=0.5, relx=0.825, relheight=0.52, relwidth=0.15)

        self.text = tk.StringVar()

        tip = tix.Balloon(root)
        # self.vcmd = root.register(lambda: self.callback)

        self.output = tk.Entry(self.frame, bg="white", borderwidth=3, relief="groove", font=('arial', 15),
                               justify='right', textvariable=self.text)
        self.output.place(rely=0.5, relwidth=0.78, relheight=0.52)
        self.output.focus()

        self.output.insert(0, '0')

        self.frame.bind_all("<Return>", lambda e: self.calculate())
        self.frame.bind_all("<Delete>", lambda e: self.all_clear())
        self.frame.bind_all("<BackSpace>", lambda e: self.clear())
        self.frame.bind_all("<=>", lambda e: self.calculate())

        self.text.trace_add("write", self.callback)

        lower_frame = tk.Frame(root, bg="#80c1ff", bd=7)
        lower_frame.place(relx=0.5, rely=0.3, relwidth=1, relheight=0.7, anchor='n')

        num_1 = Button(lower_frame, font=('arial', 15), text="1", command=lambda: self.add_value('1'))
        num_1.place(relx=0.01, rely=0.02, relheight=0.17, relwidth=0.16)

        num_2 = Button(lower_frame, font=('arial', 15), text="2", command=lambda: self.add_value('2'))
        num_2.place(relx=0.21, rely=0.02, relheight=0.17, relwidth=0.16)

        num_3 = Button(lower_frame, font=('arial', 15), text="3", command=lambda: self.add_value('3'))
        num_3.place(relx=0.41, rely=0.02, relheight=0.17, relwidth=0.16)

        num_4 = Button(lower_frame, font=('arial', 15), text="4", command=lambda: self.add_value('4'))
        num_4.place(relx=0.01, rely=0.25, relheight=0.17, relwidth=0.16)

        num_5 = Button(lower_frame, font=('arial', 15), text="5", command=lambda: self.add_value('5'))
        num_5.place(relx=0.21, rely=0.25, relheight=0.17, relwidth=0.16)

        num_6 = Button(lower_frame, font=('arial', 15), text="6", command=lambda: self.add_value('6'))
        num_6.place(relx=0.41, rely=0.25, relheight=0.17, relwidth=0.16)

        num_7 = Button(lower_frame, font=('arial', 15), text="7", command=lambda: self.add_value('7'))
        num_7.place(relx=0.01, rely=0.5, relheight=0.17, relwidth=0.16)

        num_8 = Button(lower_frame, font=('arial', 15), text="8", command=lambda: self.add_value('8'))
        num_8.place(relx=0.21, rely=0.5, relheight=0.17, relwidth=0.16)

        num_9 = Button(lower_frame, font=('arial', 15), text="9", command=lambda: self.add_value('9'))
        num_9.place(relx=0.41, rely=0.5, relheight=0.17, relwidth=0.16)

        num_0 = Button(lower_frame, font=('arial', 15), text="0", command=lambda: self.add_value('0'))
        num_0.place(relx=0.21, rely=0.75, relheight=0.17, relwidth=0.16)

        oper_dot = Button(lower_frame, font=('arial', 25), text=".", anchor='center', command=lambda: self.add_value('.'))
        oper_dot.place(relx=0.41, rely=0.75, relheight=0.17, relwidth=0.16)

        oper_clear = Button(lower_frame, font=('arial', 20), text="C", command=lambda: self.clear())
        oper_clear.place(relx=0.625, rely=0.02, relheight=0.17, relwidth=0.16)

        oper_all_clear = Button(lower_frame, font=('arial', 15), text="AC", command=lambda: self.all_clear())
        oper_all_clear.place(relx=0.825, rely=0.02, relheight=0.17, relwidth=0.16)

        oper_add = Button(lower_frame, font=("bold", 25), text="+", command=lambda: self.add_value('+'))
        oper_add.place(relx=0.625, rely=0.25, relheight=0.17, relwidth=0.16)

        oper_sub = Button(lower_frame, font=("bold", 30), text="-", command=lambda: self.add_value('-'))
        oper_sub.place(relx=0.825, rely=0.25, relheight=0.17, relwidth=0.16)

        oper_mul = Button(lower_frame, font=('arial', 20), text="x", command=lambda: self.add_value('*'))
        oper_mul.place(relx=0.625, rely=0.5, relheight=0.17, relwidth=0.16)

        oper_div = Button(lower_frame, font=("bold", 25), text="/", command=lambda: self.add_value('/'))
        oper_div.place(relx=0.825, rely=0.5, relheight=0.17, relwidth=0.16)

        oper_pow = Button(lower_frame, font=('arial', 18), text="^", command=lambda: self.add_value('^'))
        oper_pow.place(relx=0.625, rely=0.75, relheight=0.17, relwidth=0.16)

        oper_sq_rt = Button(lower_frame, font=('arial', 20), text="√", command=lambda: self.add_value('√'))
        oper_sq_rt.place(relx=0.825, rely=0.75, relheight=0.17, relwidth=0.16)

        change_sign = Button(lower_frame, font=('arial', 15), text="+/-",
                               command=lambda: self.change_sign())
        change_sign.place(relx=0.01, rely=0.75, relheight=0.17, relwidth=0.16)

        tip.bind_widget(change_sign,msg="Change Sign")
    pass


class Sci_Calc:

    def __init__(self):
        self.log = Log()
        self.anti_log = Log()
        self.age = Age_find()
        self.f_history = False
        self.trigo = Trigonometric()
        try:
            self.currency = Currency()
        except requests.exceptions.ConnectionError:
            pass
        self.temp = Temperature()
        self.weight = Weight()
        self.volume = Volume()
        self.length = Length()
        self.speed = Speed()
        self.history = History()
        self.prev_val = ''
        self.calculated = False
        global base_calc

    def display(self, value):
        self.output.delete(0, tk.END)
        self.output.insert(0, value)

    def clear(self):
        new_value = self.output.get()
        tot_value = ""
        for i in new_value[:len(new_value) - 1]:
            tot_value += i
        self.prev_val = tot_value
        self.display(tot_value)

    def all_clear(self):
        self.output.delete(0, tk.END)
        self.prev_val = ''

    def factorial(self):
        try:
            tot_value = self.output.get()
            base, base_value = "!", ""
            for i in tot_value[-1:-len(tot_value) - 1:-1]:
                if i in "+-*/":
                    break
                base += i
            for i in base[-1:-len(base) - 1:-1]:
                base_value += i
            tot_value += '!'
            rem = tot_value.split(base_value)[0]
            # messagebox.showerror("GUI_CALC", f'{tot_value},{rem}, {base_value}')
            f = 1
            for j in range(1, int(base_value.replace('!', '')) + 1):
                f = f * j
            fact_val = str(f)[:23]
            tot_value = rem + fact_val
            self.prev_val = tot_value
            self.display(self.prev_val)
        except ValueError:
            messagebox.showerror("GUI_CALC", "INVALID INPUT")
        except SyntaxError:
            messagebox.showerror("GUI_CALC", "INVALID INPUT")

    def ceil(self):
        try:
            value = float(self.output.get())
            self.prev_val = ''
            self.display(math.ceil(value))
        except ValueError:
            messagebox.showerror("GUI_CALC", "Enter a value")

    def abs(self):
        try:
            value = float(self.output.get())
            self.prev_val = ''
            values = str(abs(value))
            if values.endswith('.0'):
                values = values.replace('.0', '')
            self.prev_val = values
            self.f_history = True
            self.display(values)
            
        except ValueError:
            messagebox.showerror("GUI_CALC", "INVALID INPUT")

    def floor(self):
        try:
            value = float(self.output.get())
            self.prev_val = ''
            self.display(math.floor(value))
        except ValueError:
            messagebox.showerror("GUI_CALC", "Enter a value")

    def chk_prime(self):
        try:
            if '.' in self.output.get():
                num = int(self.output.get().split('.')[0])
            else:
                num = int(self.output.get())

            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        messagebox.showinfo("GUI_CALC", "It is not a prime")

                        break
                else:
                    messagebox.showinfo("GUI_CALC", "It is a prime")

            else:
                messagebox.showinfo("GUI_CALC", "It is neither a \nprime nor a composite")
        except ValueError:
            messagebox.showerror("GUI_CALC", "Enter a value in the box")
        except SyntaxError:
            messagebox.showerror("GUI_CALC", "INVALID INPUT")

        pass

    def percent(self):
        try:
            tot_value = self.output.get()
            base, base_value = "%", ""
            for i in tot_value[-1:-len(tot_value) - 1:-1]:
                if i in "+-*/":
                    break
                base += i
            for i in base[-1:-len(base) - 1:-1]:
                base_value += i
            tot_value += '%'
            rem = tot_value.split(base_value)[0]
            pert_val = str(float(base_value.replace('%', '')) / 100)[:23]
            tot_value = rem + pert_val
            self.prev_val = tot_value
            self.display(tot_value)
             
        except ValueError:
            messagebox.showerror("GUI_CALC", "INVALID INPUT")
        except SyntaxError:
            messagebox.showerror("GUI_CALC", "INVALID INPUT")
        
    def change_sign(self):
        value = self.output.get()
        self.calculated = False
        if value.startswith('-'):
            self.prev_val = value.replace('-', '')
            self.display(self.prev_val)
        else:
            self.prev_val = '-' + value
            self.display(self.prev_val)

    def add_value(self, value):
        self.display(self.output.get() + value)

    def sci_calculate(self):
        try:
            if self.output.get():
                question = tot_value = self.output.get()
                try:
                    if '√' in tot_value:
                        rem = tot_value.split('√')[0]
                        if rem:
                            if rem[-1] not in '+-*/':
                                rem += '*'
                        value = tot_value.split('√')[1]
                        base_value = ''
                        for i in value:
                            if i in '+-*/':
                                break
                            elif i == '^':
                                base_value += '**'
                                continue
                            base_value += i
                        sq_rt_val = str(round(math.sqrt(float(eval(base_value))),3))
                        if '**' in base_value:
                            base_value = base_value.replace('**', '^')
                        rem_2 = tot_value.split('√' + base_value)[1]
                        tot_value = rem + sq_rt_val + rem_2

                    if '^' in tot_value:
                        tot_value = tot_value.replace('^', '**')
                    
                    if '+' in tot_value or '-' in tot_value or '*' in tot_value or '/' in tot_value:
                        tot_value = str(eval(tot_value))
                        if tot_value.endswith('.0'):
                            tot_value = tot_value.replace(".0", "")
                        self.prev_val = tot_value
                        self.display(tot_value)
                        if question != tot_value:
                            self.calculated = True
                        if question not in self.history.question and question != tot_value:
                            self.history.question.append(question)
                    else:
                        if tot_value.endswith('.0'):
                            tot_value = tot_value.replace(".0", "")
                        self.prev_val = tot_value
                        self.display(tot_value)
                        if question != tot_value:
                            self.calculated = True
                        if question not in self.history.question and question != tot_value:
                            self.history.question.append(question)
                except SyntaxError :
                    messagebox.showerror("GUI_CALC", "INVALID INPUT")
                except ZeroDivisionError:
                    messagebox.showerror("GUI_CALC", "INFINITY")
            else:
                messagebox.showerror("GUI_CALC", "ENTER A VALUE")
        except tk.TclError:
            pass
        self.f_history = False
    
    def sq_rt(self):
        try:
            first = tot_value = self.output.get()
            base, base_value = "√", ""
            for i in tot_value[-1:-len(tot_value) - 1:-1]:
                if i in "+-*/":
                    break
                base += i
            for i in base[-1:-len(base) - 1:-1]:
                base_value += i
            tot_value += '√'
            rem = tot_value.split(base_value)[0]
            pert_val = str(round(math.sqrt(float(eval(base_value.replace('√', '')))),3))
            tot_value = rem + pert_val
            self.prev_val = tot_value
            self.display(tot_value)
            
        except ValueError:
            messagebox.showerror("GUI_CALC", "INVALID INPUT")
        finally:
            if first not in self.history.question:
                self.history.question.append(first)

    def from_history(self, value):
        self.scientific_calculator()
        self.prev_val = value
        self.f_history = True
        self.display(value)

    def callback(self, *args):
        if not self.f_history:
            try:
                key = self.output.get()[-1]
                if self.output.get().startswith('0') and self.output.get().isnumeric() and not self.output.get() == '0':
                    self.display(self.output.get().replace('0', ""))
                    self.prev_val = self.prev_val.replace('0', "")
                
                if not (key.isnumeric() or key in "/-+*.^()√"):
                    i = len(self.output.get())
                    self.output.delete(i - 1, tk.END)
                if key == '!':
                    self.factorial()
                if key == '%':
                    self.percent()

                if key == '√' and self.output.get() != '√':
                    self.sq_rt()
                
                if key == '.':
                    if '.' in self.prev_val:
                        i = len(self.output.get())
                        self.output.delete(i - 1, tk.END)

                if key == "." and self.output.get().startswith('.'):
                    self.prev_val = '0' + key
                    self.display(self.prev_val)

                if not self.output.get().startswith(self.prev_val):
                    self.display(self.prev_val)

                if key in "/+*.^√" or '---' in self.output.get():
                    try:
                        if key == self.prev_val[-1]:
                            self.display(self.prev_val)
                    except IndexError:
                        pass
                        
                if self.calculated:
                    self.calculated = False
                    if key.isnumeric():
                        i = len(self.output.get()) - 1
                        self.output.delete(0, i)
                        self.prev_val = self.output.get()

                if len(self.output.get()) < 20:
                    self.output.config(font=('arial', 15))
                elif 20 <= len(self.output.get()) < 25:
                    self.output.config(font=('arial', 13))
                elif 25 <= len(self.output.get()) < 30:
                    self.output.config(font=('arial', 11))
                elif 30 <= len(self.output.get()) < 35:
                    self.output.config(font=('arial', 9))
                elif 35 <= len(self.output.get()) < 50:
                    self.output.config(font=('arial', 7))
                # if len(self.output.get()) > 50:
                #     self.output.config(font=('arial', 5))
                self.prev_val = self.output.get()
            except IndexError:
                pass

    def scientific_calculator(self):
        self.prev_val = ''
        base_calc.frame.destroy()
        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.0001, relwidth=1, relheight=0.3, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="SCIENTIFIC CALCULATOR")
        title.place(relwidth=1, relheight=0.45)

        result = Button(self.frame, text="=", font=('arial', 20), command=lambda: self.sci_calculate(), bg='DarkOliveGreen1')
        result.place(rely=0.5, relx=0.825, relheight=0.52, relwidth=0.15)

        self.text = tk.StringVar()
        self.output = tk.Entry(self.frame, bg="white", borderwidth=3, relief="groove", font=('arial', 15),
                               justify='right', textvariable=self.text)
        self.output.place(rely=0.5, relwidth=0.78, relheight=0.52)
        self.output.focus()

        self.frame.bind_all("<Return>", lambda e: self.sci_calculate())
        self.frame.bind_all("<Delete>", lambda e: self.all_clear())
        self.frame.bind_all("<=>", lambda e: self.sci_calculate())
        self.frame.bind_all("<BackSpace>", lambda e: self.clear())

        self.text.trace_add("write", self.callback)

        tip = tix.Balloon(root)

        self.output.insert(0, '0')

        lower_frame_1 = tk.Frame(root, bg="#80c1ff", bd=7)
        lower_frame_1.place(relx=0.5, rely=0.3, relwidth=1, relheight=0.7, anchor='n')

        oper_log = Button(lower_frame_1, font=('arial', 15), text="LOG",
                          command=lambda: self.log.log_func())
        oper_log.place(relx=0.01, rely=0.02, relheight=0.17, relwidth=0.16)

        oper_trigo = Button(lower_frame_1, font=('arial', 10), text="Trigono\nmetric",
                            command=lambda: self.trigo.screen())
        oper_trigo.place(relx=0.21, rely=0.02, relheight=0.17, relwidth=0.16)

        oper_chk_prime = Button(lower_frame_1, font=('arial', 12), text="Check\nPrime",
                                command=lambda: self.chk_prime())
        oper_chk_prime.place(relx=0.41, rely=0.02, relheight=0.17, relwidth=0.16)

        num_1 = Button(lower_frame_1, font=('arial', 15), text="1", command=lambda: self.add_value('1'))
        num_1.place(relx=0.01, rely=0.25, relheight=0.15, relwidth=0.16)

        num_2 = Button(lower_frame_1, font=('arial', 15), text="2", command=lambda: self.add_value('2'))
        num_2.place(relx=0.21, rely=0.25, relheight=0.15, relwidth=0.16)

        num_3 = Button(lower_frame_1, font=('arial', 15), text="3", command=lambda: self.add_value('3'))
        num_3.place(relx=0.41, rely=0.25, relheight=0.15, relwidth=0.16)

        num_4 = Button(lower_frame_1, font=('arial', 15), text="4", command=lambda: self.add_value('4'))
        num_4.place(relx=0.01, rely=0.42, relheight=0.15, relwidth=0.16)

        num_5 = Button(lower_frame_1, font=('arial', 15), text="5", command=lambda: self.add_value('5'))
        num_5.place(relx=0.21, rely=0.42, relheight=0.15, relwidth=0.16)

        num_6 = Button(lower_frame_1, font=('arial', 15), text="6", command=lambda: self.add_value('6'))
        num_6.place(relx=0.41, rely=0.42, relheight=0.15, relwidth=0.16)

        num_7 = Button(lower_frame_1, font=('arial', 15), text="7", command=lambda: self.add_value('7'))
        num_7.place(relx=0.01, rely=0.59, relheight=0.15, relwidth=0.16)

        num_8 = Button(lower_frame_1, font=('arial', 15), text="8", command=lambda: self.add_value('8'))
        num_8.place(relx=0.21, rely=0.59, relheight=0.15, relwidth=0.16)

        num_9 = Button(lower_frame_1, font=('arial', 15), text="9", command=lambda: self.add_value('9'))
        num_9.place(relx=0.41, rely=0.59, relheight=0.15, relwidth=0.16)

        num_0 = Button(lower_frame_1, font=('arial', 15), text="0", command=lambda: self.add_value('0'))
        num_0.place(relx=0.21, rely=0.76, relheight=0.15, relwidth=0.16)
        
        oper_dot = Button(lower_frame_1, font=('arial', 25), text=".", justify='center', command=lambda: self.add_value('.'))
        oper_dot.place(relx=0.41, rely=0.76, relheight=0.15, relwidth=0.16)
        
        change_sign = Button(lower_frame_1, font=('arial', 15), text="+/-",
                           command=lambda: self.change_sign())
        change_sign.place(relx=0.01, rely=0.76, relheight=0.15, relwidth=0.16)

        oper_clear = Button(lower_frame_1, font=('arial', 20), text="C", command=lambda: self.clear())
        oper_clear.place(relx=0.625, rely=0.02, relheight=0.17, relwidth=0.16)

        oper_all_clear = Button(lower_frame_1, font=('arial', 15), text="AC",
                                command=lambda: self.all_clear())
        oper_all_clear.place(relx=0.825, rely=0.02, relheight=0.17, relwidth=0.16)

        oper_abs = Button(lower_frame_1, font=('arial', 15), text="|x|", command=self.abs)
        oper_abs.place(relx=0.625, rely=0.21, relheight=0.17, relwidth=0.16)

        ten_pow = Button(lower_frame_1, font=("bold", 15), text="10^", command=lambda: self.add_value('10^'))
        ten_pow.place(relx=0.825, rely=0.21, relheight=0.17, relwidth=0.16)

        oper_ceil = Button(lower_frame_1, font=('arial', 15), text="⌈x⌉", command=self.ceil)
        oper_ceil.place(relx=0.625, rely=0.4,relheight=0.17, relwidth=0.16)

        oper_floor = Button(lower_frame_1, font=("bold", 15), text="⌊x⌋", command=self.floor)
        oper_floor.place(relx=0.825, rely=0.4, relheight=0.17, relwidth=0.16)

        oper_fact = Button(lower_frame_1, font=("bold", 15), text="!", command=lambda: self.factorial())
        oper_fact.place(relx=0.625, rely=0.59, relheight=0.17, relwidth=0.16)

        oper_pert = Button(lower_frame_1, font=("bold", 15), text="%", command=lambda: self.percent())
        oper_pert.place(relx=0.825, rely=0.59, relheight=0.17, relwidth=0.16)

        oper_pow = Button(lower_frame_1, font=('arial', 15), text="^", command=lambda: self.add_value('^'))
        oper_pow.place(relx=0.625, rely=0.78, relheight=0.17, relwidth=0.16)

        oper_sq_rt = Button(lower_frame_1, font=('arial', 15), text="√", command=lambda: self.add_value('√'))
        oper_sq_rt.place(relx=0.825, rely=0.78, relheight=0.17, relwidth=0.16)

        tip.bind_widget(oper_ceil,msg="Ceil")
        tip.bind_widget(oper_floor,msg="Floor")
        tip.bind_widget(change_sign,msg="Change Sign")
        tip.bind_widget(oper_abs, msg="Absolute")

    pass


class Log:
    def __init__(self):
        self.log_value = ''
        self.history = History()
        global base_calc

    def display(self, value):
        self.output = tk.Label(self.log_frame, font=('arial', 15),
                               justify='center', text=value)
        self.output.place(relx=0.1, rely=0.14, relwidth=0.8, relheight=0.12)

    def from_history(self, value):
        value = str(value)
        values = value.split(')')
        expo = values[0].split('(')[1]
        base = values[1]
        self.log_func()
        self.expo_ent.insert(0, expo)
        self.base_ent.insert(0, base)
        self.log(expo, base)

    def log(self, expo, base):
        # try:
        subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

        q = "log(" + expo + ")" + base
        if base == 'e':
            self.log_value = str(math.log(float(expo)))
        else:
            self.log_value = str(math.log(float(expo), float(base)))
        self.display("log(" + expo + ")" + base.translate(subscript) + " = " + self.log_value)
        if q not in self.history.question:
            self.history.question.append(q)
        # except ValueError:
        #     self.display("INVALID INPUT")
        # except ZeroDivisionError:
        #     self.display("INVALID INPUT")

    def log_func(self):
        try:
            base_calc.sci_calc.frame.destroy()
        except AttributeError:
            pass
        self.log_frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.log_frame.place(relx=0.5, rely=0.001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.log_frame, bg="light green", font=('bold', 15), text="LOG CALCULATOR")
        title.place(relwidth=1, relheight=0.12)

        expo = tk.Label(self.log_frame, text="Exponent :", font=10)
        expo.place(relx=0.02, rely=0.35, relheight=0.1, relwidth=0.23)

        self.text = tk.StringVar()
        self.ent_text = tk.StringVar()

        self.expo_ent = tk.Entry(self.log_frame, textvariable=self.ent_text, font=10)
        self.expo_ent.place(relx=0.3, rely=0.35, relheight=0.1, relwidth=0.6)
        self.expo_ent.focus()

        base = tk.Label(self.log_frame, text="Base :", font=10)
        base.place(relx=0.02, rely=0.5, relheight=0.1, relwidth=0.23)

        def callback(*args):
            try:
                if not self.base_ent.get()[-1].isnumeric():
                    i = len(self.base_ent.get()) - 1
                    self.base_ent.delete(i, tk.END)
            except IndexError:
                pass

        def ent_callback(*args):
            try:
                if not self.expo_ent.get()[-1].isnumeric():
                    i = len(self.expo_ent.get()) - 1
                    self.expo_ent.delete(i, tk.END)
            except IndexError:
                pass

        self.base_ent = tk.Entry(self.log_frame, textvariable=self.text, font=10)
        self.base_ent.place(relx=0.3, rely=0.5, relheight=0.1, relwidth=0.6)

        self.text.trace_add("write", callback)
        self.ent_text.trace_add("write", ent_callback)

        calculate_log = Button(self.log_frame, text="Calculate", font=10,
                               command=lambda: self.log(self.expo_ent.get(), self.base_ent.get()))
        calculate_log.place(relx=0.38, rely=0.7, relheight=0.1, relwidth=0.23)

        history = Button(self.log_frame, font=15, text="History", command=lambda: self.history.screen())
        history.place(relx=0.18, rely=0.85, relheight=0.1, relwidth=0.2)

        return_butt = Button(self.log_frame, text="Return to Scientific", font=10,
                             command=lambda: base_calc.sci_calc.scientific_calculator())
        return_butt.place(relx=0.4, rely=0.85, relheight=0.1, relwidth=0.43)

    pass


class Age_find:
    def __init__(self):
        self.years = 0
        global base_calc

    def display(self, age='', next_birth='', error=''):
        if "INVALID" in error or "DOB" in error:
            self.output = tk.Label(self.age_frame, font=('arial', 12))
            self.output.place(relx=0.23, rely=0.15, relwidth=0.55, relheight=0.1)

            self.output['text'] = error

            error = tk.Label(self.age_frame, bg="#80c1ff")
            error.place(relx=0.02, rely=0.43, relheight=0.35, relwidth=1)
        else:
            self.output = tk.Label(self.age_frame, font=('arial', 12))
            self.output.place(relx=0.23, rely=0.15, relwidth=0.55, relheight=0.1)

            self.output['text'] = "Your age: " + str(self.years) + ' Years'
            label = tk.LabelFrame(self.age_frame, bg="#80c1ff", text="Other details:")
            label.place(relx=0.02, rely=0.41, relheight=0.4225, relwidth=0.935)

            age_val = tk.Label(label, text="AGE :", font=10, borderwidth=3, relief="groove")
            age_val.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.3)

            next_bday = tk.Label(label, text="Next birthday\ncomes in :", font=10, borderwidth=3,
                                 relief="groove")
            next_bday.place(relx=0.09, rely=0.48, relwidth=0.32, relheight=0.34)

            age_output = tk.Label(label, bg="white", borderwidth=3, relief="groove",
                                  font=('calibri', 15),
                                  justify='left', text=age)
            age_output.place(relx=0.45, rely=0.1, relwidth=0.5, relheight=0.3)

            next_output = tk.Label(label, bg="white", borderwidth=3, relief="groove",
                                   font=('calibri', 15),
                                   justify='left', text=next_birth)
            next_output.place(relx=0.45, rely=0.5, relwidth=0.5, relheight=0.3)

    def input_age(self):
        if not self.date_box.get() == 'DD' and not self.month_box.get() == 'MM' and not self.year_box.get() == 'YYYY':
            dob = self.date_box.get() + '/' + self.month_box.get() + '/' + self.year_box.get()
            date = dob.split('/')[0]
            month = dob.split('/')[1]
            year = dob.split('/')[2]
            self.calculate_age(date, month, year)
        else:
            self.display(error="INVALID FORMAT")

    def leap(self, i):
        if i % 4 == 0 and i % 100 != 0 or i % 400 == 0:
            return True
        else:
            return False

    def calculate_age(self, date, month, year):
        try:
            n = datetime.date(int(year), int(month), int(date))
            
        except ValueError:
            self.display(error="INVALID DATE")
        today = datetime.date.today()
        age_year = today.year - n.year - ((today.month, today.day) < (n.month, n.day))
        self.years = age_year
        if today.month in (2, 4, 6, 8, 9, 11, 1):
            days = 31
        elif today.month == 3:
            days = 28
        elif today.month == 3 and self.leap(today.year):
            days = 29
        else:
            days = 30
        if n.month in (1, 2, 4, 6, 8, 9, 11):
            rem_days = 31
        elif n.month == 3:
            rem_days = 28
        elif n.month == 3 and self.leap(today.year):
            rem_days = 29
        else:
            rem_days = 30
        if today.month == n.month and today.day == n.day:
            self.display(str(age_year) + " Y", "HAPPY BIRTHDAY")
            
        elif today.month > n.month and today.day > n.day:
            age_month = today.month - n.month
            age_day = today.day - n.day
            rem_month = (n.month + 12) - today.month - 1
            rem_day = (rem_days - today.day) + n.day
            self.display(str(age_year) + " Y, " + str(age_month) + " M, " + str(age_day) + " D ",
                            str(rem_month) + " M, " + str(rem_day) + " D")
            
        elif today.month == n.month and today.day > n.day:
            age_day = today.day - n.day
            rem_month = 11
            rem_day = (rem_days - today.day) + n.day + 1
            self.display(str(age_year) + " Y, " + str(age_day) + " D ",
                            str(rem_month) + " M, " + str(rem_day) + " D")
            
        elif today.month > n.month and today.day == n.day:
            age_month = today.month - n.month
            rem_month = (n.month + 12) - today.month
            self.display(str(age_year) + "Y, " + str(age_month) + "M ", str(rem_month) + "M ")
        elif today.month < n.month and today.day == n.day:
            age_month = (today.month + 12) - n.month
            rem_month = n.month - today.month
            self.display(str(age_year) + " Y, " + str(age_month) + " M ", str(rem_month) + " M ")
            
        elif today.month < n.month and today.day < n.day:
            age_month = (today.month + 11) - n.month
            age_day = (days - n.day) + today.day
            rem_month = n.month - today.month
            rem_day = n.day - today.day
            self.display(str(age_year) + "Y, " + str(age_month) + "M, " + str(age_day) + "D ",
                            str(rem_month) + " M, " + str(rem_day) + " D")
            
        elif today.month == n.month and today.day < n.day:
            age_month = (today.month + 11) - n.month
            age_day = (days - n.day) + today.day
            rem_day = n.day - today.day
            self.display(str(age_year) + " Y, " + str(age_month) + " M, " + str(age_day) + " D ",
                            str(rem_day) + " D")
            
        elif today.month > n.month and today.day < n.day:
            age_month = today.month - n.month - 1
            age_day = (days - n.day) + today.day
            rem_month = n.month + 12 - today.month
            rem_day = n.day - today.day
            if age_month:
                self.display(str(age_year) + " Y, " + str(age_month) + " M, " + str(age_day) + " D ",
                                str(rem_month) + " M, " + str(rem_day) + " D")
            else:
                self.display(str(age_year) + " Y, " + str(age_month) + " M, " + str(age_day) + " D ",
                                str(rem_month) + " M, " + str(rem_day) + " D")
            
        elif today.month < n.month and today.day > n.day:
            age_month = (today.month + 12) - n.month
            age_day = today.day - n.day
            rem_month = n.month - today.month - 1
            rem_day = (rem_days - today.day) + n.day
            if rem_month:
                self.display(str(age_year) + " Y, " + str(age_month) + " M, " + str(age_day) + " D ",
                                str(rem_month) + " M, " + str(rem_day) + " D")

            else:
                self.display(str(age_year) + " Y, " + str(age_month) + " M, " + str(age_day) + " D ",
                                str(rem_day) + " D")
            
        pass

    def find_age(self):
        try:
            base_calc.sci_calc.frame.destroy()
        except AttributeError:
            pass

        self.age_frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.age_frame.place(relx=0.5, rely=0.001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.age_frame, bg="light green", font=('bold', 15), text="AGE FINDER")
        title.place(relwidth=1, relheight=0.12)

        dob = tk.Label(self.age_frame, text="Enter your DOB:", font=5)
        dob.place(relx=0.01, rely=0.28, relheight=0.1, relwidth=0.4)

        self.fourth = tk.Frame(self.age_frame, bg="#80c1ff")
        self.fourth.place(relx=0.45, rely=0.3, relheight=0.13, relwidth=0.53)

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
            date = ['DD']
            if self.month_box.get() in ['1', '3', '5', '7', '8', '10' '12']:
                for i in [i for i in range(1, 32)]:
                    date.append(i)
                self.date_box['values'] = date

            elif self.month_box.get() in ['4', '6', '9', '11']:
                for i in [i for i in range(1, 31)]:
                    date.append(i)
                self.date_box['values'] = date
                if not self.date_box.get() == 'DD':
                    if int(self.date_box.get()) > 31:
                        self.date_box.current(0)

            elif self.month_box.get() == '2':
                i = int(self.year_box.get()) if self.year_box.get() != 'YYYY' else 2001
                if i % 4 == 0 and i % 100 != 0 or i % 400 == 0:
                    for i in [i for i in range(1, 30)]:
                        date.append(i)
                    self.date_box['values'] = date
                    if not self.date_box.get() == 'DD':
                        if int(self.date_box.get()) > 29:
                            self.date_box.current(0)

                else:
                    for i in [i for i in range(1, 29)]:
                        date.append(i)
                    self.date_box['values'] = date
                    if not self.date_box.get() == 'DD':
                        if int(self.date_box.get()) > 28:
                            self.date_box.current(0)
                    

        self.month_box.bind("<<ComboboxSelected>>", dates)
        self.year_box.bind("<<ComboboxSelected>>", dates)

        calculate = Button(self.age_frame, text='Calculate', font=('arial', 13)
                           , command=lambda: self.input_age())
        calculate.place(relx=0.34, rely=0.85, relheight=0.1225, relwidth=0.275)

    pass


class Trigonometric:
    def __init__(self):
        global base_calc
        self.deg = True
        self.history = History()

    def display(self, value):
        self.output = tk.Label(self.tri_frame, text=value, font=('bold', 12))
        self.output.place(relx=0.23, rely=0.15, relwidth=0.55, relheight=0.1)

    def from_history(self, value):
        value = str(value)
        tri = value.split('(')[0]
        val = value.split('(')[1]
        val = val[:len(val) - 1]
        self.screen()
        self.value.insert(0, val)
        if tri == "sin":
            self.sine(val)
        elif tri == "cos":
            self.cos(val)
        elif tri == "tan":
            self.tan(val)
        elif tri == "cosec":
            self.cosec(val)
        elif tri == "sec":
            self.sec(val)
        elif tri == "cot":
            self.cot(val)

    def to_history(self, value):
        if value not in self.history.question:
            self.history.question.append(value)

    def sine(self, sin_value):
        try:
            if self.deg:
                deg = math.radians(int(sin_value))
                sine = math.sin(deg)
            else:
                sine = math.sin(int(sin_value))
            self.display("sin(" + sin_value + ") = " + str(sine)[:9])
            self.to_history("sin(" + sin_value + ")")
        except ValueError:
            self.display("ENTER A VALUE")

    def cos(self, cos_value):
        try:
            if self.deg:
                deg = math.radians(int(cos_value))
                cos = round(math.cos(deg), 1)
            else:
                cos = round(math.cos(int(cos_value)), 1)
            
            self.display("cos(" + cos_value + ") = " + str(cos)[:9])
            self.to_history("cos(" + cos_value + ")")
        except ValueError:
            self.display("ENTER A VALUE")

    def tan(self, tan_value):
        try:
            if self.deg:
                deg = math.radians(int(tan_value))
                tan = round(math.sin(deg), 1) / round(math.cos(deg), 1)
            else:
                tan = round(math.tan(int(tan_value)), 1)
                # tan = round(math.sin(int(tan_value)), 1) / round(math.cos(int(tan_value)), 1)
            self.display("tan(" + tan_value + ") = " + str(tan)[:9])
            self.to_history("tan(" + tan_value + ")")
        except ValueError:
            self.display("ENTER A VALUE")
        except ZeroDivisionError:
            self.display("INFINITY")

    def cosec(self, cosec_value):
        try:
            if self.deg:
                deg = math.radians(int(cosec_value))
                sin = round(math.sin(deg), 1)
                cosec = 1 / sin
            else:
                sin = round(math.sin(int(cosec_value)), 1)
                cosec = 1 / sin
            self.display("cosec(" + cosec_value + ") = " + str(cosec)[:9])
            self.to_history("cosec(" + cosec_value + ")")
        except ValueError:
            self.display("ENTER A VALUE")
        except ZeroDivisionError:
            self.display("INFINITY")
            self.to_history("cosec(" + cosec_value + ")")

    def sec(self, sec_value):
        try:
            if self.deg:
                deg = math.radians(int(sec_value))
                cos = round(math.cos(deg), 1)
                sec = 1 / cos
            else:
                cos = round(math.cos(int(sec_value)), 1)
                sec = 1 / cos
            self.display("sec(" + sec_value + ") = " + str(sec)[:9])
            self.to_history("sec(" + sec_value + ")")
        except ValueError:
            self.display("ENTER A VALUE")
        except ZeroDivisionError:
            self.display("INFINITY")

    def cot(self, cot_value):
        try:
            if self.deg:
                deg = math.radians(int(cot_value))
                tan = round(math.sin(deg), 1) / round(math.cos(deg), 1)
                cot = 1 / tan
            else:
                tan = round(math.tan(int(cot_value)), 1)
                cot = 1 / tan
            self.display("cot(" + cot_value + ") = " + str(cot)[:9])
            self.to_history("cot(" + cot_value + ")")
        except ValueError:
            self.display("ENTER A VALUE")
        except ZeroDivisionError:
            self.display("INFINITY")
            self.to_history("cot(" + cot_value + ")")

    def deg_rad(self):
        if self._text.get() == "Degrees: ":
            self._text.set("Radians: ")
            self.deg = False
        else:
            self._text.set("Degrees: ")
            self.deg = True

    def screen(self):
        try:
            base_calc.sci_calc.frame.destroy()
        except AttributeError:
            pass
        self._text = tk.StringVar()
        self._text.set("Degrees: ")
        self.tri_frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.tri_frame.place(relx=0.5, rely=0.001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.tri_frame, bg="light green", font=('bold', 15), text="TRIGONOMETRIC CALCULATOR")
        title.place(relwidth=1, relheight=0.12)

        self.deg_rad_but = tk.Button(self.tri_frame, textvariable=self._text, font=5, command=lambda: self.deg_rad())
        self.deg_rad_but.place(relx=0.01, rely=0.28, relheight=0.13, relwidth=0.4)

        def callback(*args):
            try:
                if not self.value.get()[-1].isnumeric():
                    i = len(self.value.get()) - 1
                    self.value.delete(i, tk.END)
            except IndexError:
                pass

        self.text = tk.StringVar()

        self.value = tk.Entry(self.tri_frame, font=('calibri', 15), justify='center', textvariable=self.text)
        self.value.place(relx=0.45, rely=0.28, relheight=0.13, relwidth=0.53)
        self.value.focus()

        self.text.trace_add("write", callback)

        sine = Button(self.tri_frame, text='Sine', font=('arial', 12),
                      command=lambda: self.sine(self.value.get()))
        sine.place(relx=0.15, rely=0.5, relheight=0.1, relwidth=0.15)

        cosine = Button(self.tri_frame, text='Cosine', font=('arial', 12),
                        command=lambda: self.cos(self.value.get()))
        cosine.place(relx=0.37, rely=0.5, relheight=0.1, relwidth=0.2)

        tan = Button(self.tri_frame, text='Tangent', font=('arial', 12),
                     command=lambda: self.tan(self.value.get()))
        tan.place(relx=0.63, rely=0.5, relheight=0.1, relwidth=0.25)

        cosec = Button(self.tri_frame, text='Cosecant', font=('arial', 12),
                       command=lambda: self.cosec(self.value.get()))
        cosec.place(relx=0.1, rely=0.65, relheight=0.1, relwidth=0.225)

        sec = Button(self.tri_frame, text='Secant', font=('arial', 12),
                     command=lambda: self.sec(self.value.get()))
        sec.place(relx=0.37, rely=0.65, relheight=0.1, relwidth=0.2)

        cot = Button(self.tri_frame, text='Cotangent', font=('arial', 12),
                     command=lambda: self.cot(self.value.get()))
        cot.place(relx=0.63, rely=0.65, relheight=0.1, relwidth=0.25)

        return_but = Button(self.tri_frame, text='Back to Scientific\nCalculator', font=('arial', 10),
                            command=lambda: base_calc.sci_calc.scientific_calculator())
        return_but.place(relx=0.6, rely=0.83, relheight=0.15, relwidth=0.4)

    pass


class Currency:

    def __init__(self):
        global base_calc
        self.data = requests.get('https://api.exchangerate-api.com/v4/latest/USD').json()
        self.currencies = self.data['rates']
        
        
    def convert(self, from_val, to_val, value):
        initial_value = value
        if from_val != 'USD':
            value = value / self.currencies[from_val]

        value = round(value * self.currencies[to_val], 4)
        return value

    def screen(self):
        try:
            base_calc.sci_calc.frame.destroy()
        except AttributeError:
            pass

        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="CURRENCY CONVERTOR")
        title.place(relwidth=1, relheight=0.12)
        date = datetime.datetime.strptime(self.data['date'], '%Y-%m-%d')
        date = date.strftime("%d - %b, %Y")
        value = tk.Label(self.frame, text=f"Updated on : {date}", font=10, borderwidth=2, relief="groove")
        value.place(relx=0.15, rely=0.2, relheight=0.1, relwidth=0.7)
        def callback(*args):
            try:
                if self.from_value.get() == '00':
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0, '0')
                if not self.from_value.get()[-1].isnumeric():
                    i = len(self.from_value.get()) - 1
                    self.from_value.delete(i, tk.END)
                if self.from_value.get().startswith('0') and self.from_value.get() != '0':
                    val = self.from_value.get().replace('0', '')
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0,val)
                    self.perform()
                else:
                    self.perform()

            except IndexError:
                self.from_value.insert(0, "0")
                self.perform()

        self.text = tk.StringVar()

        self.from_value = tk.Entry(self.frame, font=('calibri', 15), textvariable=self.text)
        self.from_value.focus()
        self.from_value.insert(0, '0')

        self.converted_value_field_label = tk.Label(self.frame, text='', font=('calibri', 15), justify='center',
                                                     borderwidth=3)
        self.converted_value_field_label.config(text='0')

        self.from_value_dropdown = ttk.Combobox(self.frame, values=list(self.currencies.keys()), state='readonly',
                                                   width=15, justify=tk.CENTER)
        self.to_value_dropdown = ttk.Combobox(self.frame, values=list(self.currencies.keys()), state='readonly',
                                                 width=15, justify=tk.CENTER)

        self.text.trace_add("write", callback)

        self.from_value_dropdown.current(0)
        self.to_value_dropdown.current(list(self.currencies.keys()).index('INR'))

        self.from_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())
        self.to_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())

        tk.Label(self.frame, text='From:', bg="#80c1ff").place(relx=0.03, rely=0.32, relheight=0.03, relwidth=0.2)
        self.from_value.place(relx=0.1, rely=0.36, relheight=0.1, relwidth=0.8)
        self.from_value_dropdown.place(relx=0.1, rely=0.48, relheight=0.08)
        tk.Label(self.frame, text='To:', bg="#80c1ff").place(relx=0.03, rely=0.58, relheight=0.03, relwidth=0.2)
        self.converted_value_field_label.place(relx=0.1, rely=0.63, relheight=0.1, relwidth=0.8)
        self.to_value_dropdown.place(relx=0.1, rely=0.77, relheight=0.08)

    def perform(self):
        value = float(self.from_value.get())
        from_val = self.from_value_dropdown.get()
        to_val = self.to_value_dropdown.get()

        converted_value = self.convert(from_val, to_val, value)
        converted_value = round(converted_value, 5)
        converted_value = str(converted_value)
        if converted_value.endswith('.0'):
            converted_value = converted_value.replace('.0', '')
        self.converted_value_field_label.config(text=str(converted_value))

    pass


class Volume:

    def __init__(self):
        global base_calc


    def convert(self, from_unit, to_unit, value):
        if from_unit == "Milliliters":
            if to_unit == "Milliliters":
                converted_value = value

            elif to_unit == "Cubic centimeters":
                converted_value = value

            elif to_unit == "Liters":
                converted_value = value/1000

            elif to_unit == "Cubic meters":
                converted_value = value/1000000

            elif to_unit == "Gallons":
                converted_value = value/3785.412

        elif from_unit == "Cubic centimeters":
            if to_unit == "Milliliters":
                converted_value = value

            elif to_unit == "Cubic centimeters":
                converted_value = value

            elif to_unit == "Liters":
                converted_value = value/1000

            elif to_unit == "Cubic meters":
                converted_value = value/1000000

            elif to_unit == "Gallons":
                converted_value = value/3785.412

        elif from_unit == "Liters":
            if to_unit == "Milliliters":
                converted_value = value*1000

            elif to_unit == "Cubic centimeters":
                converted_value = value*1000

            elif to_unit == "Liters":
                converted_value = value

            elif to_unit == "Cubic meters":
                converted_value = value/1000

            elif to_unit == "Gallons":
                converted_value = value/3.785412

        elif from_unit == "Cubic meters":
            if to_unit == "Milliliters":
                converted_value = value*1000000

            elif to_unit == "Cubic centimeters":
                converted_value = value*1000000

            elif to_unit == "Liters":
                converted_value = value*1000

            elif to_unit == "Cubic meters":
                converted_value = value

            elif to_unit == "Gallons":
                converted_value = value*264.1721

        elif from_unit == "Gallons":
            if to_unit == "Milliliters":
                converted_value = value*3785.412

            elif to_unit == "Cubic centimeters":
                converted_value = value*3785.412

            elif to_unit == "Liters":
                converted_value = value*3.785412

            elif to_unit == "Cubic meters":
                converted_value = value/264.1721

            elif to_unit == "Gallons":
                converted_value = value
        
        return converted_value
    def screen(self):
        try:
            base_calc.sci_calc.frame.destroy()
        except AttributeError:
            pass

        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="VOLUME CONVERTOR")
        title.place(relwidth=1, relheight=0.12)

        def callback(*args):
            try:
                if self.from_value.get() == '00':
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0, '0')
                if not self.from_value.get()[-1].isnumeric():
                    i = len(self.from_value.get()) - 1
                    self.from_value.delete(i, tk.END)
                if self.from_value.get().startswith('0') and self.from_value.get() != '0':
                    val = self.from_value.get().replace('0', '')
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0,val)
                    self.perform()
                else:
                    self.perform()
            except IndexError:
                self.from_value.insert(0, "0")
                self.perform()

        self.text = tk.StringVar()

        self.from_value = tk.Entry(self.frame, font=('calibri', 15), textvariable=self.text)
        self.from_value.focus()

        self.converted_value_field_label = tk.Label(self.frame, text='', font=('calibri', 15), justify='center',
                                                     borderwidth=3)
        self.from_value.insert(0, '0')
        self.converted_value_field_label.config(text='0')

        lis = ['Milliliters', 'Cubic centimeters', 'Liters', 'Cubic meters', 'Gallons']

        self.from_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                   width=15, justify=tk.CENTER)
        self.to_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                 width=15, justify=tk.CENTER)

        self.text.trace_add("write", callback)

        self.from_value_dropdown.current(0)
        self.to_value_dropdown.current(0)

        self.from_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())
        self.to_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())

        tk.Label(self.frame, text='From:', bg="#80c1ff").place(relx=0.03, rely=0.18, relheight=0.03, relwidth=0.2)
        self.from_value.place(relx=0.1, rely=0.23, relheight=0.1, relwidth=0.8)
        self.from_value_dropdown.place(relx=0.1, rely=0.36, relheight=0.08)
        tk.Label(self.frame, text='To:', bg="#80c1ff").place(relx=0.03, rely=0.55, relheight=0.03, relwidth=0.2)
        self.converted_value_field_label.place(relx=0.1, rely=0.6, relheight=0.1, relwidth=0.8)
        self.to_value_dropdown.place(relx=0.1, rely=0.73, relheight=0.08)


    def perform(self):
            value = float(self.from_value.get())
            from_val = self.from_value_dropdown.get()
            to_val = self.to_value_dropdown.get()

            converted_value = self.convert(from_val, to_val, value)
            converted_value = round(converted_value, 5)
            converted_value = str(converted_value)
            if converted_value.endswith('.0'):
                converted_value = converted_value.replace('.0', '')
            self.converted_value_field_label.config(text=str(converted_value))

    pass


class Length:

    def __init__(self):
        global base_calc


    def convert(self, from_unit, to_unit, value):
        if from_unit == "Millimeters":
            if to_unit == "Millimeters":
                converted_value = value

            elif to_unit == "Centimeters":
                converted_value = value/10

            elif to_unit == "Meters":
                converted_value = value/1000

            elif to_unit == "Kilometers":
                converted_value = value/1000000

            elif to_unit == "Inches":
                converted_value = value/25.4

            elif to_unit == "Feet":
                converted_value = value/304.8

            elif to_unit == "Miles":
                converted_value = value/1609344

        elif from_unit == "Centimeters":
            if to_unit == "Millimeters":
                converted_value = value*10

            elif to_unit == "Centimeters":
                converted_value = value

            elif to_unit == "Meters":
                converted_value = value/100

            elif to_unit == "Kilometers":
                converted_value = value/100000

            elif to_unit == "Inches":
                converted_value = value/2.54

            elif to_unit == "Feet":
                converted_value = value/30.48

            elif to_unit == "Miles":
                converted_value = value/160934.4

        elif from_unit == "Meters":
            if to_unit == "Millimeters":
                converted_value = value*1000

            elif to_unit == "Centimeters":
                converted_value = value*100

            elif to_unit == "Meters":
                converted_value = value

            elif to_unit == "Kilometers":
                converted_value = value/1000

            elif to_unit == "Inches":
                converted_value = value*39.37008

            elif to_unit == "Feet":
                converted_value = value*3.28084

            elif to_unit == "Miles":
                converted_value = value/1609.344

        elif from_unit == "Kilometers":
            if to_unit == "Millimeters":
                converted_value = value-1000000

            elif to_unit == "Centimeters":
                converted_value = value*100000

            elif to_unit == "Meters":
                converted_value = value*1000

            elif to_unit == "Kilometers":
                converted_value = value

            elif to_unit == "Inches":
                converted_value = value*39370.08

            elif to_unit == "Feet":
                converted_value = value*3280.84

            elif to_unit == "Miles":
                converted_value = value/1.609344

        elif from_unit == "Inches":
            if to_unit == "Millimeters":
                converted_value = value*25.4

            elif to_unit == "Centimeters":
                converted_value = value*2.54

            elif to_unit == "Meters":
                converted_value = value/39.37008

            elif to_unit == "Kilometers":
                converted_value = value/39370.08

            elif to_unit == "Inches":
                converted_value = value

            elif to_unit == "Feet":
                converted_value = value/12

            elif to_unit == "Miles":
                converted_value = value/63360

        elif from_unit == "Feet":
            if to_unit == "Millimeters":
                converted_value = value*304.8

            elif to_unit == "Centimeters":
                converted_value = value*30.48

            elif to_unit == "Meters":
                converted_value = value/3.28084

            elif to_unit == "Kilometers":
                converted_value = value/3280.84

            elif to_unit == "Inches":
                converted_value = value*12

            elif to_unit == "Feet":
                converted_value = value

            elif to_unit == "Miles":
                converted_value = value/5280

        elif from_unit == "Miles":
            if to_unit == "Millimeters":
                converted_value = value*1609344

            elif to_unit == "Centimeters":
                converted_value = value*160934.4

            elif to_unit == "Meters":
                converted_value = value*1609.344

            elif to_unit == "Kilometers":
                converted_value = value*1.609344

            elif to_unit == "Inches":
                converted_value = value*63360

            elif to_unit == "Feet":
                converted_value = value*5280

            elif to_unit == "Miles":
                converted_value = value

        
        return converted_value
    def screen(self):
        try:
            base_calc.sci_calc.frame.destroy()
        except AttributeError:
            pass

        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="LENGTH CONVERTOR")
        title.place(relwidth=1, relheight=0.12)


        def callback(*args):
            try:
                if self.from_value.get() == '00':
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0, '0')
                if not self.from_value.get()[-1].isnumeric():
                    i = len(self.from_value.get()) - 1
                    self.from_value.delete(i, tk.END)
                if self.from_value.get().startswith('0') and self.from_value.get() != '0':
                    val = self.from_value.get().replace('0', '')
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0,val)
                    self.perform()
                else:
                    self.perform()
            except IndexError:
                self.from_value.insert(0, "0")
                self.perform()

        self.text = tk.StringVar()

        self.from_value = tk.Entry(self.frame, font=('calibri', 15), textvariable=self.text)
        self.from_value.focus()

        self.converted_value_field_label = tk.Label(self.frame, text='', font=('calibri', 15), justify='center',
                                                     borderwidth=3)
        
        self.from_value.insert(0, '0')
        self.converted_value_field_label.config(text='0')

        lis = ['Millimeters', 'Centimeters', 'Meters', 'Kilometers', 'Inches', 'Feet', 'Miles']

        self.from_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                   width=15, justify=tk.CENTER)
        self.to_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                 width=15, justify=tk.CENTER)

        self.text.trace_add("write", callback)

        self.from_value_dropdown.current(0)
        self.to_value_dropdown.current(0)

        self.from_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())
        self.to_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())

        tk.Label(self.frame, text='From:', bg="#80c1ff").place(relx=0.03, rely=0.18, relheight=0.03, relwidth=0.2)
        self.from_value.place(relx=0.1, rely=0.23, relheight=0.1, relwidth=0.8)
        self.from_value_dropdown.place(relx=0.1, rely=0.36, relheight=0.08)
        tk.Label(self.frame, text='To:', bg="#80c1ff").place(relx=0.03, rely=0.55, relheight=0.03, relwidth=0.2)
        self.converted_value_field_label.place(relx=0.1, rely=0.6, relheight=0.1, relwidth=0.8)
        self.to_value_dropdown.place(relx=0.1, rely=0.73, relheight=0.08)

    def perform(self):
            value = float(self.from_value.get())
            from_val = self.from_value_dropdown.get()
            to_val = self.to_value_dropdown.get()

            converted_value = self.convert(from_val, to_val, value)
            converted_value = round(converted_value, 5)
            converted_value = str(converted_value)
            if converted_value.endswith('.0'):
                converted_value = converted_value.replace('.0', '')
            self.converted_value_field_label.config(text=str(converted_value))

    pass


class Weight:

    def __init__(self):
        global base_calc


    def convert(self, from_unit, to_unit, value):
        if from_unit == "Milligrams":
            if to_unit == "Milligrams":
                converted_value = value

            elif to_unit == "Kilograms":
                converted_value = value/1000000

            elif to_unit == "Grams":
                converted_value = value/1000

            elif to_unit == "Metric Tonnes":
                converted_value = value/1000000000

            elif to_unit == "Pounds":
                converted_value = value/453592.4
                
        elif from_unit == "Kilograms":
            if to_unit == "Milligrams":
                converted_value = value*1000000

            elif to_unit == "Kilograms":
                converted_value = value

            elif to_unit == "Grams":
                converted_value = value*1000

            elif to_unit == "Metric Tonnes":
                converted_value = value/1000

            elif to_unit == "Pounds":
                converted_value = value*2.204623

        elif from_unit == "Grams":
            if to_unit == "Milligrams":
                converted_value = value*1000

            elif to_unit == "Kilograms":
                converted_value = value/1000

            elif to_unit == "Grams":
                converted_value = value

            elif to_unit == "Metric Tonnes":
                converted_value = value/1000000

            elif to_unit == "Pounds":
                converted_value = value/453.5924

        elif from_unit == "Pounds":
            if to_unit == "Milligrams":
                converted_value = value*453592.4

            elif to_unit == "Kilograms":
                converted_value = value/2.204623

            elif to_unit == "Grams":
                converted_value = value*453.5924

            elif to_unit == "Metric Tonnes":
                converted_value = value/2204.623

            elif to_unit == "Pounds":
                converted_value = value

        elif from_unit == "Metric Tonnes":
            if to_unit == "Milligrams":
                converted_value = value*1000000000

            elif to_unit == "Kilograms":
                converted_value = value/1000

            elif to_unit == "Grams":
                converted_value = value/1000000

            elif to_unit == "Metric Tonnes":
                converted_value = value

            elif to_unit == "Pounds":
                converted_value = value*2204.623

        return converted_value
    def screen(self):
        try:
            base_calc.sci_calc.frame.destroy()
        except AttributeError:
            pass

        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="WEIGHT CONVERTOR")
        title.place(relwidth=1, relheight=0.12)


        def callback(*args):
            try:
                if self.from_value.get() == '00':
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0, '0')
                if not self.from_value.get()[-1].isnumeric():
                    i = len(self.from_value.get()) - 1
                    self.from_value.delete(i, tk.END)
                if self.from_value.get().startswith('0'):
                    val = self.from_value.get().replace('0', '')
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0,val)
                    self.perform()
                else:
                    self.perform()
            except IndexError:
                self.from_value.insert(0, "0")
                self.perform()

        self.text = tk.StringVar()

        lis = ['Milligrams', 'Grams', 'Kilograms', 'Metric Tonnes', 'Pounds']

        self.from_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                   width=15, justify=tk.CENTER)
        self.to_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                 width=15, justify=tk.CENTER)
        self.from_value = tk.Entry(self.frame, font=('calibri', 15), textvariable=self.text)
        self.converted_value_field_label = tk.Label(self.frame, text='', font=('calibri', 15), borderwidth=3)
        self.from_value.insert(0, '0')
        self.converted_value_field_label.config(text='0')

        tk.Label(self.frame, text='From:', bg="#80c1ff").place(relx=0.03, rely=0.18, relheight=0.03, relwidth=0.2)
        self.from_value.place(relx=0.1, rely=0.23, relheight=0.1, relwidth=0.8)
        self.from_value_dropdown.place(relx=0.1, rely=0.36, relheight=0.08)
        tk.Label(self.frame, text='To:', bg="#80c1ff").place(relx=0.03, rely=0.55, relheight=0.03, relwidth=0.2)
        self.converted_value_field_label.place(relx=0.1, rely=0.6, relheight=0.1, relwidth=0.8)
        self.to_value_dropdown.place(relx=0.1, rely=0.73, relheight=0.08)

        self.text.trace_add("write", callback)

        self.from_value_dropdown.current(0)
        self.to_value_dropdown.current(0)
        self.from_value.focus()
        self.from_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())
        self.to_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())

    def perform(self):
            value = float(self.from_value.get())
            from_val = self.from_value_dropdown.get()
            to_val = self.to_value_dropdown.get()

            converted_value = self.convert(from_val, to_val, value)
            converted_value = round(converted_value, 5)
            converted_value = str(converted_value)
            if converted_value.endswith('.0'):
                converted_value = converted_value.replace('.0', '')
            self.converted_value_field_label.config(text=str(converted_value))

    pass


class Speed:

    def __init__(self):
        global base_calc


    def convert(self, from_unit, to_unit, value):
        if from_unit == "Miles per hour":
            if to_unit == "Miles per hour":
                converted_value = value

            elif to_unit == "Kilometers per hour":
                converted_value = value*1.6092

            elif to_unit == "Meters per second":
                converted_value = value/2.237

            elif to_unit == "Feet per second":
                converted_value = value*1.467

            elif to_unit == "Knots":
                converted_value = value/1.151
                
        elif from_unit == "Kilometers per hour":
            if to_unit == "Miles per hour":
                converted_value = value/1.609

            elif to_unit == "Kilometers per hour":
                converted_value = value

            elif to_unit == "Meters per second":
                converted_value = value/3.6

            elif to_unit == "Feet per second":
                converted_value = value/1.097

            elif to_unit == "Knots":
                converted_value = value/1.852

        elif from_unit == "Feet per second":
            if to_unit == "Miles per hour":
                converted_value = value/1.467

            elif to_unit == "Kilometers per hour":
                converted_value = value*1.097

            elif to_unit == "Meters per second":
                converted_value = value/3.281

            elif to_unit == "Feet per second":
                converted_value = value

            elif to_unit == "Knots":
                converted_value = value/1.688

        elif from_unit == "Meters per second":
            if to_unit == "Miles per hour":
                converted_value = value*2.237

            elif to_unit == "Kilometers per hour":
                converted_value = value*3.6

            elif to_unit == "Meters per second":
                converted_value = value

            elif to_unit == "Feet per second":
                converted_value = value*3.281

            elif to_unit == "Knots":
                converted_value = value*1.944

        elif from_unit == "Knots":
            if to_unit == "Miles per hour":
                converted_value = value*1.151

            elif to_unit == "Kilometers per hour":
                converted_value = value*1.852

            elif to_unit == "Meters per second":
                converted_value = value/1.944

            elif to_unit == "Feet per second":
                converted_value = value*1.688

            elif to_unit == "Knots":
                converted_value = value  

        return converted_value
    def screen(self):
        try:
            base_calc.sci_calc.frame.destroy()
        except AttributeError:
            pass

        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="SPEED CONVERTOR")
        title.place(relwidth=1, relheight=0.12)


        def callback(*args):
            try:
                if self.from_value.get() == '00':
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0, '0')
                if not self.from_value.get()[-1].isnumeric():
                    i = len(self.from_value.get()) - 1
                    self.from_value.delete(i, tk.END)
                if self.from_value.get().startswith('0'):
                    val = self.from_value.get().replace('0', '')
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0,val)
                    self.perform()
                else:
                    self.perform()
            except IndexError:
                self.from_value.insert(0, "0")
                self.perform()

        self.text = tk.StringVar()

        lis = ['Miles per hour', 'Feet per second', 'Meters per second', 'Kilometers per hour', 'Knots']

        self.from_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                   width=20, justify=tk.CENTER)
        self.to_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                 width=20, justify=tk.CENTER)
        self.from_value = tk.Entry(self.frame, font=('calibri', 15), textvariable=self.text)
        self.converted_value_field_label = tk.Label(self.frame, text='', font=('calibri', 15), borderwidth=3)
        self.from_value.insert(0, '0')
        self.converted_value_field_label.config(text='0')

        tk.Label(self.frame, text='From:', bg="#80c1ff").place(relx=0.03, rely=0.18, relheight=0.03, relwidth=0.2)
        self.from_value.place(relx=0.1, rely=0.23, relheight=0.1, relwidth=0.8)
        self.from_value_dropdown.place(relx=0.1, rely=0.36, relheight=0.08)
        tk.Label(self.frame, text='To:', bg="#80c1ff").place(relx=0.03, rely=0.55, relheight=0.03, relwidth=0.2)
        self.converted_value_field_label.place(relx=0.1, rely=0.6, relheight=0.1, relwidth=0.8)
        self.to_value_dropdown.place(relx=0.1, rely=0.73, relheight=0.08)

        self.text.trace_add("write", callback)

        self.from_value_dropdown.current(0)
        self.to_value_dropdown.current(0)
        self.from_value.focus()
        self.from_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())
        self.to_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())

    def perform(self):
            value = float(self.from_value.get())
            from_val = self.from_value_dropdown.get()
            to_val = self.to_value_dropdown.get()

            converted_value = self.convert(from_val, to_val, value)
            converted_value = round(converted_value, 5)
            converted_value = str(converted_value)
            if converted_value.endswith('.0'):
                converted_value = converted_value.replace('.0', '')
            self.converted_value_field_label.config(text=str(converted_value))

    pass


class Temperature:

    def __init__(self):
        global base_calc


    def convert(self, from_unit, to_unit, value):
        if from_unit == "Celsius":
            if to_unit == "Celsius":
                converted_value = value

            elif to_unit == "Fahrenheit":
                converted_value = (value*9/5) + 32

            elif to_unit == "Kelvin":
                converted_value = value + 273.15

        elif from_unit == "Fahrenheit":
            if to_unit == "Celsius":
                converted_value = (value - 32) * 5/9

            elif to_unit == "Fahrenheit":
                converted_value = value

            elif to_unit == "Kelvin":
                converted_value = (value - 32) * 5/9 + 273.15

        elif from_unit == "Kelvin":
            if to_unit == "Celsius":
                converted_value = value - 273.15

            elif to_unit == "Fahrenheit":
                converted_value = (value - 273.15) * 9/5 + 32

            elif to_unit == "Kelvin":
                converted_value = value

        return converted_value
    def screen(self):
        try:
            base_calc.sci_calc.frame.destroy()
        except AttributeError:
            pass

        self.frame = tk.Frame(root, bg="#80c1ff", bd=7)
        self.frame.place(relx=0.5, rely=0.001, relwidth=1, relheight=1, anchor='n')

        title = tk.Label(self.frame, bg="light green", font=('bold', 15), text="TEMPERATURE CONVERTOR")
        title.place(relwidth=1, relheight=0.12)


        def callback(*args):
            try:
                if self.from_value.get() == '00':
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0, '0')
                if not self.from_value.get()[-1].isnumeric():
                    i = len(self.from_value.get()) - 1
                    self.from_value.delete(i, tk.END)
                if self.from_value.get().startswith('0'):
                    val = self.from_value.get().replace('0', '')
                    self.from_value.delete(0, tk.END)
                    self.from_value.insert(0,val)
                    self.perform()
                else:
                    self.perform()
            except IndexError:
                
                self.from_value.insert(0, "0")
                self.perform()

        self.text = tk.StringVar()

        lis = ['Celsius', 'Fahrenheit', 'Kelvin']

        self.from_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                   width=15, justify=tk.CENTER)
        self.to_value_dropdown = ttk.Combobox(self.frame, values=lis, state='readonly',
                                                 width=15, justify=tk.CENTER)
        self.from_value = tk.Entry(self.frame, font=('calibri', 15), textvariable=self.text)
        self.converted_value_field_label = tk.Label(self.frame, text='', font=('calibri', 15), borderwidth=3)
        self.from_value.insert(0, '0')
        self.converted_value_field_label.config(text='0')

        tk.Label(self.frame, text='From:', bg="#80c1ff").place(relx=0.03, rely=0.18, relheight=0.03, relwidth=0.2)
        self.from_value.place(relx=0.1, rely=0.23, relheight=0.1, relwidth=0.8)
        self.from_value_dropdown.place(relx=0.1, rely=0.36, relheight=0.08)
        tk.Label(self.frame, text='To:', bg="#80c1ff").place(relx=0.03, rely=0.55, relheight=0.03, relwidth=0.2)
        self.converted_value_field_label.place(relx=0.1, rely=0.6, relheight=0.1, relwidth=0.8)
        self.to_value_dropdown.place(relx=0.1, rely=0.73, relheight=0.08)

        self.text.trace_add("write", callback)

        self.from_value_dropdown.current(0)
        self.to_value_dropdown.current(0)
        self.from_value.focus()
        self.from_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())
        self.to_value_dropdown.bind("<<ComboboxSelected>>", lambda e: self.perform())

    def perform(self):
            value = float(self.from_value.get())
            from_val = self.from_value_dropdown.get()
            to_val = self.to_value_dropdown.get()

            converted_value = self.convert(from_val, to_val, value)
            converted_value = round(converted_value, 5)
            converted_value = str(converted_value)
            if converted_value.endswith('.0'):
                converted_value = converted_value.replace('.0', '')
            self.converted_value_field_label.config(text=str(converted_value))


    pass


def run(master):
    global base_calc, root
    root = master
    base_calc = Base_Calc()
    menu = Add_menu_bar()
    base_calc.base_calculator()

