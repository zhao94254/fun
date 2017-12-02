### tcp协议（概念和介绍）  
#### 特性  
  
tcp是一个可靠的，面向链接的协议。  
tcp（udp也是，所以tcp udp都有一个伪头部）会对整个数据进行校验。  
对失序的报文进行排序。  
面向字节流，可以流量控制 拥塞控制。  

![状态变换图](http://pyblog-10073407.image.myqcloud.com/postimage1511276362)

由于tcp是一个面向链接的协议，所以需要建立一个逻辑上的链接，这个链接的建立过程就是  
三次握手 和 四次挥手。  
从上图可以很清楚的看出tcp链接建立和断开的过程。值得注意的是在socket编程中，是不可以  
从connect状态变到syn_sent状态的（在调用 listen后 无法调用connect）。在建立链接的过程中  
使用seq来保持同步。  

![建立和断开](http://pyblog-10073407.image.myqcloud.com/postimage1511276414)

由于tcp是一个面向链接的协议，所以需要建立一个逻辑上的链接，这个链接的建立过程就是  
三次握手 和 四次挥手。  
从上图可以很清楚的看出tcp链接建立和断开的过程。值得注意的是在socket编程中，是不可以  
从connect状态变到syn_sent状态的（在调用 listen后 无法调用connect）。在建立链接的过程中  
使用seq来保持同步。  

##### 为什么是三次握手？  
因为ip层提供的不可靠的链接，通信的双方为了可靠的建立链接 理论上是最少需要三次的。  
可以试想两次握手时， 客户端发送了一个包就建立连接了，但是这个包在网络上延时了，这个包  
是已经失效的了，但是过了一段时间后服务器又接到了， 服务器就以为还会有数据过来（其实客户  
端早就放弃连接了），就会白白浪费很多资源。  

##### 为什么是四次挥手？
首先TCP是一个全双工的协议， 其次tcp 提供了一个半关闭的一个能力，这个是四次挥手的主要原因。  
举例来说 A-B这一端需要单独断开，B-A这一端也需要断开。这种断开就提供了一种能力，即 A向B断开了，  
但是B还是可以向A发送数据的。A还是可以接收B的数据的。这就是所谓的半关闭和三次握手相比 三次握手  
中的SYN 和 ACK 是可以同时发送回去的。而断开的过程中  ACK 和 FIN 是分开的，这是因为有的数据可  
以还没传完，在一个单向上还需要发送。  


##### 同时打开链接 同时关闭 会如何？
先来看同时打开。双方同时发syn，进入syn_sent状态，当每一段收到syn后进入到syn_recv  
![同时打开](http://pyblog-10073407.image.myqcloud.com/postimage1511964984?imageView2/0/w/450/h/400 "enter image title here")
  再对其进行确认就完成了链接建立。和正常建立链接不同的是需要交换四个报文段。  
 
同时关闭，和正常的关闭不同，双方直接从established发送fin，进入closing，发送ack后进入timewait状态。  
![同时关闭](http://pyblog-10073407.image.myqcloud.com/postimage1511964982?imageView2/0/w/450/h/400 "enter image title here") 
  

##### time_wait close_wait状态？  
先来说closewait状态这个状态只会在被动关闭的一方出现。出现这个状态主要是因为两点：  
1. 应用程序没有正确处理tcp链接的关闭。  
2. 我之前遇到的，在一个程序中同时进行了大量的链接，其中有一些是很活跃的链接，一些是不活跃的  
导致那些不活跃的链接被关闭后，程序没有去处理。  
  
这里引出finwait2定时器的概念，试想有很多的链接被主动关闭了，这些链接没有进行对应的处理导致这个连接被占用着。这时就  
需要一个定时器来解决。超过时间后就完全断开这一端的链接。这时如果客户端反应过来，这个链接就变成了半打开连接（客户端）  
不知道这个链接已经断开了。



##### time_wait状态（等待2msl，msl指的是报文在网络的最大生存时间，ip层中有一个ttl的东西）是主动断开链接的一方会出现的一种状态，  
这种状态出现的原因是因为两点：  
  
第一，确保最后的ack报文到达了对方，防止丢失。  
第二，在time_wait状态下（A的ip， 端口， B的ip， 端口）无法复用。这是为了  
防止来自该链接的延迟报文对这个新开的链接造成影响。可以通过设置SO_REUSEADDR  
来立马复用处于time wait状态的链接。  

##### tcp中的序号是如何控制来防止两个链接不会乱的？  
上面提到了time wait的影响，一方面是防止ack的影响，一方面是怕延迟报文对新的链接产生影响。对于第二个问题主要是因为在tcp中  
使用序号来保持数据有序的，序号最大支持32位，这意味着发送的数据超过2**32序号可能重复，即使不超过这么大也可能重复，因为序号  
并不是从1开始的。  
这里也就意味这序号需要一种方法来判断。  

![seq1](http://pyblog-10073407.image.myqcloud.com/postimage1512216749?imageView2/0/w/450/h/400	)  
如上图，这里是通过a-b=a+(b的补码)来计算的。比如0-1 补码是111 0-2 110 0-7 001  
序号通过这种方式来循环使用。

![seq2](	http://pyblog-10073407.image.myqcloud.com/postimage1512216722?imageView2/0/w/450/h/400)  
tcp中通过这种方式来区分给定序号是新的序号还是重传的序号。如果到来的序号经过计算是大于现在正在等待的序号的就把这个数据保存  
下来，如果不是就丢掉。  
现在回到上面的问题，time wait状态下通过巧妙选择一个序号，来确保序号可以被区分开是否是新连接的数据。  

但是还是有问题的，比如这种情况：  
   
    1.A 和 B建立了一个链接，发送了一个序号为2的报文，该报文在网络上被延迟发送了    
    2.这个报文被重发，序号还是2，重发的到达B  
    3.A客户关闭链接。   
    4.A主机崩溃  
    5.客户主机崩溃重启，tcp初始tcpiss 为1  
    6.AB使用了刚才同样的链接，初始的序号还选为1  
    7.刚才延时的报文到达B，这个延时的报文被认为是新连接的报文。  
  
解决这个问题的唯一方法就是在msl的平静时间内不发任何东西（但是这样实现的人很少，这种情况出现的几率太低了）  

除了上面这种有一点风险的方法现在还可以通过设置下面这几个参数来避免time wait影响。  

    net.ipv4.tcp_tw_recycle = 1 # time wait快速回收
    net.ipv4.tcp_tw_reuse = 1 # 重用 time wait状态下的链接
    net.ipv4.tcp_timestamps = 1 # 时间戳选项

通过时间戳来判断，因为时间戳是递增的。如果收到的数据包是小于当前时间的就直接丢掉。  

 
##### SO_REUSEADDR SO_REUSEPORT？
    
    这两个选项都要求在一个链接建立的时候就启用这个选项。
    SO_REUSEADDR 允许进程绑定一个正在用的端口号，但是被绑定的ip没被用。
    如： 第一个链接绑定到了122.22.22.2 port为5000 第二个可以绑定到 127.0.0.1 port为5000
    
    SO_REUSEPORT 允许进程重用ip地址 和 端口 
    如： 进程A可以绑定 127.0.0.1 5000 进程B也可以绑定之前的这个

SO_REUSEPORT 的好处：  
在不使用SO_REUSEPORT的时候，处理的方法是用一个监听线程监听所有的链接，然后分发到不同的工作线程，  
在一些情况下这个线程可能处于瓶颈状态。而且可能任务分配不均匀。  
启用了这个SO_REUSEPORT 后，链接到达后被均匀分配，每个进程单独监听一条链接。


https://stackoverflow.com/questions/14388706/socket-options-so-reuseaddr-and-so-reuseport-how-do-they-differ-do-they-mean-t
http://rextester.com/BUAFK86204
 
##### time wait的影响  

上面提到的time wait状态带来的影响都有对应的解决办法了，但是还是要尽力避免在服务器端主动断开链接。因为当一个非常繁忙的服务器  
上出现大量的time wait的链接时，这些链接会占用不少的系统资源。网络这块的吞吐可能不会那么高，所以需要将这个压力来分发到  
客户端。让客户端这里来主动断开，减轻这个压力。
  
参见 https://www.isi.edu/touch/pubs/infocomm99/ 
  

##### tcp调优的一些参数  
    
    # 模版
    net.ipv4.tcp_syn_retries = 1
    net.ipv4.tcp_synack_retries = 1
    net.ipv4.tcp_keepalive_time = 600
    net.ipv4.tcp_keepalive_probes = 3
    net.ipv4.tcp_keepalive_intvl =15
    net.ipv4.tcp_retries2 = 5
    net.ipv4.tcp_fin_timeout = 2
    net.ipv4.tcp_max_tw_buckets = 36000
    net.ipv4.tcp_tw_recycle = 1
    net.ipv4.tcp_tw_reuse = 1
    net.ipv4.tcp_max_orphans = 32768
    net.ipv4.tcp_syncookies = 1
    net.ipv4.tcp_max_syn_backlog = 16384
    net.ipv4.tcp_wmem = 8192 131072 16777216
    net.ipv4.tcp_rmem = 32768 131072 16777216
    net.ipv4.tcp_mem = 786432 1048576 1572864
    net.ipv4.ip_local_port_range = 1024 65000
    net.ipv4.ip_conntrack_max = 65536
    net.ipv4.netfilter.ip_conntrack_max=65536
    net.ipv4.netfilter.ip_conntrack_tcp_timeout_established=180
    net.core.somaxconn = 16384
    net.core.netdev_max_backlog = 16384

    
    net.core.netdev_max_backlog = 400000
    #该参数决定了，网络设备接收数据包的速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目。
    net.core.optmem_max = 10000000
    #该参数指定了每个套接字所允许的最大缓冲区的大小
    net.core.rmem_default = 10000000
    #指定了接收套接字缓冲区大小的缺省值（以字节为单位）。
    net.core.rmem_max = 10000000
    #指定了接收套接字缓冲区大小的最大值（以字节为单位）。
    net.core.somaxconn = 100000
    #Linux kernel参数，表示socket监听的backlog(监听队列)上限
    net.core.wmem_default = 11059200
    #定义默认的发送窗口大小；对于更大的 BDP 来说，这个大小也应该更大。
    net.core.wmem_max = 11059200
    #定义发送窗口的最大大小；对于更大的 BDP 来说，这个大小也应该更大。
    net.ipv4.conf.all.rp_filter = 1
    net.ipv4.conf.default.rp_filter = 1
    #严谨模式 1 (推荐)
    #松散模式 0
    net.ipv4.tcp_congestion_control = bic
    #默认推荐设置是 htcp
    net.ipv4.tcp_window_scaling = 0
    #关闭tcp_window_scaling
    #启用 RFC 1323 定义的 window scaling；要支持超过 64KB 的窗口，必须启用该值。
    net.ipv4.tcp_ecn = 0
    #把TCP的直接拥塞通告(tcp_ecn)关掉
    net.ipv4.tcp_sack = 1
    #关闭tcp_sack
    #启用有选择的应答（Selective Acknowledgment），
    #这可以通过有选择地应答乱序接收到的报文来提高性能（这样可以让发送者只发送丢失的报文段）；
    #（对于广域网通信来说）这个选项应该启用，但是这会增加对 CPU 的占用。
    net.ipv4.tcp_max_tw_buckets = 10000
    #表示系统同时保持TIME_WAIT套接字的最大数量
    net.ipv4.tcp_max_syn_backlog = 8192
    #表示SYN队列长度，默认1024，改成8192，可以容纳更多等待连接的网络连接数。
    net.ipv4.tcp_syncookies = 1
    #表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0，表示关闭；
    net.ipv4.tcp_timestamps = 1
    #开启TCP时间戳
    #以一种比重发超时更精确的方法（请参阅 RFC 1323）来启用对 RTT 的计算；为了实现更好的性能应该启用这个选项。
    net.ipv4.tcp_tw_reuse = 1
    #表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭；
    net.ipv4.tcp_tw_recycle = 1
    #表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭。
    net.ipv4.tcp_fin_timeout = 10
    #表示如果套接字由本端要求关闭，这个参数决定了它保持在FIN-WAIT-2状态的时间。
    net.ipv4.tcp_keepalive_time = 1800
    #表示当keepalive起用的时候，TCP发送keepalive消息的频度。缺省是2小时，改为30分钟。
    net.ipv4.tcp_keepalive_probes = 3
    #如果对方不予应答，探测包的发送次数
    net.ipv4.tcp_keepalive_intvl = 15
    #keepalive探测包的发送间隔
    net.ipv4.tcp_mem
    #确定 TCP 栈应该如何反映内存使用；每个值的单位都是内存页（通常是 4KB）。
    #第一个值是内存使用的下限。
    #第二个值是内存压力模式开始对缓冲区使用应用压力的上限。
    #第三个值是内存上限。在这个层次上可以将报文丢弃，从而减少对内存的使用。对于较大的 BDP 可以增大这些值（但是要记住，其单位是内存页，而不是字节）。
    net.ipv4.tcp_rmem
    #与 tcp_wmem 类似，不过它表示的是为自动调优所使用的接收缓冲区的值。
    net.ipv4.tcp_wmem = 30000000 30000000 30000000
    #为自动调优定义每个 socket 使用的内存。
    #第一个值是为 socket 的发送缓冲区分配的最少字节数。
    #第二个值是默认值（该值会被 wmem_default 覆盖），缓冲区在系统负载不重的情况下可以增长到这个值。
    #第三个值是发送缓冲区空间的最大字节数（该值会被 wmem_max 覆盖）。
    net.ipv4.ip_local_port_range = 1024 65000
    #表示用于向外连接的端口范围。缺省情况下很小：32768到61000，改为1024到65000。
    net.ipv4.netfilter.ip_conntrack_max=204800
    #设置系统对最大跟踪的TCP连接数的限制
    net.ipv4.tcp_slow_start_after_idle = 0
    #关闭tcp的连接传输的慢启动，即先休止一段时间，再初始化拥塞窗口。
    net.ipv4.route.gc_timeout = 100
    #路由缓存刷新频率，当一个路由失败后多长时间跳到另一个路由，默认是300。
    net.ipv4.tcp_syn_retries = 1
    #在内核放弃建立连接之前发送SYN包的数量。
    net.ipv4.icmp_echo_ignore_broadcasts = 1
    # 避免放大攻击
    net.ipv4.icmp_ignore_bogus_error_responses = 1
    # 开启恶意icmp错误消息保护
    net.inet.udp.checksum=1
    #防止不正确的udp包的攻击
    net.ipv4.conf.default.accept_source_route = 0
    #是否接受含有源路由信息的ip包。参数值为布尔值，1表示接受，0表示不接受。
    #在充当网关的linux主机上缺省值为1，在一般的linux主机上缺省值为0。
    #从安全性角度出发，建议你关闭该功能。
    
    
    如果真的是要在线上使用还是需要经过大量的测试，来寻找尽可能好的方法。
    
参考 https://tonydeng.github.io/2015/05/25/linux-tcpip-tuning/




