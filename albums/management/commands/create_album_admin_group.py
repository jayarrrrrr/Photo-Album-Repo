from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create AlbumAdmin group'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='AlbumAdmin')
        if created:
            self.stdout.write(self.style.SUCCESS('Created AlbumAdmin group'))
        else:
            self.stdout.write('AlbumAdmin group already exists')
