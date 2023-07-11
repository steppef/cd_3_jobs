import argparse
import subprocess
import os

REGISTRY_NAME = 'kairkhan'
REGISTRY_USERNAME = 'kairkhan'

DJANGO_SERVICE_IMAGE_NAME = 'back_end'
DJANGO_SERVICE_PATH = os.path.abspath('../../')
VISION_SERVICE_IMAGE_NAME = 'vision'
VISION_SERVICE_PATH = os.path.abspath('../../src/vision')
VERME_SERVICE_IMAGE_NAME = 'verme'
VERME_SERVICE_PATH = os.path.abspath('../../src/verme')

RELEASE_TAG = 'master'
ROLLBACK_TAG = 'rollback'

RELEASE_GIT_BRANCH = 'main'


class Log:
    @classmethod
    def success(cls, msg):
        OKGREEN = '\033[92m'
        ENDC = '\033[0m'
        print(OKGREEN + msg + ENDC)

    @classmethod
    def error(cls, msg):
        FAILRED = '\033[91m'
        ENDC = '\033[0m'
        print(FAILRED + msg + ENDC)

    @classmethod
    def info(cls, msg):
        INFOBLUE = '\033[94m'
        ENDC = '\033[0m'
        print(INFOBLUE + msg + ENDC)


class Git:
    def __init__(self):
        self.release_commit = self.get_current_commit()

    def move_to_commit(self, commit):
        os.system(f'git checkout {commit}')

    def move_to_release_commit(self):
        os.system(f'git checkout {RELEASE_GIT_BRANCH}')

    @classmethod
    def get_current_commit(cls):
        os.chdir(DJANGO_SERVICE_PATH)
        return subprocess.getoutput('git log -n1 --format="%h"')


def read_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--rollback-commit', help='If You Deploy Failed You Can Rollback To')
    parser.add_argument('--django-service', action='store_true', help='Build Django Service')
    parser.add_argument('--vision-service', action='store_true',  help='Build Vision Service')
    parser.add_argument('--verme-service', action='store_true', help='Build Verme Service')

    return parser.parse_args()


def build_and_push_image(path_to_move, image_name, tag_name):
    image_with_tag = f'{image_name}:{tag_name}'

    os.system(f'cd {path_to_move}')

    os.system(f'docker build --tag={image_with_tag} .')
    os.system(f'docker tag {image_with_tag} {REGISTRY_NAME}/{image_with_tag}')
    os.system(f'docker push {REGISTRY_NAME}/{image_with_tag}')

    Log.success(f'finished to build image: {image_name} with tag: {tag_name} and commit: {Git.get_current_commit()}')


def build_and_push():
    args = read_args()
    if not args.rollback_commit:
        Log.error('Нужно указать коммит, на который нужно откатиться в случае проблем деплоя: git log --oneline')
        return

    git = Git()

    if args.django_service:
        git.move_to_release_commit()
        build_and_push_image(DJANGO_SERVICE_PATH, DJANGO_SERVICE_IMAGE_NAME, RELEASE_TAG)

        Log.success(f'roll {args.rollback_commit}')

        git.move_to_commit(args.rollback_commit)
        build_and_push_image(DJANGO_SERVICE_PATH, DJANGO_SERVICE_IMAGE_NAME, ROLLBACK_TAG)

    if args.vision_service:
        git.move_to_release_commit()
        build_and_push_image(VISION_SERVICE_PATH, VISION_SERVICE_IMAGE_NAME, RELEASE_TAG)

        git.move_to_commit(args.rollback_commit)
        build_and_push_image(VISION_SERVICE_PATH, VISION_SERVICE_IMAGE_NAME, ROLLBACK_TAG)

    if args.verme_service:
        git.move_to_release_commit()
        build_and_push_image(VERME_SERVICE_PATH, VERME_SERVICE_IMAGE_NAME, RELEASE_TAG)

        git.move_to_commit(args.rollback_commit)
        build_and_push_image(VERME_SERVICE_PATH, VERME_SERVICE_IMAGE_NAME, ROLLBACK_TAG)

    git.move_to_release_commit()


if __name__ == '__main__':
    build_and_push()
