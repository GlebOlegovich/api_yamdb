# Generated by Django 2.2.16 on 2021-11-09 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'default_related_name': 'categories', 'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'default_related_name': 'ganres', 'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'default_related_name': 'titles', 'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='titles', through='reviews.Genre_title', to='reviews.Genre'),
        ),
    ]
