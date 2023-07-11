import argparse
import json
import paramiko


def read_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--rollback-migration-app-name', help='Название приложения')
    parser.add_argument('--rollback-migration-number-before', help='Номер миграции до, которую надо откатить')

    return parser.parse_args()


def get_credentials():
    return json.load(open('credentials.json'))


CREDENTIALS = get_credentials()
ROLLBACK_MIGRATION_CMD = 'sh rollback_migration.sh'


def get_client():
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(CREDENTIALS['HOST'], username=CREDENTIALS['USERNAME'], password=CREDENTIALS['PASSWORD'])
    return client


def run_remote_cmd(client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd, get_pty=True)

    for line in iter(stdout.readline, ''):
        print(line, end='')


def rollback_migration():
    args = read_args()
    if not args.rollback_migration_app_name or not args.rollback_migration_number_before:
        print('Нужно указать название приложения и номер предшествующей миграции, которую надо откатить')
        return

    client = get_client()

    cmd = f'{ROLLBACK_MIGRATION_CMD} {args.rollback_migration_app_name} {args.rollback_migration_number_before}'
    print(f'Запускаем комманду: {cmd}')
    run_remote_cmd(client, cmd)
    print('Завершили')

    client.close()


if __name__ == '__main__':
    rollback_migration()
