# num = int(input("Enter a Number: "))
# # if (num==0):
# # 	fact = 1
# fact = 1
# for i in range(1,num+1):
# 	fact = fact * i
# print("Factorial of ", num, " is ", fact)

def fact(n):
	if n == 0:
		return 1
	elif n == 1:
		return n
	else:
		return n*fact(n-1)

num = int(input("Enter a number: "))
print(f'Factorial of {num} is {fact(num)}')