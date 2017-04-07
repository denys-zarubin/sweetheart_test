from django.db import models


class SelectedAnswersManager(models.Manager):
    def for_friends(self):
        return self.filter(is_friend=True)

    def initials(self):
        return self.filter(is_friend=False)

    def get_answer_by_question(self, question, user):
        self.filter(question=question, user=user)


class QuizManager(models.Manager):
    pass
