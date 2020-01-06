# -*- coding: utf-8 -*-
# @Time    : 2020/1/2 11:27
# @Author  : cc
# @File    : NLU.py
# @Software: PyCharm
import os
import requests
import uuid
from datetime import datetime
from abc import ABCMeta, abstractmethod
from aip import AipSpeech
from . import config, logging, utils, constants

logger = logging.getLogger(__name__)

class AbstractNLU(object):
    __metaclass__ = ABCMeta

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls):
        profile = cls.get_config()
        instance = cls(**profile)
        return instance

    @abstractmethod
    def parse(self, texts):
        pass


class BaiduNLU(AbstractNLU):
    SLUG = 'unit'

    def __init__(self, SERVICE_ID):
        self.api_url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat"
        self.SERVICE_ID = SERVICE_ID

    @classmethod
    def get_config(cls):
        SERVICE_ID = config.get('unit', 'SERVICE_ID')
        return {'SERVICE_ID': SERVICE_ID}

    def get_token(self):
        """
        获取 Access Token
        :return:
        """
        cache_token = self.get_cache_token()
        if cache_token == '':
            token = self.get_online_token()
        else:
            token = cache_token

        return token

    def get_cache_token(self):
        """
        获取缓存 Access Token
        :return:
        """
        token = ''

        cache_file = os.path.join(constants.TEMP_PATH, 'baidu_unit.ini')
        try:
            cache = open(cache_file, 'r')
            cache_data = cache.readlines()
            if len(cache_data) > 2:
                create_time = cache_data[0].replace('\r', '').replace('\n', '')
                cache_time = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
                expires_in = int(cache_data[1].replace('\r', '').replace('\n', ''))  # token 有效期
                now_time = datetime.now()
                expiry_second = (now_time - cache_time).seconds  # 实际有效期
                # Access Token的有效期(秒为单位，一般为1个月)；
                # 防止恰巧到有效期的时间，此处预留60秒的时间
                if expiry_second < expires_in-60:
                    token = cache_data[2].replace('\r', '').replace('\n', '')

            else:
                logger.info("共有行数 {} 行".format(str(len(cache_data))))
        except Exception as e:
            logger.warning("获取百度 unit token 缓存错误：{}".format(e))

        return token

    def get_online_token(self):
        """
        在线获取 Access Token

        在线获取token，并写入缓存文件
        :return: token
        """
        access_token = ''

        url = "https://aip.baidubce.com/oauth/2.0/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': config.get('unit', 'API_KEY'),
            'client_secret': config.get('unit', 'SECRET_KEY')
        }

        response = requests.get(url, params=data)
        try:
            result = response.json()
            if 'error' in result:
                logger.warning("获取百度 unit token码失败：" .format(result['error_description']))
            else:
                create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                access_token = result['access_token']
                expires_in = result['expires_in']

                self.cache_access_token(create_time, expires_in, access_token)
        except Exception as e:
            logger.warning("请求百度 unit token码失败：" .format(e))

        return access_token


    def cache_access_token(self, create_time, expires_in, access_token):
        """
        将请求的授权信息写入缓存文件

        :param create_time: 生成时间
        :param expires_in: 有效期（秒）
        :param access_token: Access Token
        :return:
        """
        cache_file = os.path.join(constants.TEMP_PATH, 'baidu_unit.ini')

        try:
            fp = open(cache_file, 'w+')
            fp.write(str(create_time))
            fp.write('\r\n')
            fp.write(str(expires_in))
            fp.write('\r\n')
            fp.write(str(access_token))
            fp.write('\r\n')
        except Exception as e:
            logger.warning("百度 unit 缓存信息写入失败：{}".format(e))

    def get_unit(self, query):
        """
        获取机器人对话
        :param query:
        :return:
        """
        access_token = self.get_token()
        url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token="+access_token
        request = {
            'user_id': '888888',
            'query': query
        }
        body = {
            'service_id': self.SERVICE_ID,
            'version': '2.0',
            'log_id': str(uuid.uuid4()),
            'session_id': str(uuid.uuid4()),
            'request': request
        }
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            request = requests.post(url, json=body, headers=headers)
            return request.json()
        except Exception as e:
            return None


def get_engine_by_slug(slug=None):
    if not slug or type(slug) is not str:
        raise TypeError("无效的 NLU slug %s" % slug)

    engines = list(filter(lambda engine: hasattr(engine, 'SLUG') and engine.SLUG == slug, get_engines()))
    if len(engines) == 0:
        raise ValueError("找不到名为 {} 的 NLU 引擎".format(slug))
    else:
        if len(engines) > 1:
            logger.info("注意：有多个 NLU 名称与指定名称 {} 匹配".format(slug))
        engine = engines[0]
        logger.info("使用 {} NLU 引擎".format(slug))
        return engine.get_instance()

def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [engine for engine in
            list(get_subclasses(AbstractNLU))
            if hasattr(engine, 'SLUG') and engine.SLUG]
