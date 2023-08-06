def mxmul(mx1, mx2, nrow, nk, ncol):  # 参数说明：矩阵1，矩阵2，矩阵1行数，矩阵1列数，矩阵2列数
    "矩阵乘法运算"
    rst = [[0 for y in range(ncol)] for x in range(nrow)] # 创建1个全是0的矩阵，用于存放结果
    # [i**2 for i in range(1,11)] 高效创建列表的方式，1-10的平方
    # print(rst)
    for i in range(nrow):
        for j in range(ncol):
            for k in range(nk):
                rst[i][j] += mx1[i][k] * mx2[k][j]
    return rst


def mxsum(mx, nrow, ncol):
    "矩阵各元素求和运算"
    s = 0
    for i in range(nrow):
        for j in range(ncol):
            s += mx[i][j]
    return s


if __name__ == "__main__": #import时不会被执行，只会在当前文件执行
    import time #import不一定要写在最前面，放在任何位置都可以！

    nrow, nk, ncol = 50, 30, 50
    mx1 = [[y for y in range(nk)] for x in range(nrow)]
    mx2 = [[y for y in range(ncol)] for x in range(nk)]
    start = time.perf_counter()
    rst = mxmul(mx1, mx2, nrow, nk, ncol)
    end = time.perf_counter()
    print("运算时间为{:.4f}s".format(end - start))
