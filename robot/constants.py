# -*- coding: utf-8 -*-
import os

APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

LIB_PATH = os.path.join(APP_PATH, "robot")
DATA_PATH = os.path.join(APP_PATH, "static")
LOG_PATH = os.path.join(APP_PATH, "log")
PLUGIN_PATH = os.path.join(APP_PATH, "plugins")
TEMP_PATH = os.path.join(APP_PATH, "temp")
CACHE_PATH = os.path.join(TEMP_PATH, "cache")
CONFIG_NAME = 'config.ini'

def getConfigPath():
    """
    获取配置文件的存储路径

    :return: 配置文件的存储路径
    """
    return os.path.join(APP_PATH, CONFIG_NAME)

def getData(fname):
    """
    获取资源目录下指定文件路径

    :param fname: 指定文件名
    :return: 文件的存储路径
    """
    return os.path.join(DATA_PATH, fname)

def getHotwordModel(fname):
    """
    获取唤醒词的存储路径

    :param fname: 指定文件名
    :return: 唤醒词的存储路径
    """
    return os.path.normpath(os.path.join(DATA_PATH, fname))