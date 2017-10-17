#!/usr/bin/env python
# @Author  : pengyun

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadTimeSignature
import re, urllib

# 判断是否有动态参数
_dynamic_route = re.compile(r'<(.+?)>')


def check_dynamic(path):
    """如果是动态path 返回True"""
    if len(_dynamic_route.findall(path)) == 0:
        return False
    return True


def quote(s, encoding="utf-8"):
    """将字符转化为二进制"""
    s = s.encode(encoding)
    return urllib.parse.quote(s)


def unquote(s):
    """
    >>> _unquote('http%3A//example/test%3Fa%3D1+')
    u'http://example/test?a=1+'
    """
    if isinstance(s, bytes):
        s = s.decode()
    return urllib.parse.unquote(s)


def static_stream(filepath):
    """流式传输数据"""
    BLOCK_SIZE = 1024 * 8
    with open(filepath, 'rb') as file:
        data = file.read(BLOCK_SIZE)
        while data:
            yield data
            data = file.read(BLOCK_SIZE)


def session(secret, expires=3600):
    """
    通过这个在cookie中设置
    :param secret: 密钥
    :param expires: 有效时间
    :return:
    """

    s = Serializer(secret_key=secret, expires_in=expires)
    s_cookies = s.dumps(ctx.session)
    ctx.response.set_cookie('session', s_cookies)


def open_session(secret, session):
    s = Serializer(secret_key=secret)
    try:
        s.loads(session)
    except BadTimeSignature:
        return Fa
