import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from quiz import models
from quiz.helpers import generate_random_text


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

    def generate_questions_with_answers(self, **options):
        questions_count = options['questions_count']
        questions = []
        for i in xrange(questions_count):
            obj = models.Question.objects.create(text=generate_random_text())
            for i in xrange(random.randint(1, 5)):
                models.Answer.objects.create(question=obj, text=generate_random_text())
            questions.append(obj)
        return questions

    def generate_choosen_answers(self, quiz, questions, user, is_friend=False):
        for question in questions:
            answer = random.choice(question.answer_set.all())
            models.SelectedAnswer.objects.create(
                quiz=quiz,
                user=user,
                is_friend=is_friend,
                question=question,
                answer=answer
            )

    def handle(self, *args, **options):
        if options['clean']:
            models.Quiz.objects.all().delete()
        questions = self.generate_questions_with_answers(**options)
        user1 = User.objects.create(username=generate_random_text(5))
        user2 = User.objects.create(username=generate_random_text(5))
        quiz = models.Quiz.objects.create(shared_link='http://google.com/')
        self.generate_choosen_answers(quiz, questions, user1)
        self.generate_choosen_answers(quiz, questions, user2, is_friend=True)
        print quiz.match_answers(user2)
