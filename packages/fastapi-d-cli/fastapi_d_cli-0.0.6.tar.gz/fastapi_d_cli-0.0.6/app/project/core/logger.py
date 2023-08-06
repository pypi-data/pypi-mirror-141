# -*- coding: utf-8 -*-
# @Time: 2021/6/21 16:48
# @File: logger.py
# @Desc：
import os
import time
from loguru import logger


def creat_customize_log_loguru():
    """
    loguru 自定义日志配置
    :return:
    """
    BASEDIR = os.path.dirname(os.path.dirname(__file__))
    LOG_PATH = os.path.join(BASEDIR, 'log')
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)
    # 定义info_log文件名称
    log_file_path = os.path.join(LOG_PATH, f"{time.strftime('%Y-%m-%d')}_info.log")
    # 定义err_log文件名称
    err_log_file_path = os.path.join(LOG_PATH, f"{time.strftime('%Y-%m-%d')}_error.log")
    # 定义debug_log文件名称
    debug_log_file_path = os.path.join(LOG_PATH, f"{time.strftime('%Y-%m-%d')}_debug.log")

    from sys import stdout
    LOGURU_FORMAT: str = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <16}</level> | <bold>{message}</bold>'
    # 这句话很关键避免多次的写入我们的日志
    logger.configure(handlers=[{'sink': stdout, 'format': LOGURU_FORMAT}])
    # 错误日志不需要压缩
    format = " {time:YYYY-MM-DD HH:mm:ss:SSS} | process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} |\n {message}"
    # enqueue=True表示 开启异步写入
    # 使用 rotation 参数实现定时创建 log 文件,可以实现每天 0 点新创建一个 log 文件输出了
    logger.add(err_log_file_path, format=format, rotation='00:00', encoding='utf-8', level='ERROR',
               enqueue=True)  # Automatically rotate too big file
    # 对应不同的格式
    format2 = " {time:YYYY-MM-DD HH:mm:ss:SSS} | process_id:{process.id} process_name:{process.name} | thread_id:{thread.id} thread_name:{thread.name} | {level} | {message}"

    # enqueue=True表示 开启异步写入
    # 使用 rotation 参数实现定时创建 log 文件,可以实现每天 0 点新创建一个 log 文件输出了
    logger.add(log_file_path, format=format2, rotation='00:00', compression="zip", encoding='utf-8', level='INFO',
               enqueue=True)  # Automatically rotate too big file
    logger.add(debug_log_file_path, format=format2, rotation='00:00', compression="zip", encoding='utf-8', level='DEBUG',
               enqueue=True)  # Automatically rotate too big file


creat_customize_log_loguru()
