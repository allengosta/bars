
from django.conf.urls import url, include
from django.views.generic import TemplateView

from new_app import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'candidate/$', views.CandidateView.as_view(), name='add_candidate'),
    url(r'candidate/(?P<candidate_id>[0-9]+)/order/(?P<orden_id>[0-9]+)/$',
        views.ChallengeView.as_view(), name="try-challenge"),
    url(r'candidate/passed/$',
        TemplateView.as_view(template_name='added_candidate.html'), name='passed'),
    url(r'teacher/$', views.TeacherSelectView.as_view(), name='choose_teacher'),
    url(r'teacher/(?P<teach_id>[0-9]+)/candidate/list/$', views.TeacherView.as_view(), name='teacher'),
    url(r'teacher/(?P<teach_id>[0-9]+)/candidate/(?P<candidate_id>[0-9]+)/$',
        views.CandidateToPupilView.as_view(), name='candidate'),
    url(r'teacher/list/$', views.TeacherListView.as_view(({'get': 'list'})), name='teacher-list'),
    url(r'teacher/list/new/$', views.TeacherListMoreThanOneView.as_view({'get': 'list'}), name='teacher-new')
]