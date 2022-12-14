# Generated by Django 4.1.3 on 2022-12-05 20:09

from django.db import migrations, models
import django.db.models.deletion
import quiz.models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_category_remove_quiz_name_quiz_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question', validators=[quiz.models.validate_correct_check], verbose_name='Вопрос'),
        ),
    ]
