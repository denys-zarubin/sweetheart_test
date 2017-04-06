from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from quiz import managers
from quiz.helpers import calculate_percent


class Question(models.Model):
    text = models.CharField(
        max_length=255,
        verbose_name='Text',
        null=True,
        blank=True
    )

    def __str__(self):
        return '{}?'.format(self.text)


class Answer(models.Model):
    text = models.CharField(max_length=255, verbose_name='Text')
    question = models.ForeignKey(Question, verbose_name='Question', null=True, blank=True)

    def __str__(self):
        return '{}? {}'.format(self.question.text, self.text)


class Quiz(models.Model):
    objects = managers.QuizManager()

    shared_link = models.URLField(verbose_name='Link for share')

    def get_user_answers(self, user):
        return self.selectedanswer_set.filter(user=user)

    def get_initial_answers(self):
        return dict(self.selectedanswer_set.initial().values_list('question', 'answer'))

    def match_answers(self, user):
        selected_answers = self.get_user_answers(user).values_list('question', 'answer')
        initial_answers = self.get_initial_answers()
        match = 0
        total = len(selected_answers)
        for question, answer in selected_answers:
            if initial_answers[question] == answer:
                match += 1
        percent = calculate_percent(match, total)
        return match, total, percent


class SelectedAnswer(models.Model):
    objects = managers.SelectedAnswersManager()

    quiz = models.ForeignKey(Quiz)
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    is_friend = models.BooleanField(default=True)

    class Meta:
        unique_together = ['quiz', 'user', 'question', 'answer']
