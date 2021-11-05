
from django.core.management import BaseCommand

from press.mediastack_manager import gather_and_create_news


def format(s: str) -> str:
    s = list(map((lambda a: a.split(',')), s))
    s = [j for sub in s for j in sub]
    return s

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('categories', nargs='+', help='The categories to be pulled information from')
        parser.add_argument('--languages', nargs='+', help='The languages to be pulled information from', default=['en'])
        parser.add_argument('--countries', nargs='+', help='The countries to be pulled information from', default=['us'])
        parser.add_argument('--limit', type=int, help='Limit of posts to be added')

    def handle(self, *args, **options):
        limit = options['limit']
        categories = format(options['categories'])
        languages = format(options['languages'])
        countries = format(options['countries'])

        gather_and_create_news(categories, languages, limit, countries)

        self.stdout.write(f'We are running our first command with limit: {limit}, categories {categories}, languages {languages} and countries {countries}')
