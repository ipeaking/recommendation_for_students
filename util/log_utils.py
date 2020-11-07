# -*- coding: utf-8 -*-
"""
Author : Xiaobo Cheng
Contact: shawbown@foxmail.com
Date   : 2019/5/10 15:48
Desc   : 日志打印
"""
import logging
import os
import sys
import time

level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}  # 日志级别关系映射


class Logger:
    def __init__(self, level="info",
                 name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
                 log_name=time.strftime("%Y-%m-%d.log", time.localtime()),
                 log_path="../../logs",
                 fmt="%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s : %(message)s",
                 use_console=True):
        """
            level： 设置日志的打印级别，默认为DEBUG
            name： 日志中将会打印的name，默认为运行程序的name
            log_name： 日志文件的名字，默认为当前时间（年-月-日.log）
            log_path： 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
            fmt:  日志输出格式
            use_console： 是否在控制台打印，默认为True
        """
        self.logger = logging.getLogger(name)
        format_str = logging.Formatter(fmt)  # 设置日志格式

        if level in level_relations:
            self.logger.setLevel(level_relations.get(level))  # 设置日志级别
        else:
            self.logger.setLevel(logging.NOTSET)

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_file_path = os.path.join(log_path, log_name)
        log_handler = logging.FileHandler(filename=log_file_path)    # 输出到文件
        log_handler.setFormatter(format_str)

        if use_console:    # 在控制台输出
            self.logger.handlers.clear()
            console_handler = logging.StreamHandler()    # 输出到控制台
            console_handler.setFormatter(format_str)
            self.logger.addHandler(console_handler)    # 添加控制台handler

        self.logger.addHandler(log_handler)    # 添加文件handler,addHandler需要放在最后

    def addHandler(self, hdlr):
        self.logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        self.logger.removeHandler(hdlr)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)


if __name__ == '__main__':
    log = Logger('debug')
    log.logger.info("this is a log")
