from django.db.models import Count
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import detail_route
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from new_app.serializers import CandidateSerializer, TeacherSerializer, TeacherListSerializer
from .forms import CandidateForm, ChallengeForm, AddStudent, TeacherSelectForm
from .models import Challenge, Candidate, Teacher


class CandidateView(CreateView):
    form_class = CandidateForm
    template_name = 'add_candidate.html'

    def get_success_url(self):
        return reverse('try-challenge', kwargs={'candidate_id': self.object.pk,
                                                'orden_id': self.object.planet_id})


'''class CandidateViewSet(generics.RetrieveAPIView):
    queryset = Candidate.objects.all()
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        return Response(template_name='add_candidate.html')'''


class ChallengeView(FormView):
    form_class = ChallengeForm
    template_name = 'add_challenge.html'
    success_url = reverse_lazy('passed')

    def get_form_kwargs(self):
        candidate_id = self.kwargs.get('candidate_id', None)
        candidate = get_object_or_404(Candidate, id=candidate_id)
        orden_id = self.kwargs.get('orden_id', None)
        questions = get_object_or_404(Challenge, orden_id=orden_id).question.all()
        form_kwargs = super(ChallengeView, self).get_form_kwargs()
        form_kwargs['candidate'] = candidate
        form_kwargs['questions'] = [(q.id, q.question_name) for q in questions]
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super(ChallengeView, self).form_valid(form)


class TeacherView(ListView):
    template_name = 'teacher_candidates.html'
    context_object_name = 'candidates'

    def get_queryset(self):
        teach_id = self.kwargs.get('teach_id', None)
        teach = get_object_or_404(Teacher, id=teach_id)
        return Candidate.objects.filter(planet=teach.planet, teacher__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(TeacherView, self).get_context_data(**kwargs)
        context['teach_id'] = self.kwargs['teach_id']
        return context


class CandidateToPupilView(DetailView, FormMixin):
    model = Candidate
    template_name = 'candidate_detail.html'
    pk_url_kwarg = 'candidate_id'
    form_class = AddStudent
    success_url = '/'

    def get_initial(self):
        candidate_id = self.kwargs.get('candidate_id', None)
        candidate = get_object_or_404(Candidate, id=candidate_id)
        teach_id = self.kwargs.get('teach_id', None)
        teacher = get_object_or_404(Teacher, id=teach_id)
        return {'candidate': candidate,
                'teacher': teacher}

    def form_valid(self, form):
        form.save()
        return super(CandidateToPupilView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TeacherListView(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    renderer_classes = (TemplateHTMLRenderer,)

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.annotate(
            kolvo=Count('teacher_cand')
        )
        return Response({'teacher': self.queryset.all()},
                        template_name='list_teachers.html')  # super().list(request, *args, **kwargs)


class TeacherListMoreThanOneView(mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'list_teachers.html'

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.annotate(
            kolvo=Count('teacher_cand')
        ).filter(kolvo__gt=1)
        return Response({'teacher': self.queryset.all()}, template_name='list_teachers.html')
        # return super().list(request, *args, **kwargs)


class TeacherSelectView(FormView):
    form_class = TeacherSelectForm
    template_name = 'select_teachers.html'

    def form_valid(self, form):
        return redirect(reverse('teacher', kwargs={'teach_id': form.cleaned_data['teacher'].id}))
