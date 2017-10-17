#!/usr/bin/env python
# @Author  : pengyun

import os, re, cgi, mimetypes, threading
import logging as log
from pweb.server.http_status import *
from pweb.server.units import Dict, url_for
from pweb.server.helper import *
from werkzeug.http import dump_cookie

logging = log.getLogger('pyweb')
logging.setLevel(log.DEBUG)
output = log.StreamHandler()
output.setLevel(log.DEBUG)

logging.addHandler(output)

# 全局 保存信息
ctx = threading.local()


class HttpError(Exception):
    """处理http错误的基类"""

    def __init__(self, code):
        super().__init__()
        self.status = "{code} {status}".format(code=code, status=_RESPONSE_STATUSES[code])

    def __str__(self):
        return self.status

    __repr__ = __str__


class RedirectError(HttpError):
    """
    这个类处理重定向，默认状态码 302 ''
    >>> r = RedirectError(302, 'www.bbb')
    >>> r
    302 Found, www.bbb

    """

    def __init__(self, status=302, location=''):
        super(RedirectError, self).__init__(status)
        self.location = location

    def __str__(self):
        return "{}, {}".format(self.status, self.location)

    __repr__ = __str__


def bad_request():
    return HttpError(400)


def unauthorized():
    return HttpError(401)


def forbidden():
    return HttpError(403)


def notfound():
    return HttpError(404)


def conflict():
    return HttpError(409)


def internalerror():
    return HttpError(500)


def redirect(location):
    '''
    Do permanent redirect.
    >>> raise redirect('http://www.itranswarp.com/')
    Traceback (most recent call last):
      ...
    RedirectError: 301 Moved Permanently, http://www.itranswarp.com/
    '''
    return RedirectError(301, location)


def found(location):
    '''
    Do temporary redirect.
    >>> raise found('http://www.itranswarp.com/')
    Traceback (most recent call last):
      ...
    RedirectError: 302 Found, http://www.itranswarp.com/
    '''
    return RedirectError(302, location)


def seeother(location):
    '''
    Do temporary redirect.
    >>> raise seeother('http://www.itranswarp.com/')
    Traceback (most recent call last):
      ...
    RedirectError: 303 See Other, http://www.itranswarp.com/
    >>> e = seeother('http://www.itranswarp.com/seeother?r=123')
    >>> e.location
    'http://www.itranswarp.com/seeother?r=123'
    '''
    return RedirectError(303, location)


class RuntimeError(Exception):
    """运行时错误"""
    pass


class Route:
    """将路由和函数进行绑定"""

    def __init__(self, func):
        """区分开动态 和静态 并且将路由转化成正则"""
        self.path = func.__web_route__
        self.method = func.__web_method__
        self.is_static = not check_dynamic(self.path)

        self.func = func
        if not self.is_static:
            self.route = re.compile(self.convert_re(self.path))

    def match(self, url):
        m = self.route.match(url)
        if m:
            return m.groups()
        return None

    def convert_re(self, string):
        """
        将带动态参数的这个转化成正则
        >> > a = justsplit('/post/<id>/user/<wo>')
        >> > a
        '/post/(?P<id>\\w+)/user/(?P<wo>\\w+)'
        :param
        string:
        :return:
        """
        sp = re.compile(r'/').split(string)
        result = '/'
        for i in sp[1:]:
            if i.startswith('<'):
                result += r"(?P<{0}>\w+)".format(i[1:-1])
                result += '/'
            else:
                result += i
                result += '/'
        return ''.join(result)[:-1]

    def __call__(self, *args):
        """回调 将参数和执行的函数绑定在一起后执行"""

        return self.func(*args)

    def __str__(self):
        if self.is_static:
            return "Static route {}".format(self.path)
        return "Dynamic route {}".format(self.path)

    __repr__ = __str__


class StaticFileRoute:
    """将获取的静态文件的路由中的路径获取到
    ！ 这里可以拆出一个方法来动态的进行 类似于flask的urlfor
    """

    def __init__(self, decritory='static'):
        self.method = 'GET'
        self.is_static = True
        self.decritory = decritory
        self.route = re.compile('^/{}/(.+)$'.format(self.decritory))

    def match(self, url):
        """返回一个字符串"""
        if url.startswith('/{}'.format(self.decritory)):
            return (url[1:],)
        return None

    def __call__(self, url):
        """a/b/c --> a\\b\\c 用来符合操作系统标准"""
        resource = url.replace('/', '\\')
        #
        fpath = os.path.join(ctx.app.root, resource)
        if not os.path.isfile(fpath):
            raise notfound()
        # splittext 用来获取文件的后缀
        file = os.path.splitext(fpath)[1]
        # types_map用来将这个后缀转化为mime类型 默认为是octet-stream
        ctx.response.content_type = mimetypes.types_map.get(file, 'application/octet-stream')
        return static_stream(fpath)


class MultipartFile:
    """
    从字典中读取文件信息
    获取文件名
    文件对象
    """

    def __init__(self, storage):
        self.filename = storage.filename
        self.file = storage.file


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadTimeSignature


def open_session(secret, session):
    s = Serializer(secret_key=secret)
    try:
        session = s.loads(session)
        return session
    except BadTimeSignature:
        return False


class Request:
    def __init__(self, environ):
        self._environ = environ

    def _parse_input(self):
        """将数据转化出来"""

        def _convert(data):
            """拿出数据"""
            if isinstance(data, list):
                return [i.value for i in data]
            elif data.filename:
                return MultipartFile(data)
            return data.value

        # 将wsgi中的数据通过fieldstorage转化 keep_blank_values 代表能够进行迭代
        fs = cgi.FieldStorage(fp=self._environ['wsgi.input'], environ=self._environ, keep_blank_values=True)
        inputs = Dict()

        if fs.length > 0:
            for k in fs:
                inputs[k] = _convert(fs[k])
        return inputs

    def _get_raw_input(self):
        """拿到经过解析的数据"""
        if not hasattr(self, "_raw_input"):
            self._raw_input = self._parse_input()
        return self._raw_input

    def __getitem__(self, key):
        """
        >>> from io import BytesIO
        >>> b = '----WebKitFormBoundaryQQ3J8kPsjFpTmqNz'
        >>> pl = ['--%s' % b, 'Content-Disposition: form-data; name=\"name\"\n', 'Scofield', '--%s' % b, 'Content-Disposition: form-data; name=\"name\"\n','Lincoln', '--%s' % b, 'Content-Disposition: form-data; name=\"file\"; filename=\"test.txt\"', 'Content-Type: text/plain\n', 'just a test','--%s' % b, 'Content-Disposition: form-data; name=\"id\"\n', '4008009001', '--%s--' % b, '']
        >>> payload = '\n'.join(pl)
        >>> r = {'REQUEST_METHOD':'POST', 'CONTENT_LENGTH':str(len(payload)), 'CONTENT_TYPE':'multipart/form-data; boundary=%s' %b, 'wsgi.input':BytesIO(payload.encode())}
        >>> r.get('name')
        'Scofield'
        >>> r.gets('name')
        ['Scofield', 'Lincoln']
        >>> f = r.get('file')
        >>> f.filename
        'test.txt'
        >>> f.file.read()
        'just a test'
        :param key:
        :return:
        """
        r = self._get_raw_input()[key]
        if isinstance(r, list):
            return r[0]
        return r

    @property
    def json(self):
        r = self._get_raw_input()
        return [eval(i) for i in r.keys() if isinstance(i, str)]

    @property
    def form(self):
        """返回表单信息"""
        r = self._get_raw_input()
        return r

    def input(self, **kwargs):
        """如果获取的key不存在 使用这个默认给一个"""
        copy = Dict(**kwargs)
        r = self._get_raw_input()
        for k, v in r.items():
            copy[k] = v[0] if isinstance(v, list) else v

    @property
    def session(self):
        """获取request的session"""

        return open_session(ctx.config['secret_key'], self.cookie(' session'))

    def body(self):
        """获取body信息 -- 可以做成迭代器"""
        fp = self._environ['wsgi.input']
        return fp.read()

    ### 一些基本信息
    @property
    def remote_addr(self):
        """获取客户端ip"""
        return self._environ.get('REMOTE_ADDR', '0.0.0.0')

    @property
    def document_root(self):
        """网站根目录"""
        return self._environ.get('DOCUMENT_ROOT', '')

    @property
    def query_string(self):
        """查询字符串"""
        return self._environ.get('QUERY_STRING', '')

    @property
    def environ(self):
        return self._environ

    @property
    def request_method(self):
        return self._environ['REQUEST_METHOD']

    @property
    def path_info(self):
        """
        转化为可读的。
        >>> r = Request({'PATH_INFO': '/test/a%20b.html'})
        >>> r.path_info
        '/test/a b.html'
        :return:
        """
        return unquote(self._environ.get('PATH_INFO', ''))

    @property
    def host(self):
        return self._environ.get('HTTP_HOST', '')

    def _get_headers(self):
        # convert 'HTTP_ACCEPT_ENCODING' to 'ACCEPT-ENCODING'
        if not hasattr(self, '_headers'):
            headers = {}
            for k, v in self._environ.items():
                if not isinstance(v, str):
                    v = v.decode()
                if k.startwith('HTTP_'):
                    headers[k[5:].replace('_', '-').upper()] = v
            self._headers

    @property
    def headers(self):
        """
        获取http头信息 ，表示形式为XXX-XXX.

        >>> r = Request({'HTTP_USER_AGENT': 'Mozilla/5.0', 'HTTP_ACCEPT': 'text/html'})
        >>> H = r.headers
        >>> H['ACCEPT']
        u'text/html'
        >>> H['USER-AGENT']
        u'Mozilla/5.0'
        >>> L = H.items()
        >>> L.sort()
        >>> L
        [('ACCEPT', u'text/html'), ('USER-AGENT', u'Mozilla/5.0')]
        :return:
        """
        return dict(**self._get_headers())

    def header(self, header, default=None):
        """获取具体的一个 可以自定义默认值"""
        return self._get_headersg.get(header.upper(), default)

    def _get_cookies(self):
        """
        'HTTP_COOKIE': 'UM_distinctid=15c7b3a049547-08fef361539c6f-323f5e0f-144000-15c7b3a049666a;
        CNZZDATA1262121305=568492071-1496716091-%7C1496716211;
        ---->
        UM_distinctid:15c7b3a049547-08fef361539c6f-323f5e0f-144000-15c7b3a049666a
        :return:
        """
        if not hasattr(self, '_cookies'):
            cookies = {}
            cookies_str = self._environ.get('HTTP_COOKIE')
            if cookies_str:
                for c in cookies_str.split(';'):
                    key, value = c.split('=', 1)
                    cookies[key] = unquote(value)
            self._cookies = cookies
        return self._cookies

    @property
    def cookies(self):
        return Dict(**self._get_cookies())

    def cookie(self, name, default=None):
        return self._get_cookies().get(name, default)


class Response:
    def __init__(self):
        self._status = '200 OK'
        self._headers = {'CONTENT-TYPE': 'text/html; charset=utf-8'}
        # self._mimetype = 'text/html'

    @property
    def headers(self):
        """返回响应头"""
        header = [(_RESPONSE_HEADERS_DICT.get(k, k), v) for k, v in self._headers.items()]
        if hasattr(self, '_cookies'):
            for k in self._cookies:
                # 添加cookie 到header
                header.append(('Set-Cookie', k))
        header.append(_HEADER_X_POWERED_BY)
        return header

    def header(self, key):
        KEY = key.upper()
        if KEY not in _RESPONSE_HEADERS_DICT:
            return self._headers.get(KEY)
        return self._headers.get(key)

    def unset_header(self, key):
        """去掉key"""
        if key.upper() in _RESPONSE_HEADERS_DICT:
            del self._headers[key]

    def set_header(self, key, value):
        """设置key"""
        KEY = key.upper()
        if KEY not in _RESPONSE_HEADERS_DICT:
            KEY = key
        self._headers[KEY] = value

    def delete_cookie(self, key, path='/', domain=None):
        """删掉cookie"""
        self.set_cookie(key, expires=0, max_age=0, path=path, domain=domain)

    def set_cookie(self, key, value='', max_age=None, expires=None,
                   path='/', domain=None, secure=False, httponly=False):
        """设置cookie 用来追踪状态"""
        if not hasattr(self, '_cookies'):
            self._cookies = []
        value = dump_cookie(
            key,
            value=value,
            max_age=max_age,
            expires=expires,
            path=path,
            domain=domain,
            secure=secure,
            httponly=httponly,
            charset='utf-8'
        )
        self._cookies.append(value)

    # @property
    # def mimetype(self):
    #     return self._mimetype
    #
    # @mimetype.setter
    # def mimetype(self, mtype):
    #     self.mimetype = mtype
    #     self.content_type = mtype


    @property
    def content_type(self):
        return self.header('CONTENT-TYPE')

    @content_type.setter
    def content_type(self, value):
        """设置content type"""
        if value:
            self.set_header('CONTENT-TYPE', value)
        else:
            self.unset_header('CONTENT-TYPE')

    @property
    def content_length(self):
        return self.header('CONTENT-LENGTH')

    @content_length.setter
    def content_length(self, length):
        self.set_header('CONTENT-LENGTH', str(length))

    @property
    def status_code(self):
        """
        >>> r = Response()
        >>> r.status_code
        200
        >>> r.status = 404
        >>> r.status_code
        404
        >>> r.status = '500 Internal Error'
        >>> r.status_code
        500
        :return:
        """
        return int(self._status[:3])

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):

        if isinstance(status, int):
            if 100 <= status <= 999:
                value = _RESPONSE_STATUSES.get(status, '')
                if value:
                    self._status = '{code} {status}'.format(code=status, status=value)
                else:
                    self._status = str(status)
        elif isinstance(status, str):
            if _RE_RESPONSE_STATUS.match(status):
                self._status = status
            else:
                raise ValueError("Bad request code:".format(status))
        else:
            raise ValueError("Bad request code:".format(status))


class TemplateEngine:
    """Base template engine"""

    def __call__(self, path, model):
        return "abstract class"


class Jinja2TempplateEngine(TemplateEngine):
    """使用jinja2 渲染"""

    def __init__(self, tmp_folder, **kw):
        """导入jinja2 传入要渲染的文件夹名 然后设置自动转义"""
        from jinja2 import Environment, FileSystemLoader
        if 'autoescape' not in kw:
            kw['autoescape'] = True
        self._env = Environment(loader=FileSystemLoader(tmp_folder), **kw)
        self._env.globals['url_for'] = url_for


    def add_filter(self, name, filter):
        """增加过滤函数"""
        self._env.filters[name] = filter

    def __call__(self, path, data):
        return self._env.get_template(path).render(**data).encode()


class Render:
    """渲染"""
    engine = Jinja2TempplateEngine('templates')

    def __init__(self, tmp='templates'):
        self.path = os.path.join(os.path.abspath('{}'.format(tmp)))
        if os.path.isdir(self.path):
            logging.info("Template folder is {}".format(self.path))
            Render.engine = Jinja2TempplateEngine(self.path)
        else:
            raise FileExistsError("{} not a folder".format(tmp))

    def add_filter(self, name, filter):
        self.engine.add_filter(name, filter)

    def render_template(self, template, **kw):
        return self.engine(template, kw)


class WSGIApplication:
    static_folder = 'static'

    def __init__(self, root=None, **kw):
        self._running = False
        self._tem_engine = None

        self.config = {}
        self._get_static = {}
        self._post_static = {}
        self._get_dynamic = []
        self._post_dynamic = []
        if root is None:
            self.root = os.getcwd()

    @property
    def _check_not_running(self):
        if self._running:
            raise RuntimeError("Cannot modify wsgiapplication ...")

    @property
    def template_engine(self):
        return self._tem_engine

    @template_engine.setter
    def template_engine(self, engine):
        """载入模版引擎"""
        self._check_not_running
        self._tem_engine = engine

    def save_session(self, response, session):
        """
        应用程序端需要将ctx session 写入
        通过这个函数在cookie中设置session
        :param secret: 密钥
        :param expires: 有效时间
        :return:
        """
        secret = self.config.get('secret_key')
        if secret is None:
            raise RuntimeError("You must set secret key in your application")
        s = Serializer(secret_key=secret, expires_in=3600)
        s_cookies = s.dumps(session)
        response.set_cookie('session', s_cookies)

    def process_response(self, response):
        """处理一些额外的载入工作"""
        session = ctx.session
        if session is not None:
            self.save_session(response, session)
        return response

    def route(self, route, methods=['GET']):
        """加入路由 默认是get"""

        def _route(func):
            func.__web_route__ = route
            func.__web_method__ = methods
            self.add_url(func)
            return func

        return _route

    def add_url(self, func):
        """将func的路由 。。参数加入到环字典中"""
        self._check_not_running
        route = Route(func)
        s_method = {
            'GET': self._get_static,
            'POST': self._post_static,
        }
        d_method = {
            'GET': self._get_dynamic,
            'POST': self._post_dynamic,
        }
        if route.is_static:
            for i in route.method:
                s_method[i][route.path] = route
                # logging.info("Add static route func ({}) --> {}".format(func.__name__, func.__web_route__))
        else:
            for i in route.method:
                d_method[i].append(route)
                # logging.info("Add dynamic route func ({}) --> {}".format(func.__name__, func.__web_route__))

    def run(self, host='127.0.0.1', port=5000, debug=False):
        from werkzeug.serving import run_simple, run_with_reloader
        return run_simple(host, port, self.wsgi_app(), use_debugger=debug, use_reloader=debug)

    def wsgi_app(self):
        self._check_not_running

        self._get_dynamic.append(StaticFileRoute(self.static_folder))

        self._running = True

        _app = Dict(root=self.root)

        def route_func():
            method = ctx.request.request_method
            path = ctx.request.path_info
            if method == 'GET':
                fn = self._get_static.get(path, None)
                if fn:
                    return fn()
                for fn in self._get_dynamic:

                    args = fn.match(path)

                    if args:
                        return fn(*args)
                raise notfound()
            if method == 'POST':
                fn = self._post_static.get(path, None)
                if fn:
                    return fn()
                for fn in self._post_dynamic:
                    args = fn.match(path)
                    if args:
                        return fn(args)
                raise notfound()
            raise bad_request()

        def wsgi(environ, start_response):
            ctx.app = _app
            ctx.config = self.config
            ctx.request = Request(environ)
            ctx.session = {}
            # 这里应该给一个make response 的函数
            response = ctx.response = Response()

            try:
                r_func = route_func()

                if isinstance(r_func, str):
                    r_func = r_func.encode('ascii')
                elif r_func is None:
                    return []
                response = self.process_response(response)
                start_response(response.status, response.headers)
                return [r_func]
            except RedirectError as e:
                response.set_header('Location', e.location)
                start_response(response.status, response.headers)
                return []
            finally:
                del ctx.app
                del ctx.request
                del ctx.response

        return wsgi
