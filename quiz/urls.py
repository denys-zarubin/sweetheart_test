from django.conf.urls import url

from quiz import views

urlpatterns = [
    url(r'^results/(?P<pk>\d+)/$', views.QuizDetailView.as_view(), name='quiz-detail'),
    url(r'^(?P<pk>\d+)/$', views.NewQuizView.as_view(), name='new-quiz'),
    url(r'^$', views.NewQuizView.as_view(), name='new-quiz'),
]
