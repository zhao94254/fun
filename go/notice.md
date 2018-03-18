### Go常见的一些坑    


从其它语言上手写go的时候要注意到的一些东西     

一些很容易发现的坑

1. 运行的这个go文件 package必须为main，入口函数是main函数。在python中并没有这个限制。    
2. 大括号必须是这样子的

        func main(){
            println("hello world")
        }

        而不是
        
        func main()				
        {
            println("hello world")
        }

3. 除了全局变量外的变量都必须使用， import的包也必须被使用。

        import "fmt"
        import "time" // 报错
        import _ "time" // 加一个下划线就不会报错
        var wtf int
        
        func main()  {
            var fortest int // 报错 
            _ = fortest // 可以这样子来引用一下，这个下划线和python的是一样的
            fmt.Println("wtf")
        }


4. go中的简短命名的一些坑。

        C := 33 // 全局无法使用简短命名
        func main()  {
            S := 2
            S := 3 // 报错，不能单独为一个变量声明新的变量
            S, D := 3, 4
            fmt.Println("wtf", S, D)
        }

5. struct相关

        type fortest struct {
            res int
        }
        
        fortest.res := 100 // 报错
        
        var test fortest
        test.res = 100

6. nil 相关

        在go中 interface、function、pointer、map、slice 和 channel 默认值是 nil
        
        显式类型的变量无法用nil来初始化
        var x = nil // 报错
        var x interface{} = nil // 需要指明

7. map 相关

        map 直接使用的时候会报错
        
        var m map[string]int  // 默认是nil 直接用会报错
        m := make(map[string]int) // 需要make一下使用
        
        另外 cap 无法检查 map给分配的容量大小
    
        检查一个key 是否在map中
        
        func InMap(m map[string]string, k string)  {
            if _, ok := m[k]; !ok{
                fmt.Println(k, "not in map")
            }
        }
        
        并发使用一个map的时候会报错，需要手动加锁
        
    
8. string相关

        更新字符串中的字母是不允许的。这一点和python是一样的
        可以将string转为[]byte来解决
        
        s := "wtf"
        sByte := []byte(s)
        sByte[2]='s' // 这里是rune类型的
        fmt.Println(string(sByte))
        
        但是上面这种方法是无法将字符串中的某一个字符变成汉字的。原因是因为
        一个汉字编码占了多个字节， 使用上面的方法会报这个错误
        
        .\notice.go:23:13: constant 21734 overflows byte
        
        解决方案：
        
        func changeStr(s,y string, i int)  {
            sByte := []rune(s)
            fy := []rune(y)
            if 0 < i && i <len(s){
                sByte[i] = fy[0]
                fmt.Println(string(sByte))
            }else{
                fmt.Println("超过索引范围")
            }
        }
        
        字符串的长度
        
        s := "我"
        fmt.Println(utf8.RuneCountInString(s)) // 1  这里是rune的长度
        fmt.Println(len(s)) // 3 这里返回的是byte的长度
        
        s := "é"
        fmt.Println(utf8.RuneCountInString(s)) // 2  这里是rune的长度
        
   

一些特别坑的问题

1. 运行时变量被覆盖掉了

        func main()  {
            test1 := 100
            {
                fmt.Println(test1) // 100
                test1 := 1000
                fmt.Println(test1) // 1000
            }
            fmt.Println(test1) // 这里并不是1000，而是100
        }
    
        要注意的是 使用简短声明的时候 test1变量只在里面的那个代码块作用
        在代码块内部是修改后的值（当时写一个函数被这个坑了好久。。）
        对同一个变量使用简短声明的时候并不会抛那个给已有变量声明新变量的错误。
        但是如果粗心的话当程序跑起来才会发现和预期不一致的结果
        
        解决这种问题的方案是使用go自带的工具来检查
        
        C:\Users\pengyun\Desktop\>go tool vet -shadow notice.go
        notice.go:19: declaration of "test1" shadows declaration at notice.go:16
        
        上面这种方法不会覆盖全部的， 这时需要使用go-nyet 来检查
    
2. 数组传递

        // 数组使用值拷贝传参，这里和python的list是不一样的，python传入的
        // 时候传入的是一个引用，对这个list修改是对内存中的这个值有影响的。
        func main() {
            x := [3]int{1,2,3}
        
            func(arr [3]int) {
                arr[0] = 7
                fmt.Println(arr)	// [7 2 3]
            }(x)
            fmt.Println(x)			// [1 2 3]	// 并不是你以为的 [7 2 3]
        }
        
        对原数据进行修改
        
        // 传址会修改原数据
        func main() {
            x := [3]int{1,2,3}
        
            func(arr *[3]int) {
                (*arr)[0] = 7	
                fmt.Println(arr)	// &[7 2 3]
            }(&x)
            fmt.Println(x)	// [7 2 3]
        }
        
        // 会修改 slice 的底层 array，从而修改 slice
        func main() {
            x := []int{1, 2, 3}
            func(arr []int) {
                arr[0] = 7
                fmt.Println(x)	// [7 2 3]
            }(x)
            fmt.Println(x)	// [7 2 3]
        }
        
3. go中的range 和 python的enumerate 一样，会带一个索引