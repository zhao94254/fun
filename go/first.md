**语言只是一个用来实现的工具，在合适的场景下选用合适的语言。之前做了一个网络相关的东西。用golang
是更好的选择。 正好想学学新东西。**   

和python相比 编译型静态语言， 速度快。并发支持特别好。 缺点就是生态没有python好。 不过相同点都是函数
是一等公民。写程序的时候大体思路都是差不太多的。
 
快速上手。 通过几个小函数来熟悉。


    fib 
    
    python
    
    def fib(x):
        if x < 2:
            return x
        return fib(x-1) + fib(x-2)
    
    
    go
    
    递归
    func fib(x int)(int)
       if x < 2{
          return x
       }
       return fib(x-1)+fib(x-2)
    }
    
    迭代
    func fibIter(x int)(int){
       i := 1
       a, b := 0, 1
       for i < x  {
          i += 1
          a, b = b, a+b
       }
       return b
    }
    
    执行计算密集任务时  
    go fib(35)        0.09s
    python fib(35) 7.5s

**如果是io密集的任务的话差距就不会很大了。**


go 和 python 写起来差距比较大的几点。

由于是静态类型，每个变量的后面都有一个类型定义。
     
     var a int
     var  b []string
     a := 1 

定义常量

    const xx = 2

这些在python 中也可以通过一些方法来魔改。 强行把一段代码变成静态的。 思路就是对变量增加类型注解，然后判断类型是否是注解的类型。不过这样做就放弃了python的很多特点了。


go 中很大的一个特点就是gorotine。  
    
    func mulfetch(url string)  {
       start := time.Now()
       var s string
       ch := make(chan string) //启动一个gorotine
       if !strings.HasPrefix(url, "http://"){
          url = "http://" + url
       }
       for i:=0;i<10 ;i++  {
          s = url + strconv.Itoa(i)  // 将 数字转为 字符 用来拼接
          fmt.Println(s)
          go fetchone(s, ch)
       }
       for i:=0;i<10 ;i++  {
          fmt.Println(<-ch) // 通过这个ch 来接收值
       }
       fmt.Printf("%.2fs elapsed\n", time.Since(start).Seconds())
    }
    
    mulfetch(“www.yunxcloud.cn/post")

使用起来很方便。


    todo 
    了解gorotine的背后工作机制

    go 来获取数据。 python 来统计显示















