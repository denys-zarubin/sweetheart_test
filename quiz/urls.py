from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from quiz import views

urlpatterns = [
    url(r'^results/(?P<pk>\d+)/$', login_required(views.QuizDetailView.as_view()), name='quiz-detail'),
    url(r'^(?P<pk>\d+)/$', views.QuizCreateView.as_view(), name='new-quiz'),
    url(r'^$', views.QuizCreateView.as_view(), name='new-quiz'),
]
