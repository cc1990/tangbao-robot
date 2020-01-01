# -*- coding: utf-8 -*-

import wave
import os
import shutil
import hashlib
import tempfile
import time

from . import constants, config

def get_file_content(file_path):
    """
    读取文件内容并返回
    :param filePath: 文件路径
    :return: 文件内容
    """
    with open(file_path, 'rb') as fp:
        return fp.read()

def get_pcm_from_wav(wav_path):
    """
    从 wav 文件中读取 pcm
    :param wav_path: wav 文件路径
    :return: pcm 数据
    """
    wav = wave.open(wav_path)
    return wav.readframes(wav.getnframes())

def check_and_delete(fp):
    """
    删除文件 / 文件夹
    :param fp:
    :return:
    """
    if os.path.exists(fp):
        if os.path.isfile(fp):
            os.remove(fp)
        else:
            shutil.rmtree(fp)

def write_temp_file(data, suffix, mode='w+b'):
    """
    写入临时文件
    :param data: 数据
    :param suffix: 后缀名
    :param mode: 写入模式
    :return: 临时文件路径
    """
    with tempfile.NamedTemporaryFile(mode=mode, suffix=suffix, delete=False) as f:
        f.write(data)
        tmpfile = f.name
    return tmpfile

def get_cache(msg):
    """
    获取缓存语音文件
    :param msg:
    :return:
    """
    md5_str = hashlib.md5(msg.encode("utf-8")).hexdigest()
    mp3_cache = os.path.join(constants.CACHE_PATH, md5_str + '.mp3')
    wav_cache = os.path.join(constants.CACHE_PATH, md5_str + '.wav')

    if os.path.isfile(mp3_cache):
        return mp3_cache
    elif os.path.isfile(wav_cache):
        return wav_cache
    else:
        return None

def save_cache(temp_path, msg):
    """
    临时文件保存成缓存文件
    :param temp_path:
    :param msg:
    :return:
    """
    md5_str = hashlib.md5(msg.encode("utf-8")).hexdigest()
    foo, ext = os.path.splitext(temp_path)
    cache_path = os.path.join(constants.CACHE_PATH, md5_str + ext)
    shutil.move(temp_path, cache_path)
    return cache_path