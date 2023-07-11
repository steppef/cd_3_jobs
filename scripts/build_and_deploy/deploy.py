import paramiko
import json


def get_credentials():
    return json.load(open('credentials.json'))


CREDENTIALS = get_credentials()
DEPLOY_CMD = 'sh deploy.sh'


def get_client():
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(CREDENTIALS['HOST'], username=CREDENTIALS['USERNAME'], password=CREDENTIALS['PASSWORD'])
    return client


def run_remote_cmd(client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)

    for line in iter(stdout.readline, ''):
        print(line, end='')


if __name__ == '__main__':
    client = get_client()
    run_remote_cmd(client, DEPLOY_CMD)
    client.close()
