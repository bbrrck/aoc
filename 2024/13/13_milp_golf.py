import re
import numpy as np
from scipy.optimize import Bounds as B,LinearConstraint as C,milp
print([int(sum([f.fun if(f:=milp(c=[3,1],constraints=C((x:=np.array(list(map(int,m))))[:4].reshape(2,2).transpose(),x[4:]+d-.1,x[4:]+d+.1),integrality=[1,1],bounds=B(0,u))).success else 0 for m in re.findall(r"(\d+)[^\d]*"*6,open("input.txt").read())]))for d,u in zip([0,1e13],[100,np.inf])])