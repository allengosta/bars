from django import forms
from django.core.exceptions import PermissionDenied
from django.db.models import Count

from .models import Candidate, Answer, Teacher
from django.db import IntegrityError


class CandidateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control row-sm-3',
            'placeholder' : 'Введите имя...'
        }
    ), label='Имя', max_length=100)
    age = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-control row-sm-3',
            'placeholder' : 'Введите возраст...'
        }
    ), label='Возраст')
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control row-sm-3',
            'placeholder' : 'Введите email...'
        }
    ), label='Email', max_length=100)

    class Meta:
        model = Candidate
        exclude = ('teacher', )


class ChallengeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        candidate = kwargs.pop('candidate', None)
        questions = kwargs.pop('questions', None)
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.candidate = candidate
        for q in questions:
            print(q)
            self.fields[str(q[0])] = forms.BooleanField(label=q[1], required=False)

    def save(self):
        for k, v in self.cleaned_data.items():
            Answer.objects.create(question_id=k, candidate=self.candidate, answer=v)


class TeacherSelectForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.annotate(kolvo=Count('teacher_cand')).filter(kolvo__lte=3))


class AddStudent(forms.Form):
    add = forms.BooleanField(label='Выбрать кандидата', required=False)

    def save(self):
        if self.cleaned_data['add']:
            teacher = self.initial['teacher']
            candidate = self.initial['candidate']
            candidate.teacher = teacher
            candidate.save()
