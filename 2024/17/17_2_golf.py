import itertools
import re
from common import run_program
_,b,c,*p=map(int,re.findall(r"(\d+)",open("input.txt").read()))
N=len(p)
Y=[list(range(1 if i==0 else 0,8)) for i in range(N)]
for k in range(N):
    C=[]
    for X in itertools.product(*Y[:k+1]):
        a=sum([x*8**(N-1-i) for i,x in enumerate(X)])
        if p[-k-1:]!=run_program(a,b,c,p)[-k-1:]:
            continue
        if k==N-1:
            print(a)
            break
        else:
            C.append(X)
    for i in range(k+1):
        Y[i]=sorted(list(set([X[i] for X in C])))
