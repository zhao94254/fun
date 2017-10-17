#!/usr/bin/env python
# @Author  : pengyun


class Dict(dict):
    """
    support dict.key
    >>> a = {}
    >>> a['v']=12
    >>> a
    {'v': 12}
    >>> a = Dict(a=2,b=3)
    {'a': 2, 'b': 3}
    >>> a = Dict(('a','b'),(1,2))
    {'a': 2, 'b': 3}
    """

    def __init__(self, names=(), values=(), **kwargs):
        super().__init__(kwargs)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError("Dict haven't {}".format(k))


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self._instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)
            return self._instance
        else:
            return self._instance


def redirect(location, code=302, response=None):
    # 这里必须要加 / 否则，会在一直重定向
    response.set_header('Location', '/' + location)
    response.status = code
    return """
            <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n
            <title>Redirecting...</title>\n
            <h1>Redirecting...</h1>\n
            <p>You should be redirected automatically to target URL: 
            <a href="../{}">{}</a>.  If not click the link.
            """.format(location, location)


def url_for(endpoint, **kw):
    if 'filename' in kw:
        return endpoint + '/' + kw['filename']


def jsonify(data):
    from pweb.server.pweb import ctx
    from json import dumps
    ctx.response.content_type = 'application/json'
    return dumps(data)
