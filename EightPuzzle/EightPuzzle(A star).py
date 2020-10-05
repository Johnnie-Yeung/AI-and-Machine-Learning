import numpy as np
import operator
import time

# 对节点列表按照估价函数的值的规则排序
def list_sort(list):
    cmp = operator.attrgetter('f')
    list.sort(key=cmp)

class State:
    def __init__(self, state, answer):
        self.state = state  # state是一个状态，输入为np.array，呈现为(3，3)的矩阵
        self.answer = answer
        self.f = 0  # f(n)=g(n)+h(n)
        self.g = 0  # g(n)
        self.h = 0  # h(n)
        self.parent = None  # 节点的父节点，便于回溯
        self.symbol = ' '  # 代表空位置的标志为一个空格

    # 启发函数
    def hn(self):
        forecast_cost = 0
        # 对比当前状态与目标状态有多少个位置的数字是不一样的，这个数作为h(n)，即预测的代价
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != self.answer[i][j]:
                    forecast_cost += 1
        return forecast_cost

    # 得到空的那个位置，返回它的row,col两个参数
    def getEmptyPos(self):
        position = np.where(self.state == self.symbol)
        return position

    # 基于BFS搜索算法改进的A*算法
    def A_star(self):
        openTable = []
        closeTable = []
        openTable.append(self)  # 把起始节点S放到未扩展节点OPEN表中
        steps = 0

        while len(openTable) > 0:  # 当open表不为空
            n = openTable.pop(0)  # 取出open表的首节点
            closeTable.append(n)  # 把这个节点放进close表中
            if (n.state == self.answer).all():  # 判断是否与目标状态一致
                path = []  # # 创建一个存放路径节点的list
                while n.parent is not None and n.parent != self:
                    path.append(n.parent)
                    n = n.parent
                path.reverse()  # 最后把路径list顺序调转一下
                return path, steps+1
            # 找出此时状态的空格位置
            row, col = n.getEmptyPos()

            # 开始移动
            for i in range(3):
                for j in range(3):
                    c = n.state.copy()
                    if (i + j - row - col) ** 2 == 1:  # 找到c[row, col]（即空格的位置）的邻居位置
                        c[row, col] = c[i, j]
                        c[i, j] = self.symbol
                        # 生成子状态
                        newState = State(c, self.answer)
                        newState.parent = n  # 此时取出的节点n成为新节点的父节点
                        newState.g = n.g + 1  # 新节点的g(n)要在父节点的g(n)基础上+1
                        newState.h = newState.hn()  # 新节点的启发函数值
                        newState.f = newState.g + newState.h  # 新节点的估价函数值
                        openTable.append(newState)  # 加入open表中
            list_sort(openTable)  # open表中的节点按照f(n)大小排序
            steps += 1
        else:
            return None, None

    # 输出当前状态
    def PrintState(self):
        for i in range(3):
            for j in range(3):
                print(self.state[i, j], end='  ')  # end=' '防止自动换行
            print("\n")
        print('---------------------------')
        return


start = time.perf_counter()  # 开始计时

if __name__ == '__main__':
    # 设置空位置的标志为一个空格
    EmptySymbol = ' '

    # 设置矩阵最初状态
    originState = np.array([[2, 8, 3], [1, 6, 4], [7, EmptySymbol, 5]])
    # 设置矩阵最终状态
    answer1 = np.array([[1, 2, 3], [8, EmptySymbol, 4], [7, 6, 5]])

    s1 = State(originState, answer1)
    path, steps = s1.A_star()

    if path:    # 如果找到通关路径
        print('---------------------------')
        print('The origin state is:')
        print(' ')
        s1.PrintState()  # 把初始状态显示出来
        count = 1
        for n in path:  # 打印路径
            print('[' + str(count) + ']')
            n.PrintState()
            count += 1
        print('The answer is:')
        print(' ')
        print(s1.answer)
        print("Total steps is", steps)
        print('---------------------------')
    else:
        print('Cannot find a solution.')


end = time.perf_counter()  # 结束计时
print('Running Time:', end-start, 'seconds')
print('---------------------------')