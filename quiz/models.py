from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from quiz import managers
from quiz.helpers import calculate_percent
from quiz.mixins import ModelWithTextMixin


class Question(ModelWithTextMixin, models.Model):
    objects = managers.QuestionsManager()


class Answer(ModelWithTextMixin, models.Model):
    question = models.ForeignKey(Question, verbose_name='Question', null=True, blank=True)


class Quiz(models.Model):
    def __unicode__(self):
        return "Game #".format(self.id)

    def get_questions(self):
        questions = self.selectedanswer_set.initials().values_list('question', flat=True)
        if not questions.exists():
            # Generate random questions
            questions = Question.objects.random_questions().values_list(
                'id', flat=True
            )
        return questions

    def get_user_answers(self, user):
        return self.selectedanswer_set.filter(user=user)

    def get_initial_answers(self):
        return self.selectedanswer_set.initials().values('question', 'answer')

    def match_answers(self, user):
        selected_answers = self.get_user_answers(user).values('question', 'answer')
        initial_answers = self.get_initial_answers()
        match = len(initial_answers.difference(selected_answers))
        total = len(initial_answers)
        percent = calculate_percent(match, total)
        return '{} of {} ({}%)'.format(match, total, percent)

    def get_absolute_url(self):
        return reverse('quiz-detail', kwargs={'pk': self.id})


class SelectedAnswer(models.Model):
    objects = managers.SelectedAnswersManager()

    quiz = models.ForeignKey(Quiz)
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    is_friend = models.BooleanField(default=False)

    def __unicode__(self):
        return "{} {}".format(self.question.text, self.answer.text)
