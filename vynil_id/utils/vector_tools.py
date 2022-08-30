import numpy as np

def perp(a) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# returns the intersect as an np.array
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    intersect = (num / denom.astype(float))*db + b1
    return intersect

if __name__ == '__main__':
    arr = np.array(([0,0],[5,0],[6,0],[6,1]))
    print(seg_intersect(arr[0],arr[1],arr[2],arr[3]))
