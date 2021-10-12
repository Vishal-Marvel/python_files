# def lcm(x,y):
#     if x>y:
#         greater = x
#     else:
#         greater = y
#     while True:
#         if greater %x == 0 and greater % y == 0:
#             lcm = greater
#             break
#         greater += 1
#     return lcm

def lcm(args):
    
    args = list(args)
    gr = max(args)
    
    checker = 1 
    while checker == 1:
        l = []
        for i in args:
            
            if not gr % i == 0:
                gr += 1
            else:
                l.append(i)
                if l == args:
                    checker = 0
                    return gr

li = []
num = int(input("Enter number of numbers you want to enter:"))
for i in range(num):
    li.append(int(input("Enter number:")))
print(f"The LCM of {li} is {lcm(li)}")