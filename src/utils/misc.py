from datetime import datetime
from functools import reduce

def raze(l):
    return reduce(lambda x,y: x+y,l)
    
def get_timestamp():
    return 'D'+datetime.now().strftime('%Y-%m-%dT%H.%M.%S.%f')

def are_lists_same_size(*l):
    return 1==len(set(map(len,l)))

def get_n_elements(ele,n):
    if isinstance(ele,list): return raze([ele for i in range(n)])
    return [ele for i in range(n)]

def get_where_index(arr,func=None,tt=None):
    truth_table=tt if bool(tt) else list(map(func,arr))
    return list(filter(lambda x: truth_table[x],range(len(truth_table))))

def get_where(arr,func=None,tt=None):
    where_true=get_where_index(arr,func=func,tt=tt)
    return list(map(lambda x: arr[x],where_true))