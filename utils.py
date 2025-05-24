# coding: utf-8
from datetime import datetime
import json
from flask import make_response, Response
from pathlib import Path
import os

from _utils import *
from env import main as mainenv


def info(*log):
    print(f"{datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')} ℹ️  [Info]", *log)


def infon(*log):
    print(f"\n{datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')} ℹ️  [Info]",*log)


def warning(*log):
    print(f"{datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')} ⚠️  [Warning]",*log)


def error(*log):
    print(f"{datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')} ❌  [Error]",*log)


def debug(*log):
    if mainenv.debug:
        print(f"{datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')} ⚙️  [Debug]",*log)


def format_dict(dic) -> Response:
    '''
    字典 -> Response (内容为格式化后的 json 文本)
    @param dic: 字典
    '''
    response = make_response(
        json.dumps(dic, indent=4, ensure_ascii=False, sort_keys=False, separators=(', ', ': '))
    )
    response.mimetype = 'application/json'
    return response


def reterr(code: int, message: str) -> str:
    '''
    返回错误信息 json

    :param code: 代码
    :param message: 消息
    '''
    ret = {
        'success': False,
        'code': code,
        'message': message
    }
    error(f'Response: {code} - {message}')
    return format_dict(ret)


@property
def show_404() -> str:
    return '<!DOCTYPE HTML>\n<html lang=en>\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404


class SleepyException(Exception):
    '''
    Custom Exception
    '''

    def __init__(self, msg=None):
        if msg:
            self.msg = msg

    def __str__(self):
        return self.msg


def exception(msg: str) -> SleepyException:
    '''
    抛出 SleepyException

    :param msg: 错误描述
    '''
    raise SleepyException(msg)


def list_dir(path: str, include_subfolder: bool = True, strict_exist: bool = False, ext: str = '') -> list:
    '''
    列出目录下的**文件**

    :param path: 目录路径
    :param include_subfolder: 是否包括子目录的文件 *(递归查找)*
    :param strict_exist: 目标目录不存在时是否抛出错误 *(为否则返回空列表)*
    :param ext: 指定文件扩展名 *(只有文件以此结尾才会计入)*
    '''

    try:
        filelst = os.listdir(path)
        for i in filelst:
            fullname_i = Path(path).joinpath(i)
            if os.path.isdir(fullname_i):
                # 为文件夹
                filelst.remove(i)
                if include_subfolder:
                    filelst.extend([
                        i + n if i.endswith('/') or i.endswith('\\') else i + '/' + n
                        for n in list_dir(
                            fullname_i,
                            include_subfolder=include_subfolder,
                            strict_exist=strict_exist,
                            ext=ext
                        )
                    ])
    except FileNotFoundError:
        # 找不到目标文件夹
        if strict_exist:
            raise
        else:
            return []
    else:
        if ext:
            newlst = []
            for i in filelst:
                if i.endswith(ext):
                    newlst.append(i)
            return newlst
        else:
            return filelst
