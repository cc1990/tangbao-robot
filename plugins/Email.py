# -*- coding: utf-8 -*-
# @Time    : 2019/12/27 22:47
# @Author  : cc
# @File    : Email.py
# @Software: PyCharm

from robot.Plugin import AbstractPlugin
from robot import logging

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):
    SLUG = 'email'

    def handle(self, query, parsed):
        logger.info("开始处理Email")
        self.say("开始处理邮件")

    def isValid(self, query, parsed):
        return any(word in query for word in ['邮箱', '邮件'])