# -*- coding: utf-8 -*-

from . import config, Player, constants, logging, utils, ASR, AI, TTS
from robot.Brain import Brain

from pixel_ring import pixel_ring

logger = logging.getLogger(__name__)

class Conversation(object):
    def __init__(self):
        self.asr = ASR.get_engine_by_slug(config.get('engine', 'asr'))
        self.ai = AI.get_engine_by_slug(config.get('engine', 'robot'))
        self.tts = TTS.get_engine_by_slug(config.get('engine', 'tts'))
        self.brain = Brain(self)

        self._pixel = pixel_ring

    def converse(self, fp):
        Player.play(constants.getData('dong.wav'))
        logger.info("结束录音，录音文件路径： %s" % fp)
        self.doConverse(fp)

    def doConverse(self, fp):
        self._pixel.speak()
        query = self.asr.transcribe(fp)
        logger.info("语音识别结果：%s" % query)
        try:
            utils.check_and_delete(fp)
            self.doReSponse(query)
        except Exception as e:
            logger.error(e)

        self._pixel.wakeup()

    def doReSponse(self, query):
        """
        技能响应

        将语音识别的结果进行技能锁定
        目前不对技能进行匹配，暂时交由聊天机器人处理
        :param query: 语音识别的文字信息
        :return:
        """
        try:
            if not self.brain.parse(query):
                logger.info("未命中技能，开始交由聊天机器人进行处理")
                msg = self.ai.chat(query)
                self.say(msg)

        except Exception as e:
            logger.critical(e)

    def say(self, msg):
        cache_path = utils.get_cache(msg)
        if cache_path is None:
            logger.info("没有找到缓存文件，开始缓存处理...")
            try:
                temp_path = self.tts.synthesis(msg)
                cache_path = utils.save_cache(temp_path, msg)
                logger.info("保存缓存成功，路径：{}".format(cache_path))
            except Exception as e:
                logger.error('保存缓存失败：{}'.format(e))
        else:
            logger.info("找到缓存文件，开始播放缓存文件...")

        Player.play(cache_path)


