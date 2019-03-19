#!/usr/bin/env python

import  paramiko

paramiko.util.log_to_file("hehe.log")

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="192.168.0.19",port=22,username="admin",look_for_keys=True,timeout=60)
stdin, stdout, stderr = ssh.exec_command('df -h')
result = stdout.read().decode("utf8") or stderr.read().decode("utf8")
stdin_tmp, stdout_tmp, stderr_tmp = ssh.exec_command('free -m')
result2 = stdout_tmp.read().decode("utf8") or stderr_tmp.read().decode("utf8")
print(result)
print(result2)
ssh.close()

# private_key = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
# transport = paramiko.Transport(('192.168.0.19', 22))
# # transport.connect(username='root', pkey=private_key)
# transport.start_client()
# # transport.auth_publickey(username="root",key=private_key)
# transport.auth_password(username="root",password="123321")

# ssh = paramiko.SSHClient()
# ssh._transport = transport
# stdin, stdout, stderr = ssh.exec_command('df -h')
# result = stdout.read().decode("utf8") or stderr.read().decode("utf8")
# print(result)
# # sftp = paramiko.SFTPClient.from_transport(transport)
# # sftp.put('./index.html','/opt/index.html_bak_123')
# # sftp.get("/opt/haha_202002181126.log", "/opt/haha/haha_202002181126123456.log")
#
# transport.close()