from django.core.management import BaseCommand
from Macy.tests.factories import LinksFactory
from Macy.models import User

class Command(BaseCommand):
    help = 'Create users'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('user_id', type=int, help='Indicates the number of users to be created')
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        user = User.objects.get(id=kwargs['user_id'])
        for i in range(total):
            LinksFactory.create(user_id=user)
