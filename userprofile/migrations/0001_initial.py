# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('middle_name', models.CharField(verbose_name='Отчество', default='', max_length=30, blank=True)),
                ('about', models.TextField(verbose_name='Дополнительная информация', default='', max_length=300, blank=True)),
                ('avatar', models.ImageField(verbose_name='Изображение', upload_to='images/users')),
                ('phone_number', models.CharField(verbose_name='Номер  телефона', default='', max_length=20, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'db_table': 'UserProfile',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
