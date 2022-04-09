n = int(input())
s = [input().strip() for i in range(n)]
dic = {}

for i in range(-1, n-1):
    dic[i+1] = [0]
    for j in range(len(s[i+1])):
        if s[i][-1] == s[i+1][j]:
            dic[i+1] = [j]
for i in range(0, n):
    a = len(s[i-1])
    for j in range(len(s[i-1])-1, -1, -1):
        if s[i][0] == s[i-1][j]:
            a = j
    try:
        dic[i-1].append(a)
    except KeyError:
        dic[n-1].append(a)
for i in dic:
    print(dic[i])
    print(s[i][dic[i][0]:dic[i][1]+1])