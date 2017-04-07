from django.core.management.base import BaseCommand

from quiz import models
from quiz.helpers import generate_questions_with_answers


class Command(BaseCommand):
    help = 'Generate Questions'

    def add_arguments(self, parser):
        parser.add_argument(
            'questions_count',
            nargs='?',
            type=int,
            default=10,
        )
        parser.add_argument(
            '--clean',
            action='store_true',
            dest='clean',
            default=False
        )

    def handle(self, *args, **options):
        if options['clean']:
            models.Question.objects.all().delete()
        questions = generate_questions_with_answers(options['questions_count'])
        print questions
