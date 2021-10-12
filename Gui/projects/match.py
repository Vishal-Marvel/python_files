from tkinter import *
import random
from tkinter import messagebox

root = Tk()
root.title("Match Game!")
root.geometry("430x400")

winner = 0

# Create our matches
matches = [1,1,2,2,3,3,4,4,5,5,6,6]
random.shuffle(matches)

my_frame = Frame(root)
my_frame.pack(pady=10)

count = 0
answer_list = []
answer_dict = {}

def reset():
	global matches, winner
	winner = 0
	matches = [1,1,2,2,3,3,4,4,5,5,6,6]
	random.shuffle(matches)
	button_list = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11]
	my_label.config(text="")
	for b in button_list:
		b.config(bg="SystemButtonFace", text=" ", state="normal")

def win():
	global matches, winner
	winner = 0
	button_list = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11]
	for b in button_list:
		b.config(bg="yellow")
	message = messagebox.askyesnocancel("Game Over", "Congratulations you won\nDo you want to start the game again")
	if message:
		reset()
	else:
		root.quit()

def button_click(b, number):
	global count,answer_dict, answer_list, winner

	if b["text"] == " " and count < 2:
		b["text"] = matches[number]
		answer_list.append(number)
		answer_dict[b] = matches[number]

		count += 1
	# Determine matched
	if len(answer_list) == 2:
		if matches[answer_list[0]] == matches[answer_list[1]]:
			my_label.config(text="MATCH!")
			for key in answer_dict:
				key["state"] = "disabled"
			count=0
			answer_list=[]
			answer_dict={}
			winner += 1
			if winner == 6:
				win()

		else:
			my_label.config(text=" ")
			count=0
			answer_list = []

			messagebox.showinfo("Incorrect!", "Incorrect")
			for key in answer_dict:
				key["text"] = " "

			answer_dict = {}


# Define our buttons
b0 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b0, 0), relief="groove")
b1 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b1, 1), relief="groove")
b2 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b2, 2), relief="groove")
b3 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b3, 3), relief="groove")

b4 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b4, 4), relief="groove")
b5 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b5, 5), relief="groove")
b6 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b6, 6), relief="groove")
b7 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b7, 7), relief="groove")

b8 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b8, 8), relief="groove")
b9 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b9, 9), relief="groove")
b10 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b10, 10), relief="groove")
b11 = Button(my_frame, text=' ', bd=2, font=30, height=5, width=9, command=lambda: button_click(b11, 11), relief="groove")

b0.grid(row=0, column=0)
b1.grid(row=0, column=1)
b2.grid(row=0, column=2)
b3.grid(row=0, column=3)

b4.grid(row=1, column=0)
b5.grid(row=1, column=1)
b6.grid(row=1, column=2)
b7.grid(row=1, column=3)

b8.grid(row=2, column=0)
b9.grid(row=2, column=1)
b10.grid(row=2, column=2)
b11.grid(row=2, column=3)

my_label = Label(root, text="")
my_label.pack(pady=10)

my_menu = Menu(root)
root.config(menu=my_menu)

options_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Reset Game", command=reset)
options_menu.add_separator()
options_menu.add_command(label="Exit", command=root.quit)

root.mainloop()