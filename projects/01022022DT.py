import time

n = int(input())
l = list(map(int, input().split()))
start = time.time()
li = [l[0]]
ctr=0
for i in l[1:]:
    if n%2!=0 and ctr==0:
        li.append(i)
        ctr=1
    elif n%2!=0 and ctr==1:
        li = [i] + li
        ctr=0
    elif n%2==0 and ctr==0:
        li = [i] + li
        ctr=1
    elif n%2==0 and ctr==1:
        li.append(i)
        ctr=0
# li = []
# for i in l:
#     li.append(i)
#     li = li[::-1]
end = time.time()
print()
print(*li)
print('\n')
print(end-start)
