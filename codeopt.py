import re
file = input("Enter file name: ")
code = open(file,'r')
l = code.readlines()

op = ['+','-','*','/','%','^']

def removeWhiteSpaces():
    for i in range(0,len(l)):
        l[i] = l[i].rstrip()

def removeUnreachableCode():
    seek = 0
    while(seek!=len(l)-1):
        for i in range(seek,len(l)):
            if re.match('^return',l[i]):
                k = i
                break

        i = k+1
        while(l[i]!='}'):
            #print(l[i])
            del l[i]
        seek=i

def removeUnusedVariables():
    declarativeStatements = []
    deadVariables = []
    printStatements = []
    assi = []
    assi2 = []
    non_assi = ['if','while','for','elif']
    for x in l:
        if(re.match('int|char|float',x) and 'main' not in x):
            declarativeStatements.append(x)

    for x in declarativeStatements:
        x1=x.replace(';','')
        v=x1.split()[1]
        v=v.split(',')
        for a in v:
            deadVariables.append(a)

    for line in l:
        if('print' in line):
            printStatements.append(line)
        if('=' in line and 'if' not in line and 'else' not in line and 'for' not in line and 'while' not in line):
            assi.append(line)
            assi2.append(line)

    for x in printStatements:
        tmprmv=[]
        if('",' in x):
            m = x.index('",')
            while(m!=len(x)-1):
                for v in deadVariables:
                    if(v==x[m]):
                        tmprmv.append(v)
                m+=1

        if('("' not in x):
            m = x.index('(')
            while(m!=len(x)-1):
                for v in deadVariables:
                    if(v==x[m]):
                        tmprmv.append(v)
                m+=1

        for v in tmprmv:
            if v in deadVariables:
                deadVariables.remove(v)

    i=0
    while(i!=len(assi)):
        x=assi[i]
        m=x.index('=')
        if(str(x[m+1:-1]).isdigit()):
            assi.remove(x)
        else:
            i+=1

    i=0
    while(i!=len(assi)):
        tmprmv=[]
        x=assi[i]
        m=x.index('=')
        while(m!=len(x)-1):
            for v in deadVariables:
                if(v==x[m]):
                    tmprmv.append(v)
            m+=1
        i+=1
        for v in tmprmv:
            if v in deadVariables:
                deadVariables.remove(v)

    for x in declarativeStatements:
        for v in deadVariables:
            if v in x:
                x1=x.replace(','+v,'')
                x1=x1.replace(v+',','')
                for line in l:
                    if(x==line):
                        m=l.index(line)
                        l[m]=x1

    for x in assi:
        for y in assi2:
            if(x==y):
                assi2.remove(x)

    for v in deadVariables:
        for x in assi2:
            if(v in x):
                l.remove(x)

print('ORIGINAL CODE'.center(50,'*'))
print()
for x in l:
    print(x,end='')
removeWhiteSpaces()
removeUnreachableCode()
removeUnusedVariables()
print('\n')
print('OPTIMIZED CODE'.center(50,'*'))
print()
for x in l:
    print(x)
code.close()
