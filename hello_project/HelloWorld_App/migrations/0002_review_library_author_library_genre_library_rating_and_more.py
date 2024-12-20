# Generated by Django 5.1 on 2024-12-11 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HelloWorld_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('review_title', models.TextField()),
                ('review_content', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='library',
            name='author',
            field=models.TextField(default='n/a'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='library',
            name='genre',
            field=models.TextField(default='fiction'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='library',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='library',
            name='review_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='HelloWorld_App.review'),
        ),
        migrations.AddIndex(
            model_name='library',
            index=models.Index(fields=['content'], name='HelloWorld__content_f44e4b_idx'),
        ),
    ]
