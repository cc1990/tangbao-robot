# -*- coding: utf-8 -*-
# @Time    : 2020/1/4 21:33
# @Author  : cc
# @File    : Brain.py
# @Software: PyCharm

from . import config, logging, NLU, Plugin

logger = logging.getLogger(__name__)

class Brain(object):
    def __init__(self, conversion):
        self.conversion = conversion
        self.nlu = NLU.get_engine_by_slug(config.get('engine', 'nlu'))
        self.plugins = Plugin.load_plugin(self.conversion)

    def isValid(self, plugin, text, parsed):
        return plugin.isValid(text, parsed)

    def parse(self, text):
        parsed = self.nlu.get_unit(text)
        for plugin in self.plugins:
            if not self.isValid(plugin, text, parsed):
                continue

            logger.info("'{}' 命中技能 {}".format(text, plugin.SLUG))

            try:
                plugin.handle(text, parsed)
                return True
            except Exception as e:
                logger.critical("执行插件失败：{}".format(e))
                msg = u"抱歉，插件{}出故障了，晚点再试试吧".format(plugin.SLUG)
                self.conversion.say(msg)

        return False
