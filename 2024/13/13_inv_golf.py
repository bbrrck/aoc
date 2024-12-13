import re
import numpy as np
print([int(sum([np.dot([3,1],np.round(y))if np.abs((y:=np.linalg.solve((x:=np.array(list(map(int,m))))[:4].reshape(2,2).transpose(),x[4:]+d))-np.round(y)).sum()<.01 else 0 for m in re.findall(r"(\d+)[^\d]*"*6,open("input.txt").read())]))for d in[0,1e13]])