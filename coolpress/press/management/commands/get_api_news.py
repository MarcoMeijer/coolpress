
from django.core.management import BaseCommand

from press.mediastack_manager import gather_and_create_news


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('categories', nargs='+', help='The categories to be pulled information from')
        parser.add_argument('--limit', type=int, help='Limit of posts to be added')

    def handle(self, *args, **options):
        limit = options['limit']
        categories = options['categories']
        categories = list(map((lambda a : a.split(',')), categories))
        categories = [j for sub in categories for j in sub]

        gather_and_create_news(categories, ['en'], limit)

        self.stdout.write(f'We are running our first command with limit: {limit} and categories {categories}')
