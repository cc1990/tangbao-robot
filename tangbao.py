# -*- coding: utf-8 -*-
from snowboy import snowboydecoder
import signal

from robot import config, logging, constants, Player, LED
from robot.Conversation import Conversation

logger = logging.getLogger(__name__)

class TangBao(object):
    def __init__(self):
        self._interrupted = False
        self._conversation = Conversation()
        print("""
********************************************************
*          tangbao-robot - 中文语音对话机器人          *
*          (c) 2020 CC <rnckty@sina.com>              *
*     https://github.com/cc1990/tangbao-robot.git        *
********************************************************
        """)


    def _signal_handler(self, signal, frame):
        self._interrupted = True

    def _detected_callback(self):
        Player.play(constants.getData('ding.wav'))
        self._conversation._pixel.think()
        logger.info('唤醒成功，开始录音...')

    def _interrupt_callback(self):
        return self._interrupted

    def run(self):
        print("请对机器人说：{}".format(config.get('snowboy', 'hotword_name')))
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, self._signal_handler)

        try:
            if config.get('led','enable'):
                LED.wakeup()
            self.initDetector()
        except Exception as e:
            raise e

    def initDetector(self):
        model = config.get('snowboy', 'hotword', 'tangbao.pmdl')
        detector = snowboydecoder.HotwordDetector(constants.getHotwordModel(model),
                                                  sensitivity=config.get('snowboy', 'sensitivity', '0.5'))

        logger.info("开始进入监听状态..")
        detector.start(detected_callback=self._detected_callback,
                       audio_recorder_callback=self._conversation.converse,
                       interrupt_check=self._interrupt_callback,
                       recording_timeout=int(config.get('snowboy', 'recording_timeout', 5)) * 4
                       )


if __name__ == '__main__':
    tangbao = TangBao()
    tangbao.run()

