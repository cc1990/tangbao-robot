# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

from robot import constants

def getLogger(name):
    """
    重写getLogger方法

    :return: logger
    """
    log_name = '%s.log' % datetime.strftime(datetime.now(), '%Y-%m-%d')
    log_file = os.path.join(constants.LOG_PATH, log_name)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.addHandler(file_handler)
    file_handler.setFormatter(formatter)
    return logger
