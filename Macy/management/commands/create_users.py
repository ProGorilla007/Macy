from django.core.management import BaseCommand
from Macy.tests.factories import UserFactory, NonActivatedUserFactory


class Command(BaseCommand):
    help = 'Create users'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            UserFactory.create()
