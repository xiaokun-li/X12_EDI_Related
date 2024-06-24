# _*_ coding:utf-8 _*_

import paramiko
from pathlib import Path

class SFTPClient:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.sftp = None

    def connect(self):
        # 创建SSH对象
        self.client = paramiko.SSHClient()
        # 允许连接不在known_hosts列表的服务器
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        self.client.connect(self.hostname, self.port, self.username, self.password)
        # 创建SFTP会话
        self.sftp = self.client.open_sftp()

    def upload_file(self, local_path, remote_path):
        # 上传文件
        try:
            self.sftp.put(local_path, remote_path)
            print(f"文件已上传到 {remote_path}")
        except Exception as e:
            print(f"上传文件失败: {e}")

    def close(self):
        # 关闭SFTP会话和SSH连接
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()

# 使用示例
if __name__ == "__main__":
    # SFTP服务器信息
    hostname = 'sftp.example.com'
    port = 22  # SFTP端口，默认为22
    username = 'your_username'
    password = 'your_password'

    # 本地文件路径和远程文件路径
    local_path = 'path/to/your/edi_file.edi'
    remote_path = '/remote/directory/edi_file.edi'

    # 创建SFTP客户端
    sftp_client = SFTPClient(hostname, port, username, password)

    # 连接到SFTP服务器
    sftp_client.connect()

    # 上传文件
    sftp_client.upload_file(local_path, remote_path)

    # 关闭连接
    sftp_client.close()