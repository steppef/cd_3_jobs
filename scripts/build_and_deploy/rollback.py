import json
import paramiko


def get_credentials():
    return json.load(open('credentials.json'))


CREDENTIALS = get_credentials()
ROLLBACK_CMD = 'sh rollback.sh'


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
    prompt_value = input("А ты откатил миграции (Y|N)?")

    if prompt_value == 'Y':
        client = get_client()

        print('Начинаем роллбэк...')
        run_remote_cmd(client, ROLLBACK_CMD)
        print('Завершили роллбэк')

        client.close()
