# -*- coding: utf-8 -*-
# @Time    : 2019/12/31 10:54
# @Author  : cc
# @File    : LED.py
# @Software: PyCharm

"""
默认使用的是ReSpeaker 4-mics的LED效果
参考文档：http://wiki.seeedstudio.com/cn/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/
"""

from pixel_ring import pixel_ring
from gpiozero import LED

power = LED(5)
power.on()

pixel_ring.set_brightness(10)

def wakeup():
    pixel_ring.wakeup()

def think():
    pixel_ring.think()

def speak():
    pixel_ring.speak()

def off():
    pixel_ring.off()