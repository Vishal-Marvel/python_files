n = 3
s = ['pqjhello', 'uehee', 'abshonest']
while 1:
    h = s[0][0]
    flag =1
    for i in s:
        if i[0] != h:
            flag=0
    if flag:break
    else:
        s = [j[1:] for j in s]
    print(s)
print(s)