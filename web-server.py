from flask import Flask
from flask import request,session,redirect,url_for,jsonify
from flask import render_template,flash
#from flask import json
import json
import socket
import os
import time

cur_username = ''
app = Flask(__name__)
#建立socket，连接数据处理器的过程，一定要在这里先写，如果写在main函数里，不能写在run函数之后
HOST = 'localhost'
PORT = 8008
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
print("接下来输出s的类型")
print(type(s))

#生成密钥，作用于session和cookie
#app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.secret_key = os.urandom(24)
#全局变量，用来将数据传到数据处理器
response = ''

file_list = []#用来保存管理员目前已上传的文件的列表
data_filelist = []#从数据处理器传来的文件列表

dir_path = ['D:']#路径初始化为D盘根目录
dir_filelist = []
#dir_message = {'dir_path':dir_path,'dir_filelist':dir_filelist}
@app.route('/',methods = ['GET','POST'])
def index():
	#判断用户是否已经登陆，若已登录，则直接进入User.html
	if session.get('username') is None:
		#return render_template('login.html')
		return render_template('index.html')
	else:
		return render_template('User.html')

@app.route('/check_file',methods = ['GET','POST'])
def check_file():
	print('显示本层信息')
	if request.method == 'POST':
		dir = request.get_data()
		dir = dir.decode('utf-8')
		final_path = ''
		for p in dir_path:
			final_path += p
			final_path += '/'
		final_path += dir
		dir_path.append(dir)
		response = {'path':final_path,'function':'check_file'}
		response = json.dumps(response)
		s.sendall(response.encode('utf-8'))

		data = s.recv(1024).decode('utf-8')
		data = json.loads(data)
		if data.get('message') == '文件夹非空':
			dir_filelist = data.get('dir_list')
			return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)
		else:
			return render_template('create_menu.html',dir_path=dir_path,dir_filelist=[])
		
		


@app.route('/go_back',methods = ['GET','POST'])
def go_back():#返回上一层，同时显示文件夹信息
	print('准备返回上一层')
	dir_path.pop()
	final_path = ''
	for p in dir_path:
		final_path += p
		final_path += '/'
	print('上一层路径'+final_path)
	response = {'path':final_path,"function":'go_back'}
	response = json.dumps(response)#将字典转成字符串
	s.sendall(response.encode('utf-8'))
	data = s.recv(1024).decode('utf-8')
	data = json.loads(data)
	dir_filelist = data.get('dir_list')
	return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)#dir_filelist要从后端获得


@app.route('/create_dir',methods = ['GET','POST'])#新建文件夹
def create_dir():
	if request.method == 'POST':
		dir = request.get_data()
		#从ajax传来的纯文本内容是bytes类型
		dir = dir.decode('utf-8')
		dir_path.append(dir)
		final_path = ''
		for p in dir_path:		
			final_path += p
			final_path += '/'
		print(final_path)
		response = {'path':final_path,"function":'create_dir'}
		response = json.dumps(response)#将字典转成字符串
		s.sendall(response.encode('utf-8'))
		data = s.recv(1024).decode('utf-8')
		print(data)


	return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)#dir_filelist要从后端获得

@app.route('/goto_new',methods = ['GET','POST'])
def goto_new():
	if cur_username in dir_path:
		final_path = ''
		for p in dir_path:		
			final_path += p
			final_path += '/' 
		response = {'path':final_path,"function":'create_dir'}
		response = json.dumps(response)
		s.sendall(response.encode('utf-8'))
		data = s.recv(1024).decode('utf-8')
		data = json.loads(data)
		if data.get('message') == '创建成功':
			#return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)
			return render_template('create_menu.html',dir_path=dir_path,dir_filelist=[])
		else:
			dir_filelist = data.get('dir_list')
			return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)
	else:
		dir_path.append(cur_username)
		final_path = ''
		for p in dir_path:		
			final_path += p
			final_path += '/' 
		response = {'path':final_path,"function":'create_dir'}
		response = json.dumps(response)
		s.sendall(response.encode('utf-8'))
		data = s.recv(1024).decode('utf-8')
		data = json.loads(data)
		if data.get('message') == '创建成功':
			#return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)
			return render_template('create_menu.html',dir_path=dir_path,dir_filelist=[])
		else:#说明路径已存在
			dir_filelist = data.get('dir_list')
			return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)
	#return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)


@app.route('/user_download',methods = ['GET','POST'])
def user_download():
	print("收到用户下载自己文件请求")
	if request.method == "POST":
		data = request.get_data()
		data = data.decode('utf-8')
		data = json.loads(data)
		filename = data.get('filename')
		final_path = ''
		for p in dir_path:
			final_path += p
			final_path += '/'
		response = {'filename':filename,'function':'user_download','path':final_path}
		response = json.dumps(response)
		s.sendall(response.encode('utf-8'))
		data = s.recv(1024).decode('utf-8')
		data = json.loads(data)#变成字典
		size = data.get('file_size')#获取文件大小
		num = size/1024.0
		if num != int(num):
			num = int(num) +1
		else:			
			num = int(num)
		print('要接收的次数:',num)

		s.sendall("已知道长度，请继续发送".encode('utf-8'))
		rev_file = ""
		for i in range(num):
			print("第"+str(i)+"次接收文件")
			file_content = s.recv(1024).decode('gbk')
			rev_file += file_content
			#print(file_content)
		print("准备开始保存文件")
		File = open('C:\\Users\\李瀚哲\\Desktop\\user_download\\'+filename,'w+') 
		File.write(rev_file)
		#print("写入完成")
		File.close()
		s.sendall("下载接收成功，放心吧".encode('utf-8'))
		print(s.recv(1024).decode('utf-8'))
		return jsonify("download sucessfully")

@app.route('/download',methods = ['GET','POST'])
def download():
	print("收到下载文件请求")
	if request.method == "POST":
		data = request.get_data()
		data = data.decode('utf-8')
		data = json.loads(data)
		filename = data.get('filename')
		response = {'filename':filename,'function':'download'}
		response = json.dumps(response)
		s.sendall(response.encode('utf-8'))
		
		#接收文件大小反馈
		data = s.recv(1024).decode('utf-8')
		data = json.loads(data)#变成字典
		size = data.get('file_size')#获取文件大小
		#计算要接收的次数
		num = size/1024.0
		if num != int(num):
			num = int(num) +1
		else:			
			num = int(num)
		print('要接收的次数:',num)

		s.sendall("已知道长度，请继续发送".encode('utf-8'))
		rev_file = ""
		for i in range(num):
			print("第"+str(i)+"次接收文件")
			file_content = s.recv(1024).decode('gbk')
			rev_file += file_content
			#print(file_content)
		print("准备开始保存文件")
		File = open('C:\\Users\\李瀚哲\\Desktop\\keep_file\\'+filename,'w+') 
		File.write(rev_file)
		#print("写入完成")
		File.close()
		s.sendall("下载接收成功，放心吧".encode('utf-8'))
		print(s.recv(1024).decode('utf-8'))
		return jsonify("download sucessfully")#一定要 因为前端ajax定义数据类型是json，所以返回的数据也必须是json，不然就会进入error方法


@app.route('/user_upload',methods = ['GET','POST'])
def user_upload():
	print('用户要上传文件了')
	if request.method == "POST":
		file = request.files['upload-file']
		filename = file.filename
		print(filename,type(file))
		file_data = request.files['upload-file'].read()
		size = len(file_data)
		final_path = ''
		for p in dir_path:
			final_path += p
			final_path += '/'
		print(final_path)

		#头文件信息
		header_data = {
			'function':'user_upload',
  			'file_name': filename,
    		'file_size': size,
    		'date': time.strftime('%Y-%m-%d %X',time.localtime()),
    		'charset':'utf-8',
			'path':final_path
		}
		print("文件大小：",size)
		print('文件格式：',type(file_data))

		s.sendall(json.dumps(header_data).encode('utf-8'))
		data = s.recv(1024)#这里是接收来自数据处理器的接受请求
		data = data.decode('utf-8')
		print(data)
		if data == '接受头文件信息成功,请发送文件吧!':
			s.sendall(file_data)
			data = s.recv(1024)
			data = data.decode('utf-8')
			#
			data = json.loads(data)
			print("让我们来看看data里面是什么",data)
			# global data_filelist 
			# data_filelist = data.get('file_list')
			# print(data_filelist)
			dir_filelist = data.get('dir_list')
			print(dir_filelist)
			data = data.get('response')
			if data == '接受文件成功':				
				return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)
			if data == '没有接受到文件':
				print('发送文件失败')
				return render_template('create_menu.html',dir_path=dir_path,dir_filelist=dir_filelist)
		


@app.route('/upload',methods = ['GET','POST'])
def upload():
	print("收到管理员上传文件")
	if request.method == "POST":
		file = request.files['upload-file']
		filename = file.filename
		#file_type = filename.split('.')[1]
		#print(file_type)
		#file_list.append(filename)
		print(filename,type(file))
		file_data = request.files['upload-file'].read()
		size = len(file_data)
		#头文件信息
		header_data = {
			'function':'upload',
  			'file_name': filename,
    		'file_size': size,
    		'date': time.strftime('%Y-%m-%d %X',time.localtime()),
    		'charset':'utf-8'
			#'file_type':file_type
		}
		print("文件大小：",size)
		#print('文件内容：',file_data)
		print('文件格式：',type(file_data))
		s.sendall(json.dumps(header_data).encode('utf-8'))
		data = s.recv(1024)#这里是接收来自数据处理器的接受请求
		data = data.decode('utf-8')
		print(data)
		if data == '接受头文件信息成功,请发送文件吧!':
			s.sendall(file_data)
			data = s.recv(1024)
			data = data.decode('utf-8')
			#
			data = json.loads(data)
			print("让我们来看看data里面是什么",data)
			global data_filelist 
			data_filelist = data.get('file_list')
			print(data_filelist)
			data = data.get('response')
			#
			if data == '接受文件成功':
				print('发送文件成功,牛!')
			if data == '没有接受到文件':
				print('发送文件失败')
		return ("upload success")


@app.route('/logout')
def logout():
	session.pop('username',None)
	dir_filelist.clear()
	for i in range(len(dir_path)-1):
		dir_path.pop()
	return redirect(url_for('login'))

@app.route('/get_list',methods = ['GET'])
def get_list():
	print(data_filelist)
	return jsonify(data_filelist)

@app.route('/login',methods = ['GET','POST'])
def login():
	print("开始登陆")
	form_data = request.form
	username = form_data.get('username','')
	global cur_username
	cur_username = username
	password = form_data.get('password','')
	#将response变成字符串,并发送给数据处理器
	response = {'username':username,'password':password,'function':'login'}
	response = json.dumps(response)
	s.sendall(response.encode('utf-8'))

	#data接收的是数据处理器返回的response
	data = s.recv(1024)
	data = data.decode('utf-8')
	print(data)
	#登陆之后，设置session会话，表示已登录
	if data.split(',')[0] == 'success':
		session['username'] = username
		if data.split(',')[1] == '管理员':
			return render_template('Manager.html',name=username)
		elif data.split(',')[1] == '客户':
			return render_template('User.html',file_list=file_list)#传参:文件列表
	elif data == 'non-exited':
		flash("输入用户名或密码错误")
	
	return render_template('index.html')
	#return render_template('login.html')

@app.route('/register',methods = ['GET','POST'])
def register():
	if request.method == 'POST':
		form_data = request.form
		username = form_data.get('username')
		password = form_data.get('password')
		password2 = form_data.get('password2')
		level = form_data.get('level')#获取的是radio里value的值
		print(username,password,password2,level)
		if not all([username,password,password2]):
			flash("参数不完整")
			print("参数不完整")
			
		elif password != password2:
			flash("两次输入的密码不一致，请重新输入")
			print("两次输入的密码不一致，请重新输入")
		else:
			response = {'username':username,'password':password,'function':'register','level':level}
			response = json.dumps(response)
			s.sendall(response.encode('utf-8'))

			#data接收的是数据处理器返回的response
			data = s.recv(1024)
			data = data.decode('utf-8')
			if data == 'existed':
				flash('用户名已注册，请重试')
			elif data == 'success':#如果成功注册，则跳到登陆界面
				#return render_template('login.html')
				return render_template('index.html')
			
			#return render_template('ex1.html')
	return render_template('register.html')

@app.route('/calculate',methods =['GET','POST'])
def calculate():
	print("进入计算器")
	if request.method =='POST':
		#ajax传过来的是json类型（字符串）
		ajax_data = request.get_data()
		#变成字典
		ajax_data = json.loads(ajax_data)
		#获取两个操作数和操作
		first_oper = ajax_data.get('first_oper')
		second_oper = ajax_data.get('second_oper')
		kind = ajax_data.get('kind')
		print(first_oper)
		print(second_oper)
		print(kind)
		response = {'first_oper':first_oper,'second_oper':second_oper,'kind':kind,'function':'calculate'}
		response = json.dumps(response)
		s.sendall(response.encode('utf-8'))
		
		data = s.recv(1024)
		data = data.decode('utf-8')
		return str(data)
	
if __name__ == '__main__':
	app.run()
	
	#print('发送helloworld')
	#t='HelloWorld'
	#s.sendall(t.encode('utf-8'))
	#s.sendall(response.encode('utf-8'))
	#data=s.recv(1024)
	#s.close()
	#print('接收到来自服务器端的反馈：',data.decode('utf-8'))#如果不解码的话，中文会乱码



	