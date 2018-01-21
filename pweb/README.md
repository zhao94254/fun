## http 理解     

包含http协议中常用的一些东西。以及python在做后端的时候要用到的一些东西。    






### server文件夹下是一个简单的wsgi 框架，用来理解后台的整个流程。
### example 是使用的例子


Request --> (wsgi) 请求处理 (wsgi) -->Response  

框架的主要功能就是将用户请求转化为wsgi格式的，  
将经过逻辑代码的处理后的请求再返回。  




example 中是一个类植物大战僵尸的游戏。
前后端分离，后端使用面向对象的思维进行抽象，进行计算数据，前台只需要显示。
代码清晰明了，用来复习面向对象编程。

![image](http://pyblog-10073407.image.myqcloud.com/postimage1508203711?imageView2/0/w/450/h/400 "enter image title here")    




concurrency 下是python 或者go 的一些测试    

stress.py 测试工具。

















