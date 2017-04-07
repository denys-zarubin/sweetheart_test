from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic as views
from extra_views import ModelFormSetView

from quiz import models, forms


class QuizDetailView(views.DetailView):
    model = models.Quiz
    template_name = 'quiz.html'

    def get_context_data(self, **kwargs):
        ctx = super(QuizDetailView, self).get_context_data(**kwargs)
        if self.object.selectedanswer_set.filter(user=self.request.user, is_friend=True):
            ctx['mathed_answers'] = self.object.match_answers(self.request.user)
        ctx['selected_answers'] = self.object.get_user_answers(self.request.user)
        return ctx


class NewQuizView(ModelFormSetView):
    template_name = 'quiz_new.html'
    form_class = forms.SelectedAnswersForm
    max_num = settings.QUESTIONS_PER_QUIZ
    model = models.SelectedAnswer

    def get_queryset(self):
        # Disable edit data
        return self.model.objects.none()

    def dispatch(self, request, pk=None, *args, **kwargs):
        # Create new game or play in existing one, basically check if is user new or friend
        self.is_friend = False
        self.quiz = models.Quiz()
        if pk:
            self.quiz = get_object_or_404(models.Quiz, id=pk)
            self.is_friend = True
        return super(NewQuizView, self).dispatch(request, pk, *args, **kwargs)

    def formset_valid(self, formset):
        if not self.request.user.is_authenticated() and self.request.method == "POST":
            self.request.session['post'] = self.request.POST
            # Facebook login
            print 'HERE'
            return HttpResponseRedirect(reverse("social:begin", args=["facebook"]))
        else:
            self.object_list = formset.save(commit=False)
            self.quiz.save()
            for obj in self.object_list:
                obj.quiz = self.quiz
                obj.is_friend = self.is_friend
                obj.user = self.request.user
            self.model.objects.bulk_create(self.object_list)
            self.request.session['post'] = None
            return HttpResponseRedirect(self.get_success_url())

    def get_formset_kwargs(self):
        kwargs = super(NewQuizView, self).get_formset_kwargs()
        kwargs['data'] = self.request.session.get('post', kwargs.get('data'))
        return kwargs

    def get_initial(self):
        initial = super(NewQuizView, self).get_initial()
        if not self.initial:
            questions = self.quiz.get_questions()
            for question in questions:
                initial.append({'question': question})
        return initial

    def get_success_url(self):
        return self.quiz.get_absolute_url()
