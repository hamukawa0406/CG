import numpy as np
import csv

class temp():
    def __init__(self,):
        self.ret = np.matrix([[1, 3, 4], [3, 6, 7]])
        self.axis1 = np.array([0, 0, 0])
        self.axis2 = np.array([0, 0, 0])
    
def func(cA, axis_):
    axis = np.dot(cA.axis1, axis_)
    print(axis)

def asdf():
    global c1
    func(c1, c1.axis2)

c1 = temp()
print(c1.ret)
def main():
    asdf()
    sList = []
    with open('sphPt.csv', 'r') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            if not len(row):
                pass
            else:
                ar = np.array(row)
                ar = ar.reshape(-1,1)
                print(ar)
                sList.append(ar)


if __name__ == "__main__":
    main()