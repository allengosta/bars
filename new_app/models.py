from django.db import models


class Planet(models.Model):
    class Meta:
        verbose_name = 'Планета'
        verbose_name_plural = 'Планеты'

    name = models.CharField('Наименование планеты', max_length=100, blank=False, null=False,)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    class Meta:
        verbose_name = 'Джедай'
        verbose_name_plural = 'Джедаи'

    name = models.CharField('Имя джедая', max_length=100, blank=False, null=False,)
    planet = models.ForeignKey(Planet, verbose_name='Джедай планеты', related_name='teacher_planet', blank=True,
                               null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    name = models.CharField('Имя кандидата', max_length=100, blank=False, null=False,)
    planet = models.ForeignKey(Planet, verbose_name='Кандидат планеты', related_name='candidate_planet', blank=True,
                               null=True, on_delete=models.SET_NULL)
    age = models.IntegerField('Возраст', blank=True, null=True)
    email = models.EmailField('Почта кандидата', blank=True, null=True)
    teacher = models.ForeignKey(Teacher, verbose_name='Джедай планеты', related_name='teacher_cand', blank=True,
                               null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return '%s, %s, %s' % (self.name, self.age, self.planet.name)


class Question(models.Model):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    question_name = models.CharField('Вопрос для кандидата', max_length=255, blank=False, null=False,)
    checked = models.BooleanField('Правильный ответ', default=True)

    def __str__(self):
        return '%s, %s' % (self.question_name, self.checked)


class Answer(models.Model):
    class Meta:
        verbose_name = 'Ответ кандидата'
        verbose_name_plural = 'Ответы кандидата'

    candidate = models.ForeignKey(Candidate, verbose_name='Ответ кандидата', related_name='candidate_answer', blank=True,
                               null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, verbose_name='Вопрос для кандидата', related_name='candidate_question', blank=True,
                               null=True, on_delete=models.SET_NULL)
    answer = models.BooleanField('Ответ кандидата', default=True)

    def __str__(self):
        return '%s, %s' % (self.question.question_name, self.answer)


class Challenge(models.Model):
    class Meta:
        verbose_name = 'Испытание'
        verbose_name_plural = 'Испытания'

    position = models.PositiveSmallIntegerField('Порядковый номер', blank=False, null=False, default=0)
    orden = models.OneToOneField(Planet, on_delete=models.CASCADE)
    question = models.ManyToManyField(Question)

