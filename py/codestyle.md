### python 代码风格

命名： 清晰易懂，代码风格要一致

函数： 函数是抽象的主要机制，最好一个函数只做一件事。便于组合 复用。

目的： 每一行代码应该有一个明确的目的，减少冗余的代码。

简洁： 代码应该是简洁明了的。

变量命名

Good

	goal, score, opp_score = 1 00, 0, 0
	greeting = ' hello world'
	is_even = lambda x: x % 2

Bad

	a, b, m = 1 00, 0, 0
	thing = ' hello world'
	stuff = lambda x: x % 2

### 注意字母和数字

当很明确一个字母是做什么的时候，使用缩写的可以的。

Good

	i = 0 # a counter for a loop
	x, y = 0, 0 # x and y coordinates
	p, q = 5, 1 7 # mathematical names in the context of the question
	一般来说 i , j , k是循环中最常用的。

Bad

	o = O + 4 # letter ' O' or number 0?
	l = l + 5 # letter ' l' or number 1 ?
	用 o 和 l 很容易使 o 和 0 ，l 和1搞混


### 不必要的变量

Good

	return answer(argument)

Bad

	result = answer(argument)
	return result
	
	如果是表达式太长，或者返回的这个结果不是清晰明了的应该
	创建一个变量。

Good

	divisible_49 = lambda x: x % 49 == 0
	score = (total + 1 ) // 7
	do_something(divisible_49, score)

Bad

	do_something(lambda x: x % 49 == 0, (total + 1 ) // 7)
	
	
	
### 命名约定

Good
	total_score = 0
	final_score = 1
	
	def mean_strategy(score, opp):
	
	class ExampleClass:
Bad
	TotalScore = 0
	finalScore = 1
	
	def Mean_Strategy(score, opp):
	
	class example_class:
		
	# python 中一般变量和函数名使用下划线，类名使用驼峰
	

使用空格代替tab，一般使用四个空格键。保存一行代码不要过长，
大概在 70 个字符作用就好。

### 操作符之间的间隔

Good

	x = a + b*c*(a**2) / c - 4
	tup = (x, x/2, x/3, x/4)
	
Bad

	x=a+b*c*(a**2)/c-4
	tup = (x, x/2, x/3, x/4)
	
Good

	def func(a, b, c, d, e, f,
			g, h, i):
		# body
		
	tup = (1 , 2, 3, 4, 5,
			6, 7, 8)
			
	names = (' alice' ,
			' bob' ,
			' eve' )
	
	
### 控制语句

Bad

	if pred == True: # bad!
	. . .
	if pred == False: # bad!

Good

	if pred: # good!
	. . .
	if not pred: # good!
	
python 中的 [] , () , {} , set() 都可以使用bool判断
	
	if lst: # if lst is not empty
	. . .
	if not tup: # if tup is empty
	
这里要注意的一点是如果要将一个元素默认为一个list，

	这种做法会使得每次调用都增加一个元素在x中。
	
	def demo(x=[]):
		pass

	正确的做法是
		
	def demo(x=None):
		if x is None:
			x = []
	
	这里也不可以使用 not x，因为可能传入的是一个空字符，
	这种程序就会报错。

### 多余的if else

Bad

	if pred: # bad!
		return True
	else:
		return False
		
	if num ! = 49:
		total += example(4, 5, True)
	else:
		total += example(4, 5, False)
		
	if pred: # bad!
		print(' stuff' )
		x += 1
		return x
	else:
		x += 1
		return x

	多余的逻辑
	if x == 10:
	    return True
	else:
	    return False

	正确的方式
	    return x == 10
	

Good

	return pred
	
	total += example(4, 5, num!=49)
	
	if pred: # good!
		print(' stuff' )
	x += 1
	return x
	
Good
	
	把注释写到doc中，使用help函数可以看到
	
	def average(fn, samples):
		" " " Calls a 0-argument function SAMPLES times, and takes
		the average of the outcome.
		" " "
### 不必要的注释

Bad

	def example(y):
		x += 1 # increments x by 1
		return square(x) # returns the square of x
			
### 重复，使用一个变量保存。

Bad

	if a + b - 3 * h / 2 % 47 == 4:
		total += a + b - 3 * h / 2 % 47
		return total
		
Good

	turn_score = a + b - 3 * h / 2 % 47
	if turn_score == 4:
		total += turn_score
		return total
		
### 合理使用 列表生成式

Good

	ex = [x*x for x in range(1 0)]
	L = [pair[0] + pair[1 ]
		for pair in pairs
		if len(pair) == 2]
			
Bad

	L = [x + y + z for x in nums if x > 1 0 for y in nums2 for z in nums3 if y > z]


### 通用的一些手段   

**写程序很重要的一点是控制复杂度，抽象、模块化就是解决这个问题的手段。 好的代码应该是清晰易懂，代码即注释的，这点    
是需要很多锻炼才可以做到的，下面是一些方法：**      


### 告别面条代码    

Bad 

    if val == 'x':
        do xxx
    elif val == 'y':
        do xxx
    elif val == 'z':
        do xxx
    elif val == 'a':
        do xxx
    else:
        do xxx


Good    

    map_func = {'x': func1, 'y': func2, 'z': func3, 'a': func4}
    if val in map_func:
        return map_func[val]
    else:
        do xxx
        
上面这种方式在代码比较复杂的时候尤其适用， 很多时候这种代码都有大量可以复用的，可以抽象出来使用。    


### 模块化

**代码的模块化不是把代码扔在不同的py文件中，有人很天真的把代码放在不同的文件下，自以为做到了模块化，这完全就是搞笑。
真正的模块化应该是逻辑上模块化，这是一个抽象的过程，抽象的好的程序无论是在扩展还是在维护的时候都很容易。**

几个基本的方法：

* 写简短的函数，可以一眼在屏幕中看完的。 如果函数太长就将它拆为更小的。
* 经常写工具函数，将一些常用的操作抽象出来
* 一个函数只做一个事情。

### 写可读的代码 

代码即注释是需要很多练习才可以实现的，做不到这一点就通过注释来讲清楚函数做了什么。      

Bad    

    [
                    {
                        "night": getTonight(self.checkinoutdate['checkindate'], i),
                        "ratetype": self.ratekey['ratetype'],
                        "includebreakfastqty2": self.ratekey['includebreakfastqty2'],
                        "preeprice": preeprice
                    }
                for i, preeprice in zip(range((strptime(self.checkinoutdate['checkoutdate'])-strptime(self.checkinoutdate['checkindate'])).days), self.ratekey['preeprices'])],

上面的这种做法是一种很糟糕的做法，读起来很痛苦，也没注释， 属于滥用python 的列表生产式


Good
    
    orderitems = []
    for i, preeprice in zip(range((strptime(self.checkinoutdate['checkoutdate'])- 
            strptime(self.checkinoutdate['checkindate'])).days), self.ratekey['preeprices'])],
            orderitems.append({
                            "night": getTonight(self.checkinoutdate['checkindate'], i),
                            "ratetype": self.ratekey['ratetype'],
                            "includebreakfastqty2": self.ratekey['includebreakfastqty2'],
                            "preeprice": preeprice
                        })


**局部变量和使用它们的地方应该尽量接近， 不要重用局部变量，防止混淆**

做好手下的事情再去考虑复用，扩展等问题，就像一些常用的框架一样，很多都是作者做一些重复的事情做多了，发现可以抽象出来一个框架。
如果一开始就想去做一个框架肯定是得不偿失的。

### Code Case