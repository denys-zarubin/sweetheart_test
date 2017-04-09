from django.conf import settings
from django.db import models


class SelectedAnswersManager(models.Manager):
    def initials(self):
        return self.filter(is_friend=False)


class QuestionsManager(models.Manager):
    def random_questions(self):
        return self.order_by('?')[:settings.QUESTIONS_PER_QUIZ]
