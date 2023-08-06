user = ""
port = ""

pwd = ""  # 密码登录
root_pwd = ""  # root密码登录

key = ""  # 密钥登录
root_key = ""  # root密钥登录

tbj_pem = ""  # 跳板机序号


# 当pwd为空时采用ssh(OPENSSH方式)免密登录

server_dict = {
    "vpc实例名称": {"host": "外网地址", "user": "用户名", "port": "端口号", "pwd": "密码", "key": "密钥文件路径"},
    "tbj": {"host": "", "user": "", "port": "22", "pwd": "", "pem": tbj_pem},
    "233": {"host": "", "user": "", "port": "22", "pwd": ""},
}
