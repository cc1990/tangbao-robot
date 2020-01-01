# -*- coding: utf-8 -*-

import os
import subprocess
import _thread as thread

from . import logging

logger = logging.getLogger(__name__)

def play(fname):
    player = getPlayerByFileName(fname)
    player.play(fname)

def getPlayerByFileName(fname):
    foo, ext = os.path.splitext(fname)
    if ext in ['.mp3', '.wav']:
        return SoxPlayer()

class SoxPlayer(object):
    def __init__(self):
        pass

    def doPlay(self):
        cmd = ['play', str(self.src)]
        logger.info("Executing %s", ' '.join(cmd))
        self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def play(self, src):
        if os.path.exists(src):
            self.src = src
            thread.start_new_thread(self.doPlay, ())
        else:
            logger.critical("path is not exists: %s" % src)