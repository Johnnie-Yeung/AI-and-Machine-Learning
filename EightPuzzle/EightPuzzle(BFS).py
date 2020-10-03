import numpy as np
import time  # 计算程序运行时间

# 利用广度优先算法进行路径搜索，如果找到正确路径，则利用迭代方法进行回溯，回溯得到的就是路径

class State:   # 创建一个状态类
    def __init__(self, state, answer, last_pos_direction=None, parent=None):
        self.state = state  # state是一个状态，输入为list，呈现为(3，3)的矩阵
        self.answer = answer
        self.direction = ['up', 'down', 'left', 'right']
        if last_pos_direction:  # 代表上一步的那个方向，避免走重复的路
            self.direction.remove(last_pos_direction)  # 经过这一步，direction代表了在当前状态下能够前进的方向
        self.parent = parent    # 便于回溯
        self.symbol = ' '  # 代表空位置的标志为一个空格

    # 输出当前状态
    def PrintState(self):
        for i in range(3):
            for j in range(3):
                print(self.state[i, j], end='  ')  # end=' '防止自动换行
            print("\n")
        print('---------------------------')
        return

    # 得到空的那个位置，返回它的row,col两个参数
    def getEmptyPos(self):
        postion = np.where(self.state == self.symbol)
        return postion

    # 获取子状态，即前进一步之后可能的状态
    def generateSubStates(self):
        if not self.direction:  # 如果已经无路可走，就直接return一个空的子状态list
            return []
        subStates = []  # 创建一个装所有可能的子状态结点的空list
        boarder = len(self.state) - 1  # 这里的len是获取矩阵的阶数，边界等于阶数-1（因为row和col都从0开始）
        row, col = self.getEmptyPos()

        # 遵循‘上下左右’的优先顺序
        if 'up' in self.direction and row > 0:
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row-1, col]
            s[row-1, col] = temp[row, col]
            newState = State(s, answer=self.answer, last_pos_direction='down', parent=self)
            subStates.append(newState)
        if 'down' in self.direction and row < boarder:
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row+1, col]
            s[row+1, col] = temp[row, col]
            newState = State(s, answer=self.answer, last_pos_direction='up', parent=self)
            subStates.append(newState)
        if 'left' in self.direction and col > 0:  # 如果可以向左走
            s = self.state.copy()  # 把现在的状态先复制一个副本
            temp = s.copy()  # 再复制一个，以便位置互换
            s[row, col] = s[row, col-1]  # 把原先的空位设置为它左边一个位的值
            s[row, col-1] = temp[row, col] # 把原先空位的左边一个位设置为空位
            newState = State(s, answer=self.answer, last_pos_direction='right', parent=self)  # directionFlag设为right，因为我们刚刚向左走，所以走了这步之后不能再向右走
            subStates.append(newState)  # 放入到装子状态的list中
        if 'right' in self.direction and col < boarder:
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col+1]
            s[row, col+1] = temp[row, col]
            newState = State(s, answer=self.answer, last_pos_direction='left', parent=self)
            subStates.append(newState)
        return subStates

    def BFS_search(self):
        openTable = []
        closeTable = []
        openTable.append(self)  # 把起始节点S放到未扩展节点OPEN表中
        steps = 1

        while len(openTable) > 0:
            n = openTable.pop(0)  # 取出open表中的第一个节点
            closeTable.append(n)  # 把这个节点放进close表中
            subStates = n.generateSubStates()  # 得到节点n的所有子状态
            path = []  # 创建一个存放路径节点的list
            for s in subStates:  # 遍历n的所有子状态
                if (s.state == s.answer).all():  # 如果目前状态等于answer，则代表路径有解
                    while s.parent and s.parent != s1:  # 递归回溯节点，存入路径list中
                        path.append(s.parent)
                        s = s.parent
                    path.reverse()  # 最后把路径list顺序调转一下
                    return path, steps+1
            openTable.extend(subStates)  # 如果没有一个子状态是最终解，则把subStates放入open表里，继续这个循环
            steps += 1
        else:
            return None, None


start = time.perf_counter()  # 开始计时

if __name__ == '__main__':
    # 设置空位置的标志为一个空格
    EmptySymbol = ' '

    # 设置矩阵最初状态
    originState = np.array([[2, 8, 3], [1, 6, 4], [7, EmptySymbol, 5]])
    # 设置矩阵最终状态
    answer1 = np.array([[1, 2, 3], [8, EmptySymbol, 4], [7, 6, 5]])
    s1 = State(state=originState, answer=answer1)
    path, steps = s1.BFS_search()
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

end = time.perf_counter()  # 结束计时
print('Running Time:', end-start, 'seconds')
print('---------------------------')