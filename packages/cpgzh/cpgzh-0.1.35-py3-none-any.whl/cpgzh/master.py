import gc
import os
import sys
import time

import guizero
import pygame
import pygame.draw
from guizero import App

from .data import Data

MAX_FPS = 120


def round_xy(pos):
    "四舍五入坐标"
    if isinstance(pos, tuple):
        x, y = pos
        return (round(x), round(y))
    else:
        return round(pos)


class Task:
    '任务类'

    def __init__(self, id, time_count, func, args) -> None:
        '任务类'
        self.id = id
        self.time_count = time_count
        self.__func = func
        self.__args = args
        self.hp = 1

    def run(self):
        '运行任务'
        if int(time.time()*MAX_FPS) >= self.time_count:
            self.__func(*self.__args)
            self.hp = 0


class Master:
    "管家类，负责一些管理类的功能"

    def __init__(self, data_path="data.dat") -> None:
        "管家类，负责一些管理类的功能"
        self._fullscreen = False
        self.data = Data(data_path)
        self.load_data()
        self.data.temp = ""
        self.app = App(visible=False)
        self.mod = sys.modules["__main__"]
        self._task_id = 0
        self.tasks = []

    @property
    def data_path(self):
        "获取data_path"
        return self.data.data_path

    @data_path.setter
    def data_path(self, path):
        "设置data_path"
        print(f"数据地址{path}")
        self.data.data_path = path

    def load_data(self):
        "加载数据"
        self.data.load_data()

    def save_data(self):
        "保存数据"
        self.data.save_data()

    def del_data(self):
        "删除数据"
        self.data.del_data()

    def set_fullscreen(self) -> None:
        "设置全屏"
        self.mod.screen.surface = pygame.display.set_mode(
            (self.mod.WIDTH, self.mod.HEIGHT), pygame.FULLSCREEN
        )
        self._fullscreen = True

    def set_windowed(self) -> None:
        "设置窗口化"
        os.environ['SDL_VIDEO_CENTERED'] = "1"  # pygame设置窗口在中心，实测无效
        self.mod.screen.surface = pygame.display.set_mode(
            (self.mod.WIDTH, self.mod.HEIGHT)
        )
        self._fullscreen = False

    def toggle_fullscreen(self) -> None:
        "切换全屏和窗口化"
        if self._fullscreen:
            self.set_windowed()
        else:
            self.set_fullscreen()

    def input(self, msg="请输入数据：", dtype=0) -> str or int or float:
        """
        简单输入框\n
        dtype控制输入的数据类型\n
        dtype=0或其他输入字符串\n
        dtype=1输入整数\n
        dtype=2输入浮点数\n
        """
        if dtype == 1:
            text = guizero.askstring("输入整数", msg)
            text = int(text)
        elif dtype == 2:
            text = guizero.askstringt("输入小数", msg)
            text = float(text)
        else:
            text = guizero.askstring("输入", msg)
        self.data.temp = text
        return text

    def select_file(self, msg="请选择文件", filetypes=[["All files", "*.*"]]) -> str:
        """
        选择文件，filetypes是文件类型，比如：

        filetypes=[["All files", "*.*"]]

        不想限定的话，就不传递这个参数。
        """
        file = guizero.select_file(msg, filetypes=filetypes)
        self.data.temp = file
        return file

    def select_file_save(self, msg="请选择文件", filetypes=[["All files", "*.*"]]) -> str:
        """
        保存文件的选择提示框，filetypes是文件类型，比如：

        filetypes=[["All files", "*.*"]]

        不想限定的话，就不传递这个参数。
        """
        path = guizero.select_file(msg, filetypes=filetypes, save=True)
        self.data.temp = path
        return path

    def select_dir(self, msg="请选择文件夹") -> str:
        "选择一个文件夹"
        dir = guizero.select_folder(msg)
        self.data.temp = dir
        return dir

    def yes_no(self, msg="是否？"):
        "是否做某件事的选择框"
        yes_or_no = guizero.yesno("请选择", msg)
        self.data.temp = yes_or_no
        return yes_or_no

    def msg(self, msg="这是提示信息"):
        "提示信息"
        guizero.info("提示", msg)

    def warning(self, msg="这是警告信息"):
        "警告信息"
        guizero.warn("警告", msg)

    def error(self, msg="这是错误信息"):
        "错误信息"
        guizero.error("错误", msg)

    def run_tasks(self):
        """
        根据计划任务执行要做的事\n
        需要放在update函数中执行
        """
        left_tasks = []
        for task in self.tasks:
            task.run()  # 执行计划任务
            if task.hp:
                left_tasks.append(task)
        self.tasks = left_tasks
        del left_tasks
        gc.collect()  # 释放内存

    def create_delay_tasks(self, task, seconds=1, times=1, args=()):
        """
        创建任务队列并添加到角色的任务列表中。\n
        延迟seconds秒执行task任务，times代表这个任务执行多少次。\n
        args是这个任务要用到的参数。\n
        只写第一个参数就是等待1秒执行1次task。\n
        """
        now = time.time()
        for i in range(times):
            task_time = now + (i + 1) * seconds  # 计算执行任务的时间
            time_count = int(task_time * MAX_FPS)  # 计算计数器走到哪一帧
            self._task_id += 1
            # 将任务加到任务队列
            task = Task(self._task_id, time_count, task, args)
            self.tasks.append(task)

    def remove_taskById(self, id):
        "根据id删掉任务"
        del_task = 0
        for task in self.tasks:
            if task.id == id:
                del_task = task
                break
        del del_task
