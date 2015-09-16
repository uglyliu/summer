#!/usr/bin/python

import paramiko

DEFAULT_USERNAME = 'tomcat'
DEFAULT_KEY_FILE = '~/.ssh/id_rsa'


def trans_data(hostname, key_file=DEFAULT_KEY_FILE, remote_path=None, local_path=None):
    t = paramiko.Transport((hostname, 22))
    key = paramiko.RSAKey.from_private_key_file(key_file)
    t.connect(username=DEFAULT_USERNAME, pkey=key)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(local_path, remote_path)
    t.close()


def command(hostname, key_file=DEFAULT_KEY_FILE, command=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, 22, DEFAULT_USERNAME, key_filename=key_file)
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        if stderr.readlines():
            return False
        else:
            return True
    finally:
        ssh.close()


def command_with_result(hostname, key_file=DEFAULT_KEY_FILE, command=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, 22, DEFAULT_USERNAME, key_filename=key_file)
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        return stdout.readlines()
    finally:
        ssh.close()
