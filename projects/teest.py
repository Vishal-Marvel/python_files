n = int(input())
m1 = [[0]*n]*n
for i in range(n):
    m1[i] = list(map(int, input().split()))
x = int(input())
m2 = [[0]*x]*x
for i in range(x):
    m2[i] = list(map(int, input().split()))
m = []
for i in m1:
    for k in range(x//n):
        for j in i:
        
            for l in range(x//n):
                m.append(j)
m_index=0
for i in m2:
    for j in i:
        if (j!=m[m_index]):break
        else:m_index+=1

print('Yes' if m_index==len(m) else 'No')