### 首先来明白什么是声明式编程。    

声明式编程就是我们在使用的时候将程序的目的提供出来，其它都不需要去考虑。    
系统将这些目的转化为具体的执行，并且会找到最好的执行路径来获取结果。
而命令式语言的话就是需要程序员来手动告诉机器如何执行，这里人写出来的    
不一定会比优化器写出来的更好，而且写起来也很麻烦。

sql xpath 都是声明式编程的一个示例，我们使用的时候只需要关心结果就可以了，    
降低了心智负担。 具体的处理由数据库查询器来做。


我们可以通过解析一个简单的sql来加深这个理解。



 首先来创建一个表

有name，age， location 三列。写一个创建表的函数。


    def create_table(row, data):
            """row[0] 表名 row[1:] 列名 data 要插入的数据"""
            table_row = namedtuple(row[0], row[1:])
            table = [table_row(*i) for i in data]
            return table


传入数据

    row = ('Row', 'name', 'age', 'location')
    data = [('jack', 12, 'beijing'),
            ('rose', 15, 'shanghai'),
            ('aha', 20, 'taiyuan'),
            ('liuxing', 18, 'changzhi'),
            ('luben', 18, 'shanghai'),
            ('douchuan', 18, 'changzhi'),
            ('heihai', 18, 'shanghai'),]

我们要的是

    select xx from yy where zz

定义一个select 函数，传入要获取的列名，表名，条件

    def select(name, table, condition):
    """ select name from table where condition"""
        res = []
        name = split_name(name)
        rows = copy.deepcopy(table_to_dict(table))
        for j, i in enumerate(table_to_dict(table)):
             if filter(condition, i):
                    res.append(get_data(name,i))
         return res[0] if len(res) == 1 else res

将表传入，然后获取每一行的数据，然后按照输入的条件将结果筛出来。

还需要一个filter函数，为了获取多列还需要一个处理name的函数。

处理name的比较简单，就是将name按照逗号分开，需要考虑的一点是有的时候会   
输入多个空格，这个要处理下，否则后面无法匹配。



    def split_name(name):
        return sum([i.split() for i in name.split(',')], [])

filter函数的话传入一个字典，直接执行条件就好了

    def filter(condition, row):
          if condition:
               return eval(condition, row)
           else:
                return True


使用

    print(select('name,age', table, "age != 18"))
    print(select('name,age', table, "age >= 18 and location=='changzhi'"))


通过这些大体可以理解声明式编程是什么了。简单来说就是给一个好的抽象，让使用者使用的时   
候只需要来考虑结果，不用考虑过程。


为什么声明式更适用于并行，而命令式并行起来更麻烦？


为什么声明性语言往往适合于并行执行，命令代码很难在多个内核和多个机器之间并行化？    
 - 阿莱克西斯的回答 - 知乎 https://www.zhihu.com/question/268062648/answer/332762202


本着不懂就问的原则，这里是一个解释的比较清楚的回答


简单来说 如果要并行运行一个系统，就要考虑到这个系统中的函数之间是否有依赖，
举例来说 如果A函数 需要 B 函数的结果来处理，这就是一个依赖。 有依赖的必须是    
在一个时间线上，反之则不需要。

串行解决就是A B 在一个机器上执行，B执行完执行A。

或者就是并行在 A B 在两台机器上，通过通信保证先后。

设计一个系统要 了解我们的目标，使用那些函数来组成一个计算达成目标，如何安排    
一个良好的时间线。  使用命令式的时候三点都需要考虑，而声明式的时候只需要考虑    
第一点。其它的东西由系统来考虑。

虽然使用声明式的时候只需要考虑结果，但是明白sql 是怎么执行的是很重要的，这直    
接决定了你的一条sql是执行1秒 还是 1分钟。


https://github.com/zhao94254/fun/blob/master/other/parsesql.py










