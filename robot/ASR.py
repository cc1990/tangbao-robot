# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from aip import AipSpeech
from . import config, logging, utils

logger = logging.getLogger(__name__)

class AbstractASR(object):
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
    def transcribe(self, fp):
        pass


class BaiduASR(AbstractASR):
    """
    百度语音识别API
    dev_pid:
        - 1936: 普通话远场
        - 1536：普通话(支持简单的英文识别)
        - 1537：普通话(纯中文识别)
        - 1737：英语
        - 1637：粤语
        - 1837：四川话
    """

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

    def transcribe(self, fp):
        """
        识别本地文件
        :param fp: wav 文件路径
        :return:
        """
        pcm = utils.get_pcm_from_wav(fp)
        res = self.client.asr(pcm, 'pcm', 16000, {
            'dev_pid': self.dev_pid
        })
        if res['err_no'] == 0:
            logger.info('{} 语音识别内容：{}'.format(self.SLUG, res['result']))
            return ''.join(res['result'])
        else:
            logger.info("{} 语音识别出错：".format(self.SLUG, res['err_msg']))
            return ''


def get_engine_by_slug(slug=None):
    if not slug or type(slug) is not str:
        raise TypeError("无效的 ASR slug %s" % slug)

    engines = list(filter(lambda engine: hasattr(engine, 'SLUG') and engine.SLUG == slug, get_engines()))
    if len(engines) == 0:
        raise ValueError("找不到名为 {} 的 ASR 引擎".format(slug))
    else:
        if len(engines) > 1:
            logger.info("注意：有多个 ASR 名称与指定名称 {} 匹配".format(slug))
        engine = engines[0]
        logger.info("使用 {} ASR 引擎".format(slug))
        return engine.get_instance()

def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [engine for engine in
            list(get_subclasses(AbstractASR))
            if hasattr(engine, 'SLUG') and engine.SLUG]
