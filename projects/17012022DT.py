s1=input().strip()
s2=input().strip()
s3=input().strip() 
s4=input().strip()
c=max(len(s1),len(s3))+max(len(s2),len(s4))
r=max(len(s1),len(s2))+max(len(s3),len(s4))
l=[['*']*c for i in range(r)] 
m=max(len(s1),len(s2))-1
n=max(len(s1),len(s3))-1
x,y=m,n 
ind=0
# print(l)
while ind<len(s1):
    l[x][y]=s1[ind]
    ind+=1 
    x-=1 
    y-=1
x,y=m,n+1 
ind=0

while ind<len(s2):
    l[x][y]=s2[ind] 
    ind+=1 
    x-=1
    y+=1
x,y=m+1,n 
ind=0
while ind<len(s3):
    l[x][y]=s3[ind] 
    ind+=1 
    x+=1 
    y-=1 
x,y=m+1,n+1 
ind=0 
while ind<len(s4):
    l[x][y] = s4[ind] 
    ind+=1 
    x+=1 
    y+=1 
for i in l:
    print(*i,sep="")