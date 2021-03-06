from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from quiz import models
from quiz.helpers import generate_random_text, generate_questions_with_answers, generate_choosen_answers


class Command(BaseCommand):
    help = 'Generate Quiz'

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
            models.Quiz.objects.all().delete()
        questions = generate_questions_with_answers(options['questions_count'])
        user1 = User.objects.create(username=generate_random_text(5))
        user2 = User.objects.create(username=generate_random_text(5))
        quiz = models.Quiz.objects.create()
        generate_choosen_answers(quiz, questions, user1)
        generate_choosen_answers(quiz, questions, user2, is_friend=True)
        print quiz.match_answers(user2)
