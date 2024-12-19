from functools import cache
T,D=open("input.txt").read().split("\n\n")
T,D=T.split(", "),D.split("\n")
@cache
def f(x):return 1 if x=="" else sum([f(x[len(t):]) for t in T if x.startswith(t)]) 
print(tuple(map(sum,zip(*[((n:=f(d))>0,n) for d in D]))))

# Note:
# x.startswith(t) is 2 chars longer than x[:len(t)]==t, but it is also ~3x faster 
