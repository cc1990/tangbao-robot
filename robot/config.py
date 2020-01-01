# -*- coding: utf-8 -*-
import os
import configparser

from . import logging
from . import constants

logger = logging.getLogger(__name__)

def get(section, option, default=''):
    config_file = constants.getConfigPath()
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        return config.get(section, option)
    except Exception as e:
        logger.error("读取配置文件错误：%s" % str(e))
        return default