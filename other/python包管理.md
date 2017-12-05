### 模块  
任何python文件都可以被视为一个模块  

    # test.py
    def testa(x):
        pass

可以通过两种方式导入  

    import test
    a = test.testa('a')
    from test import testa
    b = testa('a')
    
#### 命名空间

下面的两个变量各自在各自的作用域中是不影响的。  

    # testa.py
    x = 'testa'
    # testb.py
    x = 'testb'
    
#### 模块的执行

当一个模块被导入的时候，这个模块中的所有的语句都被执行。  

    testb.py
    def test():
        print('test')
    test()
        
    import testb
    output 'test'
        
    from module import x 从module 中导入x函数 或者类
    from module import *  导入所有的。要尽量避免使用    
    
    # 下面这三种没什么区别    
    import math as m
    from math import cos, sin
    from math import *

**在导入的时候总是会执行整个文件
每个模块都是一个孤立的环境**

#### 模块命名  

    good.py # good
    2bad.py # bad

模块名应该是可以让人看出模块功能的。  
避免使用 non-ascii 字符。  
模块名应该是简洁的 使用小写字母  

    foo.py # good
    MyFooModule.py # bad

对于私有的模块使用下划线开头。
不要把自己的模块名起的和标准库的一样。  

#### 模块搜索路径  
    
    # 如果要导入的模块不在这个列表里就无法被搜索到。
    >>>import sys
    >>> sys.path
    ['', 'E:\\py3\\python35.zip',
     'E:\\py3\\DLLs',
      'E:\\py3\\lib', 
      'E:\\py3',
       'E:\\py3\\lib\\site-packages']
    
    # 有时候我们可以自己添加
    import sys
    sys.path.append("/project/foo/myfiles")
 
#### 模块缓存  

模块只被加载一次
 
    >>> import spam
    >>> import sys
    >>> 'spam' in sys.modules
    True
    >>> sys.modules['spam']
    <module 'spam' from 'spam.py'>

#### 模块重载  

在python2中，设置默认的编码需要这样：  

    import sys
    reload（sys）
    sys.setdefalutencoding('utf-8')
    
在reload前，这个模块必须被import过，之所以需要reload时因为这个sys在这里不是第一次调用的，这里调用的是缓存中的，  
具体来说这只是一个引用。通过reload才可以重新设置。 除了特殊情况尽量不要使用reload。  

#### __main__    
在python中我们经常这么写：  
       
    if __name__ == '__main__':
        do something

这是因为如果一个模块被引用了，这个模块所有的东西都会被执行一次，在调用的时候这个__name__是模块的名字。在执行的时候  
这个名字是__main__。  


#### 包  
对于更复杂点的程序，就需要把程序组织为包结构。  

    像这样：  
    first/
        __init__.py
        testa.py
        second/
             __init__.py
            testb.py
    
    这个__init__文件是必不可少的。
    
#### 为什么要使用包？  

试想，一个文件中包含20个类，10000行代码好还是 20个文件，一个文件一个类好？  
毫无疑问肯定是后者更好。 当要多个人共同开发一个程序时，将不同的功能划分在不同的模块中  
每个人去开发一个功能 开发效率会提升很多。但是如果是在一个文件中，多个人一起开发的时候  
光来回修改 来回查找代码就很痛苦了。  

模块控制  

    # foo.py
    __all__ = ['Foo']
    class Foo(object):
        pass
        
    # bar.py
    __all__ = ['Bar']
    class Bar(object):
        pass
    
    __all__ 中定义了那些， 那些就可以被 from xx import * 导入  
    
    # __init__.py
    from .foo import *
    from .bar import *
    __all__ = (foo.__all__ + bar.__all__)
    
    # asyncio 是一个很好的例子。
    
也可以通过装饰器来实现  

    # spam/__init__.py
    __all__ = []
    def export(defn):
        globals()[defn.__name__] = defn
        __all__.append(defn.__name__)
        return defn
        
    from . import foo
    @export
    class A:
        pass 
    上面的方法等同于 __all__ = ['A']

pathonpath 环境变量
env pythonpath=/foo:/bar python3 -s  
这样子就把需要添加的路径加入了sys.path  
    
    # 模块的属性
    __name__ # Module name
    __file__  # Associated source file (if any)
    __doc__ # Doc string
    __path__ # Package path
    __package__ # Package name
    __spec__ # Module spec

要注意循环引用  
    
    # foo.py
    import bar
    # bar.py
    import bar
    
再谈reload。
    
    # before
    # testf.py
    class Spam:
        def yow(self):
            print("yow")
    import testf
    a=testf.Spam()
    
    class Spam:
        def yow(self):
            print("new yow")
    
    reload(spam)
    b = testf.Spam()
    a.yow() # yow
    b.yow() # new yow
    
    上面已经存在的a 的实例用的还是之前的。
    b则是新的  
    >>> a.__class__
    <class 'foo.testf.Spam'>
    >>> b.__class__
    <class 'foo.testf.Spam'>
    >>> type(a)
    <class 'foo.testf.Spam'>
    >>> type(b)
    <class 'foo.testf.Spam'>
    >>> type(a) == type(b)
    False
    
这也是为什么要尽量避免使用reload的原因。


#### 模块寻找  

    使用 imporlib.util.find_spec 
    
    def find_spec(modname):
        for imp in sys.meta_path:
            spec = imp.find_spec(modname)
            if spec:
                return spec
        return None
    
    find_spec('sys')
    find_spec('socket')

**在好多库里能看到这种写法**  

    try:
        __import__('watchdog.observers')
    except ImportError:
        reloader_loops['auto'] = reloader_loops['stat']
    else:
        reloader_loops['auto'] = reloader_loops['watchdog']
     
    先去寻找 watchdog.observers 如果没找到就去找其它的。


#### 通过一些方法还可以使代码从远程加载，或者从redis中加载。  


#### 如何将文件夹加入到sys.path  

在写程序的时候经常要导入一些我们自己的文件，有两种方法可以  
1. 添加新目录到pythonpath 的环境变量中  
2. 创建一个.pth 的文件，放在site-packages中。  

也可以写代码来手动调节这个sys.path 的值。  

    import sys
    sys. path. insert(0, ' /some/dir' )
    sys. path. insert(0, ' /other/dir' )

上面这种方法是行得通的。但是在实践的时候难免会遇到需要修改的情况。这时这样就不是一个  
好的选择。更好的做法是将这些path配置在一个文件中，或者构造一个合适的绝对路径。  




    
    
    
    
    
    
    
    
    
    






  




    














