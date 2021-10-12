# # Python program to draw star
# # using Turtle Programming
# import turtle

# star = turtle.Turtle()

# for i in range(50):
# 	star.forward(50)
# 	star.right(144)
	
# turtle.done()
# Python program to draw
# Spiral Square Outside In and Inside Out
# using Turtle Programming
# import turtle #Outside_In
# wn = turtle.Screen()
# wn.bgcolor("light green")
# wn.title("Turtle")
# skk = turtle.Turtle()
# skk.color("blue")

# def sqrfunc(size):
# 	for i in range(4):
# 		skk.fd(size)
# 		skk.left(90)
# 		size = size-5

# sqrfunc(146)
# sqrfunc(126)
# sqrfunc(106)
# sqrfunc(86)
# sqrfunc(66)
# sqrfunc(46)
# sqrfunc(26)
# import turtle #Inside_Out
# wn = turtle.Screen()
# wn.bgcolor("light green")
# skk = turtle.Turtle()
# skk.color("blue")

# def sqrfunc(size):
# 	for i in range(4):
# 		skk.fd(size)
# 		skk.left(90)
# 		size = size + 5

# sqrfunc(6)
# sqrfunc(26)
# sqrfunc(46)
# sqrfunc(66)
# sqrfunc(86)
# sqrfunc(106)
# sqrfunc(126)
# sqrfunc(146)
# Python program to user input pattern
# using Turtle Programming
# import turtle #Outside_In
# import turtle
# import time
# import random

# print ("This program draws shapes based on the number you enter in a uniform pattern.")
# num_str = input("Enter the side number of the shape you want to draw: ")
# if num_str.isdigit():
# 	squares = int(num_str)

# angle = 180 - 180*(squares-2)/squares

# turtle.up

# x = 0
# y = 0
# turtle.setpos(x, y)


# numshapes = 8
# for x in range(numshapes):
# 	turtle.color(random.random(), random.random(), random.random())
# 	x += 5
# 	y += 5
# 	turtle.forward(x)
# 	turtle.left(y)
# 	for i in range(squares):
# 		turtle.begin_fill()
# 		turtle.down()
# 		turtle.forward(40)
# 		turtle.left(angle)
# 		turtle.forward(40)
# 		print (turtle.pos())
# 		turtle.up()
# 		turtle.end_fill()

# time.sleep(11)
# turtle.bye()
# Python program to draw
# Spiral Helix Pattern
# using Turtle Programming

# import turtle
# loadWindow = turtle.Screen()
# turtle.speed(2)

# for i in range(100):
# 	turtle.circle(5*i)
# 	turtle.circle(-5*i)
# 	turtle.left(i)

# turtle.exitonclick()
# Python program to draw
# Rainbow Benzene
# using Turtle Programming
# import turtle
# colors = ['red', 'purple', 'blue', 'green', 'orange', 'yellow']
# t = turtle.Pen()
# turtle.bgcolor('black')
# for x in range(360):
# 	t.pencolor(colors[x%6])
# 	t.width(x/100 + 1)
# 	t.forward(x)
# 	t.left(59)

