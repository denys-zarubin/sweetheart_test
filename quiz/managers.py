from django.db import models
from django.db.models import Q


class SelectedAnswersManager(models.Manager):
    def for_friends(self):
        return self.filter(is_friend=True)

    def initial(self):
        return self.filter(is_friend=False)

    def get_answer_by_question(self, question):
        self.filter(question=question)

    def is_matched(self):
        self.for_creator()
        self.filter()


class QuizManager(models.Manager):
    def matched_answers(self, user):
        self.selectedanswer_set.filter(Q(user=user) | Q(is_friend=False))
        return self.annotate().filter()
