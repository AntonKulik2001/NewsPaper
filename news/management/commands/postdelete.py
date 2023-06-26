from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет все новости выбранной категории'

    def add_arguments(self, parser):
        parser.add_argument('postCategory', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы действительно хотите удалить все статьи категории {options["postCategory"]}? да/нет ')

        if answer != 'да':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(name=options['postCategory'])
            Post.objects.filter(postCategory=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Успешно удалены все новости из категории {category.name}'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категория не найдена '))