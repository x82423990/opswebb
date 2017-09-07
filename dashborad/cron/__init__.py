# coding:utf8
import paramiko, re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
hostname = '192.168.44.132'
pat = r'^#'
# 指定本地的RSA私钥文件,如果建立密钥对时设置的有密码，password为设定的密码，如无不用指定password参数
pkey = paramiko.RSAKey.from_private_key_file('cao')
# 建立连接
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname,
            port=22,
            username='xie',
            pkey=pkey)
stdin, stdout, stderr = ssh.exec_command('sudo crontab -l')
for i in stdout.readlines():
    if not re.match(pat, i):
        print i
