import numpy as np

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

if __name__ == "__main__":
    main()