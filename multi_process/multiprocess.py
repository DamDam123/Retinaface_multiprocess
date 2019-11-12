"""
多进程练习
"""

#导入多进程模块
import multiprocessing as mp
import os

#定义进程执行的函数
def job(a ,b):
    print("子进程", os.getpid())  # os.getpid获得当前进程的id
    print(a + b)

if __name__ == "__main__":
    p1 = mp.Process(target=job, args=(1, 2))#创建进程，target定义进程要执行的函数，args定义函数的需要的参数
    p1.start() #开始进程
    p1.join() #连接进程
    print(os.getpid()) #os.getppid获得当前父进程的id
    # print(os.getpid()) #os.getpid获得当前进程的id

