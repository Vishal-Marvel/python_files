from Gui_Calc_Functions import run
import tkinter as tk
import tkinter.tix as tix


root = tix.Tk()
root.title("Python Calculator")
root.geometry("350x350")
# file_name = sys._MEIPASS + "\calculator.ico"
# root.wm_iconbitmap(file_name)
# root.wm_iconbitmap("Images/calculator.ico")
# canvas = tk.Canvas(root, height=350, width=350, bg='light green')
# canvas.resizable(height=False, width=False)
root.resizable(height=False, width=False)
root.focus_force()
# canvas.pack()

if __name__ == '__main__':
    run(root)

root.mainloop()
