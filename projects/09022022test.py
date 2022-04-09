s = input().strip()
st=''
l = s.split('_')
for i in range(1, len(l)-1):
    st += l[i][::-1]
    st += '_' if l[i] != '' else ''

print(l[0] + '_' + st + l[len(l)-1])