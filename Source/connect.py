# -*- encoding: utf-8 -*-

import socket
import time
import threading
import re


runState= 1;

class Connections():	
	serverIP= 'localhost'; # 所要连接的电信设备地址
	serverPort= '2012'; # 电信设备端口
	bufferSize= 1024;
	dataReceived= []; # 接收到的数据
	dataToBeSent= []; # 作为s'时需要发送的数据
	clientList= []; # 作为s'时,已经连接上的客户端
	workAsServerPort= 0; # 作为s'时的伺服端口


#	def __init__(self,serverIP,serverPort,bufferSize):
#		self.serverIP= serverIP;
#		self.serverPort= serverPort;
#		self.bufferSize= bufferSize;
		
	def connect(self,ip,port,isRealServer= True):
		# 尝试连接服务器,如果isRealServer == True,则要连接的是s,否则是s'
		self.tcpSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM);#建立tcpSocket
		self.tcpSocket.settimeout(3);#设置超时时间


		if isRealServer:
			self.serverIP= ip; #服务器ip地址
			self.serverPort= port; # 服务器端口号
			serverAddress= (self.serverIP,self.serverPort);#socket
		else:
			serverAddress= (ip,port);
			
		try:
			self.tcpSocket.connect(serverAddress); #尝试连接
		except:
			# 若当前尝试连接s失败,则继续尝试连接s'

                        if isRealServer:#如果直接连接s失败
				self.error('direct connect to the device failed, try another way');
				#那么就等待广播消息
                                turnOut= self.waitForBroadcast();
				return turnOut;
			else: #如果是尝试连接s'失败就返回失败
				self.error('connection time out');
				return False;

		# 连接成功后打开接收数据的线程
		threadReceive= threading.Thread(target= self.receive);
		threadReceive.start();
		
		if isRealServer:
			# 若当前连接上了电信设备,则向外广播"我是pesudo服务器",并且在某个端口等待连接
                        # 等待客服端连接s'的线程
			threadWaitForClient= threading.Thread(target= self.waitForClient);
			threadWaitForClient.start();

                        # s'的广播线程
			threadBroadcast= threading.Thread(target= self.broadcast);
			threadBroadcast.start();

		return True; #连接成功



	def receive(self):
		# 接收服务器传来的报文,存入dataReceived和dataToBeSent
		global runState;
		bufferSize= self.bufferSize;
		self.tcpSocket.settimeout(None);
		
		normalEnd= True;
		while runState: #当当前处于运行状态就接受数据
			try:
				received= self.tcpSocket.recv(bufferSize);
			except:
				self.tcpSocket.close();
				try:
					self.broadcastSocket.close();
					self.serverSocket.close();
				except:
					pass;

				self.connect(self.serverIP,self.serverPort,True);
				normalEnd= False;
				break;

			if received == '': #如果接受数据为空就忽略
				pass;
			else:
				timeNow=  time.strftime('[%Y/%m/%d %H:%M:%S]',time.localtime());
				timeAndMessage= (timeNow,received);
				self.dataReceived.append(timeAndMessage);# 保存已经收到的消息
				self.dataToBeSent.append(received);	# 讲信息保存到发送队列中，对于s'有用
									# 转发的报文不加时间戳	
				print timeAndMessage;

		if normalEnd:
			self.tcpSocket.close();

		print 'socket has been closed';

	def waitForBroadcast(self):
		# 连接电信设备失败后,等待网络中的广播
		print 'waiting for broadcast...'

		address= ('',7777); # 广播的来源IP任意,端口号7777
		udpSocket= socket.socket(socket.AF_INET,socket.SOCK_DGRAM);
		udpSocket.bind(address);
		udpSocket.settimeout(3); # 设置最长等待时间为3s
		attempt= 0; #尝试次数
		while runState and attempt< 10: # 最大尝试次数为10
			try:
				data,serverAddress= udpSocket.recvfrom(self.bufferSize);
				attempt+= 1;
			except: # if attempt >= 10, return False
				return False;

			# 收到广播报文后,取出该s'所连接的电信设备的IP和该s'的伺服端口
			# 因为可能有多个电信设备,这里还要判断是否是所需要连接的那个
			match= re.search("I'm the pesudo-server of ([\.\d\w]+),port@(\d+)",data);
			ip= match.group(1);
			port= int(match.group(2));
			if ip== self.serverIP:
				print port;
				self.connect(serverAddress[0],port,False);
				udpSocket.close();
				threadAlwaysListen= threading.Thread(target= self.alwaysListen,\
						args=(data,attempt) );
				threadAlwaysListen.start();
				return True;
		return False;


	def alwaysListen(self,correctData,totalAttempts):
		global runState;
		address= ('',7777);
		udpSocket= socket.socket(socket.AF_INET,socket.SOCK_DGRAM);
		udpSocket.bind(address);
		udpSocket.settimeout(3);
		attempt= 0;
		while runState and attempt< totalAttempts+ 1:
			try:
				data,serverAddress= udpSocket.recvfrom(self.bufferSize);
						
				if data == correctData:
					attempt= 0;
				else:
					attempt+= 1;

			except:
				attempt+= 1;
			
		self.tcpSocket.close();



	def broadcast(self):
		# 连接到电信设备后,在网络中广播"我连接到xxx电信设备了!"

		global runState;
		address= '<broadcast>'; # 广播地址的写法
		port= 7777;		# 广播的接收端口
		self.broadcastSocket= socket.socket(socket.AF_INET,socket.SOCK_DGRAM);
		self.broadcastSocket.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1);
		time.sleep(1);		# 休眠1s,确保waitForClient()就绪
		while runState:
			# 广播内容:我是xxx的傀儡主机,我在xxx端口等待连接
			message= "I'm the pesudo-server of %s,port@%d" % (self.serverIP,self.workAsServerPort)
			print message;
			try:
				self.broadcastSocket.sendto(message,(address,port));
				time.sleep(1.5);# 每1.5s广播一次
			except:
				break;
		print 'broadcast() has ended'

	def waitForClient(self):
		# 连接到电信设备后,在一个尚未使用的端口上等待连接
		# 连接建立后在这个端口发送数据
		global runState;

		address= ('',0); # 来源IP任意,端口设置为0,即系统会自动分配一个尚未使用的端口
		self.serverSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM);
		self.serverSocket.bind(address);
		self.workAsServerPort= self.serverSocket.getsockname()[1];# 取得"系统分配端口"的确切值
		self.serverSocket.listen(100); # 最大的等待连接队列长度100
		
		# 新建一个线程,向客户机轮流发送接收到的报文
		threadRoundRobin= threading.Thread(target= self.roundRobin);
		threadRoundRobin.start();
		
		while runState:
			# 监听端口并接受连接
			try:
				tempSocket,clientAddress= self.serverSocket.accept();
				self.clientList.append(tempSocket);
				print clientAddress,'has connected.'
			except:
				break;

		print 'waitForClient() has ended';


	def roundRobin(self):
		# 向clientList中的客户机轮流发送dataToBeSent中的数据
		global runState;

		while runState:
			if self.dataToBeSent!= [] and self.clientList!= []:
				toBeSent= self.dataToBeSent.pop(0); # 发送后从dataToBeSent中出队
				for socket in self.clientList:
					try:
						socket.send(toBeSent);
					except:
						self.clientList.remove(socket);
		print 'roundRobin ends';

	def error(self,errorMessage):
		# 错误处理
		timeNow= time.strftime('[%Y/%m/%d %H:%M:%S]',time.localtime())
		print timeNow, errorMessage;

def main():
	instance= Connections();
	turnOut= instance.connect('localhost',int(2012),True);
	if turnOut:
		print 'connection OK';
	else:
		print 'connection Error';



if __name__ == '__main__':
	main();



