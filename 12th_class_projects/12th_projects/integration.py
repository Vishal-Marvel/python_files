import math

def integrate(exm, up_li, lo_li, var):
    l = []
    s, result = '', ''
    if var == '':
        var = 'x'
    for i in ex:
        if i in "+-":
            l.append(s)
            l.append(i)
            s = ''
        else:
            s += i
    if len(l) == 0:
        l.append(s)
    if (l[-1] != ex):
        l.append(ex.split(l[-1])[-1])
    for index, i in enumerate(l):
        if var in i:
            if '^' in i:
                l.remove(i)
                s = i.split(var)[0] if (not i.startswith(var)) else ''
                n = int(i.split('^')[-1])
                n += 1
                n = str(n)
                i = f'{s}({var}^{n})/{n}'
                l.insert(index, i)
                
            elif var == i:
                l.remove(i)
                n = 2
                i = f'({var}^{n})/{n}'
                l.insert(index, i)
            
            elif var in i:
                l.remove(i)
                s = i.split(var)[0]
                n = 2
                i = f'{s}({var}^{n})/{n}'
                l.insert(index, i)
            
        elif i not in '+-' and int(i):
            l.remove(i)
            i = f'{i}*{var}'
            l.insert(index, i)

    for i in l:
        result += i
    print(result)
    if up_li != '' and lo_li != '':
        result = f'({result.replace(var, up_li)})-({result.replace(var, lo_li)})'
        print(result, round(eval(result), 2), sep=' = ')


var = input("Enter the variable (default is 'x'): ")
print("Enter only integer!!")
up_li, lo_li = input("upper limit (if not press enter): "), input("lower limit (if not press enter): ")
ex = input("Enter an expression to integrate: ")
integrate(ex, up_li, lo_li, var)