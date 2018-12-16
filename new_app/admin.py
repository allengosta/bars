from django.contrib import admin

# Register your models here.
from new_app.models import Planet, Teacher, Candidate, Question, Answer, Challenge

admin.site.register(Planet)
admin.site.register(Teacher)
admin.site.register(Candidate)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Challenge)

