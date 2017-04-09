from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic as views
from extra_views import ModelFormSetView

from quiz import models, forms


class QuizDetailView(views.DetailView):
    model = models.Quiz
    template_name = 'quiz/quiz_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(QuizDetailView, self).get_context_data(**kwargs)
        user = self.request.user
        users_answers = self.object.get_user_answers(user).select_related('answer', 'question')
        if users_answers.filter(is_friend=True).exists():
            ctx['mathed_answers'] = self.object.match_answers(user)
        ctx['selected_answers'] = users_answers
        return ctx


class QuizCreateView(ModelFormSetView):
    template_name = 'quiz/quiz_new.html'
    form_class = forms.SelectedAnswersForm
    max_num = settings.QUESTIONS_PER_QUIZ
    model = models.SelectedAnswer

    def get_queryset(self):
        # Disable edit data
        return self.model.objects.none()

    def get_object(self, request, pk=None):
        if pk:
            return get_object_or_404(
                models.Quiz,
                id=pk,
            )
        return models.Quiz()

    def dispatch(self, request, pk=None, *args, **kwargs):
        self.is_friend = pk is not None
        self.quiz = self.get_object(request, pk)
        if request.user.is_authenticated() and self.quiz.get_user_answers(request.user):
            return HttpResponseRedirect(self.quiz.get_absolute_url())
        return super(QuizCreateView, self).dispatch(request, pk, *args, **kwargs)

    def formset_valid(self, formset):
        if not self.request.user.is_authenticated() and self.request.method == "POST":
            # Save data to session and redirect to facebook login
            self.request.session['post'] = self.request.POST
            return HttpResponseRedirect(reverse("social:begin", args=["facebook"]))
        self.object_list = formset.save(commit=False)
        self.quiz.save()
        for obj in self.object_list:
            obj.quiz = self.quiz
            obj.is_friend = self.is_friend
            obj.user = self.request.user
        self.model.objects.bulk_create(self.object_list)
        return HttpResponseRedirect(self.get_success_url())

    def get_formset_kwargs(self):
        kwargs = super(QuizCreateView, self).get_formset_kwargs()
        if 'post' in self.request.session:
            kwargs['data'] = self.request.session.pop('post')
        return kwargs

    def get_initial(self):
        initial = super(QuizCreateView, self).get_initial()
        questions = self.quiz.get_questions()
        for question in questions:
            initial.append({'question': question})
        return initial

    def get_success_url(self):
        return self.quiz.get_absolute_url()
