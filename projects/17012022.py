a1 = list(map(int, input().split()))
a2 = list(map(int, input().split()))
l1 = []
l2 = []
for i in a1:
    while(i>0):
        l1.append(i%10)
        i //=10

for i in a2:
    while(i>0):
        l2.append(i%10)
        i //=10

l1.sort()
l2.sort()
print(l1, l2)
if l1 == l2 and len(a1) == len(a2):
    print("Yes")
    print(sum(a1), sum(a2))
else:
    print("NO")