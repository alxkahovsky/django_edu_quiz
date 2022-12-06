# Generated by Django 4.1.3 on 2022-12-06 09:08

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_question_answer_a_question_answer_b_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('A', 'Вариант A'), ('B', 'Вариант B'), ('C', 'Вариант C'), ('D', 'Вариант D')], max_length=2),
        ),
    ]
