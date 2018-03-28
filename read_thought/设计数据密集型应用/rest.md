
**web中最主要的两点 资源（文字 图片 视频。。）和表述（展现的一种手段，例如 json xml text。。）
主要是三个东西来支撑上面两点，分别是：url http html分别用来 显示资源位置， 传输资源， 显示资源**
	
**例如：**

A的浏览器向https://www.baidu.com发送一条http请求，这个https://www.baidu.com就是url ，利用http协议传输，上面的http后面的s意味着加了一    
个加密层，用来保护数据不被篡改。服务器向浏览器返回资源后，浏览器解析，生成页面。浏览器生成就是所谓的表述。http层是在计算机网络模型的最顶层 应     
用层，在http连接开始之前，还有很多的工作。从最底层物理层开始 数据通过有线或者是无线的方式来给上层提供服务，数据链路层保证可靠点的传输。然后到    
了ip层，计算机通过ip地址，来知道服务器在哪一个地方，从而可以获取数据。 但是浏览器发送的是一个url，这时就要通过dns 发送一个udp包来获取ip。获    
取ip后还需要加上一个相应的端口。http的端口是80，通过ip加上端口号形成套接字，从而能够发送数据了。

**http协议的一大特性（无状态性）**    

服务器不需要关心客户端的状态

**Rest（表现层状态转移）六大特性**

    服务器 客户端 --有明确界限
    无状态
    缓存
    接口统一
    系统分层
    按需代码

**设计api**    

很多人对restful接口有一个误解，认为restful = endpoint + 返回json数据，这也就导致了一些奇葩api被设计出来，比如 返回的都是状态码200，在content     
中添加其它信息。这个理解是错误的，实现的时候要考虑到很多隐式的要求，要符合标准。

下图是HTTP协议提供的一些方法：   

![](http://pyblog-10073407.image.myqcloud.com/postimage1522203317?imageView2/0/w/450/h/400)

**幂等性：** 这个概念的意思是多次操作是否和一次操作的结果相同，如果相同就是幂等的。

**headers**   

    accept：决定服务端返回什么content，是xml 还是 json 还是 text
    
**常用status code**

* 200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
* 201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
* 202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
* 204 NO CONTENT - [DELETE]：用户删除数据成功。
* 302 Move temporarily请求的资源临时从不同的 URI响应请求。由于这样的重定向是临时的，客户端应当继续向原有地址发送以后的请求。     
   只有在Cache-Control或Expires中进行了指定的情况下，这个响应才是可缓存的。
* 304 Not Modified  如果客户端发送了一个带条件的 GET 请求且该请求已被允许，而文档的内容（自上次访问以来或者根据请求的条件）并没有改变，     
    则服务器应当返回这个状态码。
* 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
* 401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
* 403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
* 404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
* 406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
* 410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
* 412 Precondition Failed 服务器在验证在请求的头字段中给出先决条件时，没能满足其中的一个或多个。
* 422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
* 500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。
    
**安全性的考虑**    

  这里的安全性不只是简单的加密解密，还有其他的要求    
  
1. 验证请求数据，验证header uri body，如果不合法直接返回对应的错误码。减少资源浪费
2. 验证数据的完整性，在rest api对数据进行修改的时候，要可以保证要修改的数据和服务器的数据一致。这个通过一个标记来实现。 http中提供了一个etag    
 来判断是否一致。如果不一致返回对应的错误码。
3. 访问控制。 操作是权限的，不同权限的用户有不同权限的操作。 最基本的就是认证用户，常用的方法有 basic auth，oauth。核心的思路都是判断此用户是    
否是合法的用户。 basic auth将用户密码进行处理然后放在网络中。这是一种最不安全的方式。
    

**部署**    

拿一个博客系统来说，一开始是这样的：    

User — >(req) —>  <load balance , nginx proxy> —> Api server     

现在问题来了， 需要对用户行为进行一些监控，统计，从很多维度来分析。 这是又需要添加用户行为的api， 并且这些api是和之前的api在逻辑上是完全无关的。     
逻辑上完全不相干的系统按照上面的方式的话就被整个包在一起了。     

再进一步：    

                                 <load balance , nginx proxy> —> Application Api server 
    User — >(req) —>
                                 <load balance , nginx proxy> —> Statistic Api server 


不同类型的服务部署在不同的逻辑内。 并且在一些高峰期可以把一些不是特别重要的服务的资源放出来，供其他的服务使用。    


用户的请求过来的整个流程：   

    request -> pre-processing -> processing -> post-processing -> response    

其中 processing 是真正处理业务代码的过程，设计的好的系统应该把这些额外的组件做成中间件来使用。写具体业务的时候不需要去考虑其他东西。   


拿上面的博客再来考虑下具体的过程

* 速率控制： 比如 用户每分钟只能发一篇文章， 只能对10个文章评论。如果太多了返回对应的错误码

* 解析和验证： 对用户的request进行解析，如果有一些请求格式不符合直接拒绝

* 资源控制： 管理员可以很方便的对资源进行一些管理，比如要删除 一篇文章，或者是这篇文章只能在特定的时刻显示
 
* 用户认证： 对于一些操作是必须认证用户后才可以继续的，在api中应该使用token来对用户做认证
 
* 对一个操作权限控制： 有一些操作是不同用户的权限不同，如果一个用户进行一个无权限的操作，在这一步直接被拒绝
 
* 有条件的请求： 如果用户的一个request是 put操作，对已有的数据进行修改，则需要通过（if-match / if-modified）来做一个判断。保证客户端    
更新数据的时候使用的是和服务器版本一样的，否则应该返回412 precondition failed
 
* 具体的处理： 这里就是具体的业务逻辑了

* 在访问的出口，如果是get 操作， 通过 if-none-match/if-not-modified 来判断数据是否是可以从本地缓存直接读取的，如果可以就返回304，    
  省去了从服务器加载。
 
* 将响应进行格式化返回： 这一步将结果转化为合适的格式返回给用户

* 序列化： 用web的话一般给返回json， 其它的服务返回客户端建议的

* 文档：   资源都是通过url来访问的， 可以根据url将文档提供出来。 文档就是一个说明书，是使用者和api作者直接的一个契约， 写出一个清晰易懂的    
  文档是很重要的。


在python中有一基于flask的api库， 已经包含了上述很多功能，以下是一些功能的介绍：   


认证：

因为 REST 架构基于 HTTP 协议，所以发送密令的最佳方式是使用 HTTP 认证，基本认证
和摘要认证都可以。在 HTTP 认证中，用户密令包含在请求的 Authorization 首部中。
使用flask-httpauth可以很简单实现认证

	auth = HTTPBasicAuth()
	@auth.verify_password 确认密码或者token
	@auth.login_required  确认用户是否通过了认证
	
认证方式是将用户名和密码通过b64编码，加到authorization头中
在header中可以找到这样一条信息 Authorization:Basic ***********
使用requests 和 base64可以直接很方便的在客户端使用

	from requests import get, post
	import base64

	code = base64.decode(用户名 密码)
	header = {'Authorization':code}
	get('url', headers=header)

认证完成后需要资源，可以选择使用三方库自动生成（自己定义schema），也可以手动生成
手动将资源在模型类下生成为json格式的：

	def to_json(self):
		 json_post = {
		 'url': url_for('api.get_post', id=self.id, _external=True),
		 'body': self.body,
		 'body_html': self.body_html,
		 'timestamp': self.timestamp,
		 'author': url_for('api.get_user', id=self.author_id,
		 _external=True),
		 'comments': url_for('api.get_post_comments', id=self.id,
		 _external=True)
		 'comment_count': self.comments.count()
		 }
		 return json_post

    flask_restless

	初始化
	manager = APIManager(app, flask_sqlalchemy_db=db)

	from my_app import manager
	需要生成的资源
	manager.create_api(Product, methods=['GET', 'POST', 'DELETE'])
	manager.create_api(Category, methods=['GET', 'POST', 'DELETE'])	
	使用：	 
	import requests
	import json
	res = requests.get('http://127.0.0.1:5000/api/category')
	res.json()
	{u'total_pages': 0, u'objects': [], u'num_results': 0, u'page': 1}

但是使用这样的方法有一个不好的地方，这样显示的是数据库的模型，但是用户
并不关心数据库是怎么样的。要面向用户设计

有一个更好的扩展 flask-restful

	from flask_restful import Api
	from flask_restful import reqparse, fields, marshal_with

	api = Api(app)

	这是实现（这里可以很简单的实现对资源的控制 和 用户的认证）：
	def dispatch_request(self, *args, **kwargs):
        # Taken from flask
        #noinspection PyUnresolvedReferences
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == 'HEAD':
            meth = getattr(self, 'get', None)
        assert meth is not None, 'Unimplemented method %r' % request.method

        for decorator in self.method_decorators:
            meth = decorator(meth)
        resp = meth(*args, **kwargs)
	
	自定义
	
	class Resource(restful.Resource)
		version = 'v1'
		method_decorators = []
		required_scopes = {}

自定义自己的数据格式,fields提供了不同的方法能够将数据库中的数据转化为
我们规定的格式。

	class APISchema():
		"""describes input and output formats for resources,
		and parser deals with arguments to the api.
		"""
		get_fields = {
			'id': fields.Integer,
			'created': fields.DateTime(dt_format='iso8601')
		}

		def __init__(self):
			self.parser = reqparse.RequestParser()

		def parse_args(self):
			return self.parser.parse_args()

然后就可以实现自己想显示的格式了,例如：


	class User(Resource):
		schema = Schema()
		model = models.User
		/#marshal_with装饰器用来将输出的数据为我们定义的格式。
		@marshal_with(schema.get_fields)
		def get(self, id=None):
			user = self.model.get_by_id(id)
			data = {
				'id': user.id,
				'email': user.email,
				'username': user.username,
				'is_admin': user.is_admin,
				'profile': user.profile,
			}
			return data

		def post(self):
			self.schema.auth_user()
			return {'email':g.current_user.email}

    # 添加定义的url， 做版本控制的时候一般通过在url中加版本号来实现
    api.add_resource(User, '/v1/user', '/v1/user/<int:id>')



















