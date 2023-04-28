# Generated by Django 4.2 on 2023-04-28 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0002_rename_risposta_corretta_qa_correct_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qa',
            name='correct_answer',
        ),
        migrations.AlterField(
            model_name='qa',
            name='answer',
            field=models.CharField(max_length=3),
        ),
        migrations.CreateModel(
            name='CorrectAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.qa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]