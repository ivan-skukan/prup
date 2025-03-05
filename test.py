def tricky(lst):
    return lst[:-1] and lst[:-2] if len(lst[1]) == len(lst[-1]) else lst[1:]


names = ['Ben','Ken','Len']
print(names[:-1] and names[-1])
print(tricky(names))