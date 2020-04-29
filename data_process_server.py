import socket
import json
import pymysql
import os
db=pymysql.connect('localhost','root','','class_design')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

file_list = []#用来存储文件列表

port=8008
print("已经打开数据处理器")
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('',port))
s.listen(3)

def check_file(data):
    path = data.get('path')
    print(path)
    dir_list = os.listdir(path)#获得文件夹下信息列表
    if len(dir_list) == 0:
        print('空文件夹')
        response = {'message':'是空文件夹'}
        return json.dumps(response)

    for i in dir_list:
        print(i)
    response = {'dir_list':dir_list,'message':'文件夹非空'}
    response = json.dumps(response)
    return response

def go_back(data):
    path = data.get('path')
    print(path)
    dir_list = os.listdir(path)#获得文件夹下信息列表
    for i in dir_list:
        print(i)
    response = {'dir_list':dir_list}
    response = json.dumps(response)
    return response


def create_dir(data):
    path = data.get('path')
    print(path)
    isExist = os.path.exists(path)#判断路径是否已存在
    if not isExist:
        os.makedirs(path)
        response = {'message':'创建成功'}
        return json.dumps(response)
        #return (path+'创建成功')
    else:
        dir_list = os.listdir(path)#获取当前路径下的文件列表
        response = {'dir_list':dir_list,'message':'目录已存在,返回文件列表'}
        return json.dumps(response)
        #return (path+'目录已存在,返回文件列表')

    #return "创建成功"
def user_download(data):
    filename = data.get('filename')
    path = data.get('path')
    print(path)
    File = open(path+filename,'rb+')
    file_data = File.read()
    file_size = len(file_data)
    print("文件大小:",file_size)
    print("文件形式:",type(file_data))
    response = {'file_size':file_size}
    conn.sendall(json.dumps(response).encode('utf-8'))
    data = conn.recv(1024).decode('utf-8')
    if data == "已知道长度，请继续发送":
        #print("开始发送")
        conn.sendall(file_data)#发送文件
        #print("发送结束")
        data = conn.recv(1024).decode('utf-8')
        #print(data)
        if data == "下载接收成功，放心吧":
            print('download successfully!')
            return 'download successfully!'
    return 'wrong'

def download(data):
    filename = data.get('filename')
    File = open('D:\\计算机网络\\课设服务器\\file\\'+filename,'rb+')
    file_data = File.read()
    file_size = len(file_data)
    print("文件大小:",file_size)
    print("文件形式:",type(file_data))
    response = {'file_size':file_size}
    conn.sendall(json.dumps(response).encode('utf-8'))
    data = conn.recv(1024).decode('utf-8')
    if data == "已知道长度，请继续发送":
        #print("开始发送")
        conn.sendall(file_data)#发送文件
        #print("发送结束")
        data = conn.recv(1024).decode('utf-8')
        #print(data)
        if data == "下载接收成功，放心吧":
            print('download successfully!')
            return 'download successfully!'
    return 'wrong'

def user_upload(data):#要用路径
    file_name = data.get('file_name')
    file_size = data.get('file_size')
    path = data.get('path')
    date = data.get('date')
    print('文件名:'+file_name)
    print('文件大小:',file_size)
    print('发送时间:',date)
    rev_file = ''
    if file_name != '':
        temp = '接受头文件信息成功,请发送文件吧!'
        conn.sendall(temp.encode('utf-8'))

        #计算接收次数
        num = file_size/1024.0
        if num != int(num):
            num = int(num) +1
        else:
            num = int(num)
        print('要接收的次数:',num)

        for i in range(num):
                file_content = conn.recv(1024).decode('utf-8')
                rev_file += file_content
                #print(file_content)
        File = open(path+file_name,'w+')#保存在用户文件夹下
        File.write(rev_file)
        File.close()
        dir_list = os.listdir(path)#获得文件夹下信息列表
        response = {'response':"接受文件成功",'dir_list':dir_list}
        #return "接受文件成功"
        return json.dumps(response)
    else:
        response = {'response':"没有接受到文件",'dir_list':dir_list}
        #return "没有接受到文件"
        return json.dumps(response)


def upload(data):
    file_name = data.get('file_name')
    file_size = data.get('file_size')
    date = data.get('date')
    print('文件名:'+file_name)
    print('文件大小:',file_size)
    print('发送时间:',date)
    rev_file = ''
    if file_name != '':
        temp = '接受头文件信息成功,请发送文件吧!'
        conn.sendall(temp.encode('utf-8'))

        #计算接收次数
        num = file_size/1024.0
        if num != int(num):
            num = int(num) +1
        else:
            num = int(num)
        print('要接收的次数:',num)

        for i in range(num):
                file_content = conn.recv(1024).decode('utf-8')
                rev_file += file_content
                #print(file_content)
        #保存文件 D:\计算机网络\课设服务器\file
        File = open('D:\\计算机网络\\课设服务器\\file\\'+file_name,'w+')
        File.write(rev_file)
        File.close()
        file_list.append(file_name)
        response = {'response':"接受文件成功",'file_list':file_list}
        #return "接受文件成功"
        return json.dumps(response)
    else:
        response = {'response':"没有接受到文件",'file_list':file_list}
        #return "没有接受到文件"
        return json.dumps(response)
        

def calculate(data):
    first_oper = float(data.get('first_oper'))
    second_oper = float(data.get('second_oper'))
    kind = data.get('kind')
    if kind == '加法':
        print(first_oper,second_oper,kind)
        return first_oper+second_oper
    elif kind == '减法':
        print(first_oper,second_oper,kind)
        return first_oper-second_oper
    elif kind == '乘法':
        print(first_oper,second_oper,kind)
        return first_oper*second_oper
    else:
        print(first_oper,second_oper,kind)
        return first_oper/second_oper


def register(data):
    username = data.get('username')
    password = data.get('password')
    level = data.get('level')
    print(level)
    #查询user表中每一行的name信息
    cursor.execute("select name from user")
    #fetchall()取出所有搜索结果
    names = cursor.fetchall()
    #查找注册的用户名是否重复
    for name in names:
        if name[0] == username:
            print('用户名相同')
            return 'existed'
    
    #插入语句
    sql= '''INSERT INTO user(name,
            password, level)
            VALUES (%s,%s,%s) '''
    values = (username,password,level)
    try:
        #执行sql语句
        cursor.execute(sql,values)
        #提交到数据库运行
        db.commit()
    except:
        #如果发生错误则回滚
        db.rollback()
    return 'success'

def login(data):
    username = data.get('username')
    password = data.get('password')
    #获取用户名列表

    cursor.execute("select name,password,level from user")
    #account中以元组形式保存了name和password
    account = cursor.fetchall()
    #print('让我们来看看names里面是什么',names)
    #print('让我们来看看passwords里面是什么',passwords)
    for a in account:
        if a[0] == username:
            if a[1] == password:
                return 'success'+','+a[2] #找到用户了 登陆成功 a[2]表示等级
    return 'non-exited,none'
    


while 1:#服务器无限循环
    conn,addr = s.accept()# 开始被动接受TCP客户端的连接。
    print('连接的地址'+repr(addr))
    print('进来了')
    #接下来一定要在while True循环里一直获取信息，不然完成一次传输就会出错卡死
    while True:#通讯循环
        data=conn.recv(1024)#这里得到的data是字节类型
        #一定要判空 因为当连接的客户端断开时，收到的就是空字符串，会导致json.loads报错
        if not data:
            print("客户端已断开连接")
            break
        print(data.decode('utf-8'))
        data = data.decode('utf-8')
        data = json.loads(data)#将data变为字典
        print(type(data))
        if data.get('function') == 'register':
            print('开始注册')
            response = register(data)#注册
        elif data.get('function') == 'login':
            print('登陆验证')
            response = login(data)#登陆
        elif data.get('function') == 'calculate':
            print('开始计算')
            response = calculate(data)#计算器  response是浮点数
            print(response)
            response = str(response)
        elif data.get('function') == 'upload':
            print('开始接受文件')
            response = upload(data)#管理员上传文件
        elif data.get('function') == 'download':
            print('收到下载文件的请求')
            response = download(data)#用户下载文件
        elif data.get('function') == 'create_dir':
            print('创建新文件夹')
            response = create_dir(data)#创建新文件夹
        elif data.get('function') == 'go_back':
            print('返回上一层')
            response = go_back(data)#返回上一层
        elif data.get('function') == 'check_file':
            print('查看文件夹信息')
            response = check_file(data)#查看文件夹信息
        elif data.get('function') == 'user_upload':
            print('数据处理器:用户上传文件')
            response = user_upload(data)
        elif data.get('function') == 'user_download':
            print('数据处理器:用户要下载自己的文件')
            response = user_download(data)

        #print('接收到了'+repr(data))
        #t='我已经收到了你的内容:'+str(data)
        #conn.sendall(bytes('我已经收到了你的内容：'+repr(data),'utf-8'))
        #conn.sendall(t.encode('utf-8'))
        conn.sendall(response.encode('utf-8'))
    conn.close()
#conn.close()