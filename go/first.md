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

    go 来获取数据。 python 来统计显示


### goroutine


**goroutine 是go很大的一个特点。在一些任务中轻松开启大量的goroutine （只耗费很少的内存）来对任务进行处理。
同时可以充分利用多核。（在这个摩尔定律失效，cpu核数越来越多的情况下优点很大）**

goroutine 的特点

    有自己的调用栈,这个栈会进行动态伸缩
    它是非常轻量的，开大量的goroutine 完全可以
    不是线程

    通过channel 来通信

首先是要明白并发 和  并行。 并发
主要区别就是并发是同一个时间段同时执行，并行是同一个时刻执行。

实现并发的手段就是 快速切换，利用的是cpu 和 io 速度的不一致。
这里用户空间的线程 和 内核的线程对应的关系有 N:1,1:1和M:N

    N:1是说，多个（N）用户线程始终在一个内核线程上跑，context上下文切换确实很快，但是无法真正的利用多核。
    1：1是说，一个用户线程就只在一个内核线程上跑，这时可以利用多核，但是上下文switch很慢。
    M:N是说， 多个goroutine在多个内核线程上跑，这个看似可以集齐上面两者的优势，但是无疑增加了调度的难度

    python 的coroutine应该是 n ：1的模型。导致使用的时候都是在每一个核上部署一个任务，浪费了很多的资源

go 的调度器有三个结构 m p g

      m 是真正执行的线程。(内核线程)
      g 保存了一段程序的上下文信息。
      p 是将g 放在一个m上去执行。（调度的上下文）


参考

https://www.youtube.com/watch?v=f6kdp27TYZs    

http://www.sizeofvoid.net/goroutine-under-the-hood/













