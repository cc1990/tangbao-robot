# -*- coding: utf-8 -*-
# @Time    : 2019/12/28 17:37
# @Author  : cc
# @File    : TTS.py
# @Software: PyCharm


from abc import ABCMeta, abstractmethod
from aip import AipSpeech
from . import config, logging, utils

logger = logging.getLogger(__name__)

class AbstractTTS(object):
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
    def synthesis(self, texts):
        pass


class BaiduTTS(AbstractTTS):
    SLUG = 'baidu'

    def __init__(self, APP_ID, API_KEY, SECRET_KEY, dev_pid=1936):
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        self.dev_pid = dev_pid

    @classmethod
    def get_config(cls):
        APP_ID = config.get('baidu', 'APP_ID')
        API_KEY = config.get('baidu', 'API_KEY')
        SECRET_KEY = config.get('baidu', 'SECRET_KEY')
        dev_pid = config.get('baidu', 'dev_pid')
        return {'APP_ID': APP_ID, 'API_KEY': API_KEY, 'SECRET_KEY': SECRET_KEY, 'dev_pid': dev_pid}

    def synthesis(self, texts):
        """
        合成语音文件
        :param texts: 文字
        :return: 语音文件路径
        """
        result = self.client.synthesis(texts)
        if not isinstance(result, dict):
            tmp_file = utils.write_temp_file(result, '.mp3')
            logger.info('{} 语音合成成功，合成路径：{}'.format(self.SLUG, tmp_file))
            return tmp_file
        else:
            logger.critical('{} 合成失败！'.format(self.SLUG))


def get_engine_by_slug(slug=None):
    if not slug or type(slug) is not str:
        raise TypeError("无效的 TTS slug %s" % slug)

    engines = list(filter(lambda engine: hasattr(engine, 'SLUG') and engine.SLUG == slug, get_engines()))
    if len(engines) == 0:
        raise ValueError("找不到名为 {} 的 TTS 引擎".format(slug))
    else:
        if len(engines) > 1:
            logger.info("注意：有多个 TTS 名称与指定名称 {} 匹配".format(slug))
        engine = engines[0]
        logger.info("使用 {} TTS 引擎".format(slug))
        return engine.get_instance()

def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [engine for engine in
            list(get_subclasses(AbstractTTS))
            if hasattr(engine, 'SLUG') and engine.SLUG]
