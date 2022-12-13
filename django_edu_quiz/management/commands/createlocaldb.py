from django.core.management.base import BaseCommand, CommandError
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Создает файл настроек settings_local.py и новый экземпляр БД Sqlite'

    def handle(self, *args, **options):
        dir = os.path.abspath(__file__)
        dir = dir[:-36] + 'settings_local.py'
        if Path(dir).is_file():
            self.stdout.write(self.style.ERROR('Файл settings_local.py существует или был создан ранее'))
        else:
            with open(dir, 'w') as s:
                local_settings = r"""
from pathlib import Path


DEBUG = True
ALLOWED_HOSTS = ['*']
BASE_DIR = Path(__file__).resolve().parent.parent


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""
                s.write(local_settings)
                s.close()
            self.stdout.write(self.style.SUCCESS('Создан файл настроек settings_local.py '
                                                 'можете внести в него изменения'))
