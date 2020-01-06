# -*- coding: utf-8 -*-
# @Time    : 2020/1/4 21:43
# @Author  : cc
# @File    : Plugin.py
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
from robot import constants, logging
from pkgutil import walk_packages

logger = logging.getLogger(__name__)

class AbstractPlugin(object):
    SLUG = 'AbstractPlugin'

    __metaclass__ = ABCMeta

    def __init__(self, con):
        self.con = con

    def say(self, msg):
        self.con.say(msg)

    @abstractmethod
    def handle(self, query, parsed):
        """
        处理逻辑

        :param query: 用户的指令字符串
        :param parsed: 用户指令经过 NLU 解析后的结果
        :return:
        """
        pass

    def isValid(self, query, parsed):
        """
        是否由该插件处理

        :param query: 用户的指令字符串
        :param parsed: 用户指令经过 NLU 解析后的结果
        :return: True，适合由该插件处理；False，不适合由该插件处理
        """
        return False



def load_plugin(con):
    path = [constants.PLUGIN_PATH]
    nameSet = set()
    plugins = []
    for finder, name, ispkg in walk_packages(path):
        try:
            loader = finder.find_module(name)
            mod = loader.load_module(name)
        except Exception as e:
            logger.warning('插件 {} 加载出错：{}'.format(name, e))
            continue

        if not hasattr(mod, 'Plugin'):
            logger.debug("模块 {} 非插件，跳过".format(name))
            continue

        plugin = mod.Plugin(con)
        if plugin.SLUG == 'AbstractPlugin':
            plugin.SLUG = name

        if plugin.SLUG in nameSet:
            logger.warning("插件 {} SLUG({}) 重复，跳过".format(name, plugin.SLUG))
            continue

        nameSet.add(plugin.SLUG)

        if issubclass(mod.Plugin, AbstractPlugin):
            logger.info("插件 {} 加载成功 ".format(name))
            plugins.append(plugin)

    return plugins