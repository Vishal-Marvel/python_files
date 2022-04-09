s = 'aaabbccc'
n = []
for i in s:
    if i not in n:
        n.append(i)
n.sort(reverse=True)
max_count = 0
for i in n:
    count=0
    for j in s:
        if i==j:
            count += 1
    if  count > max_count:
        max_count = count

l = []

for i in range(max_count):
    st = ''
    for i in n:
        if i in s:
            s = s.replace(i, "", 1)
            st += '1'
        else:
            st += '0'
    l.append(st)
for index,i in enumerate(l):
    l[index] = int(i,2)

print(l)