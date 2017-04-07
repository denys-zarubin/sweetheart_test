import random
import string

from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode


def generate_random_text(length=15):
    """
    :param length: Default 15
    :return: Random string
    """
    return "".join(
        [random.choice(string.letters[:26]) for i in xrange(length)]
    )


def calculate_percent(val, total):
    """
    Used to calculate how much in percent is value
    """
    return int(val / float(total) * 100)


def generate_questions_with_answers(questions_count=None):
    from quiz import models
    questions_count = questions_count or settings.QUESTIONS_PER_QUIZ
    questions = []
    for i in xrange(questions_count):
        obj = models.Question.objects.create(text=generate_random_text())
        for i in xrange(random.randint(1, 5)):
            models.Answer.objects.create(question=obj, text=generate_random_text())
        questions.append(obj)
    return questions


def generate_choosen_answers(quiz, questions, user, is_friend=False):
    from quiz import models
    for question in questions:
        answer = random.choice(question.answer_set.all())
        models.SelectedAnswer.objects.create(
            quiz=quiz,
            user=user,
            is_friend=is_friend,
            question=question,
            answer=answer
        )


def reverse_with_params(viewname, kwargs=None, query_kwargs=None):
    """
    Custom reverse to add a query string after the url
    Example usage:
    url = my_reverse('my_test_url', kwargs={'pk': object.id}, query_kwargs={'next': reverse('home')})
    """
    url = reverse(viewname, kwargs=kwargs)

    if query_kwargs:
        return u'%s?%s' % (url, urlencode(query_kwargs))

    return url
