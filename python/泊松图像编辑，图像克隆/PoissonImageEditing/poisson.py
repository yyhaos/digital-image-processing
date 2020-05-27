
import numpy as np
from scipy.sparse import linalg as linalg
from scipy.sparse import lil_matrix as lil_matrix

OMEGA = 0
DEL_OMEGA = 1
OUTSIDE = 2

# mask：mask图像
# 判断像素index在omega，还是在边界，或者外边
def point_location(index, mask):
    if in_omega(index,mask) == False:
        return OUTSIDE
    if edge(index,mask) == True:
        return DEL_OMEGA
    return OMEGA

# 判断一个像素index在不在omega里
def in_omega(index, mask):
    return mask[index] == 1

# 判断像素点index在omega或者边界
def edge(index, mask):
    if in_omega(index,mask) == False: return False
    # 如果一个点在omega里，但是其旁边的点不在，则说明这个点在边界上
    for pt in get_surrounding(index):
        if in_omega(pt,mask) == False: return True
    return False

# 获取该像素点index上下左右像素点的坐标
def lapl_at_index(source, index):
    i,j = index
    val = (4 * source[i,j])    \
           - (1 * source[i+1, j]) \
           - (1 * source[i-1, j]) \
           - (1 * source[i, j+1]) \
           - (1 * source[i, j-1])
    return val

# 获得的所有mask内的像素点的坐标，将其存入一个list中。
def mask_indicies(mask):
    nonzero = np.nonzero(mask)
    return list(zip(nonzero[0], nonzero[1]))

# 获取上下左右像素点的坐标
def get_surrounding(index):
    i,j = index
    return [(i+1,j),(i-1,j),(i,j+1),(i,j-1)]

# 构建A矩阵
def poisson_sparse_matrix(points):
    N = len(points)
    A = lil_matrix((N,N))
    for i,index in enumerate(points):
        A[i,i] = 4
        for x in get_surrounding(index):
            if x not in points: continue
            j = points.index(x)
            A[i, j] = -1

    return A

# 泊松重建
def process(source, target, mask):
    indicies = mask_indicies(mask)
    N = len(indicies)
    A = poisson_sparse_matrix(indicies)
    b = np.zeros(N)
    for i,index in enumerate(indicies):
        b[i] = lapl_at_index(source, index)
        # Creates constraint lapl source = target at boundary
        if point_location(index, mask) == DEL_OMEGA:
            for pt in get_surrounding(index):
                if in_omega(pt,mask) == False:
                    b[i] += target[pt]
    x = linalg.cg(A, b)
    composite = np.copy(target).astype(int)
    for i,index in enumerate(indicies):
        composite[index] = x[0][i]
    return composite

def preview(source, target, mask):
    return (target * (1.0 - mask)) + (source * (mask))