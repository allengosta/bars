# Generated by Django 2.0.9 on 2018-12-16 07:00

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('new_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='teacher',
            managers=[
                ('with_padawans', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта кандидата'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='orden',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='new_app.Planet'),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='question',
            field=models.ManyToManyField(to='new_app.Question'),
        ),
    ]
