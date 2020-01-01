# -*- coding: utf-8 -*-
# @Time    : 2019/12/28 16:40
# @Author  : cc
# @File    : AI.py
# @Software: PyCharm

import requests
import json

from abc import ABCMeta, abstractmethod
from uuid import getnode as get_mac

from . import config, logging, utils


logger = logging.getLogger(__name__)

class AbstractRobot(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        pass

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls):
        profile = cls.get_config()
        instance = cls(**profile)
        return instance

    @abstractmethod
    def chat(self, text):
        pass

class TulingRobot(AbstractRobot):
    SLUG = 'tuling'

    def __init__(self, apiKey):
        self.apiKey = apiKey

    @classmethod
    def get_config(cl):
        api_key = config.get('tuling', 'api_key')
        return {'apiKey': api_key}

    def chat(self, texts):
        url="http://openapi.tuling123.com/openapi/api/v2"
        userId = get_mac()
        userInfo = {'apiKey': self.apiKey, 'userId': userId}
        perception = {
            'inputText': {
                'text': texts
            },
            'selfInfo': {
                'location': {
                    'city': config.get('location', 'city', '杭州'),
                    'province': config.get('location', 'province', '浙江')
                }
            }
        }
        data = {'reqType': 0, 'perception': perception, 'userInfo': userInfo}

        try:
            # data_json = json.dumps(data, ensure_ascii = False)
            respond = requests.post(url, json=data, headers={'content-type': 'application/json;charset=UTF-8'})
            response = json.loads(respond.text)

            result = ''
            if response['intent']['code'] < 40000:
                for v in response['results']:
                    if v['resultType'] == 'text':
                        result += v['values']['text']
                logger.info("{} 回答：{}".format(self.SLUG, result))
                return result
            else:
                logger.warning("抱歉，{} 机器人暂时无法提供服务：{}".format(self.SLUG, response['results'][0]['values']['text']))
                return "抱歉，机器人暂时无法提供服务"
        except Exception as e:
            logger.critical("抱歉，{} 机器人出现故障：{}".format(self.SLUG, str(e)))
            return "抱歉，机器人短路了，请稍后再试"


def get_engine_by_slug(slug=None):
    if not slug or type(slug) is not str:
        raise TypeError("无效的 Robot slug %s" % slug)

    engines = list(filter(lambda engine: hasattr(engine, 'SLUG') and engine.SLUG == slug, get_engines()))
    if len(engines) == 0:
        raise ValueError("找不到名为 {} 的 Robot 引擎".format(slug))
    else:
        if len(engines) > 1:
            logger.info("注意：有多个 Robot 名称与指定名称 {} 匹配".format(slug))
        engine = engines[0]
        logger.info("使用 {} Robot 引擎".format(slug))
        return engine.get_instance()

def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [engine for engine in
            list(get_subclasses(AbstractRobot))
            if hasattr(engine, 'SLUG') and engine.SLUG]