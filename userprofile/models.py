# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    middle_name = models.CharField(default='', blank=True, max_length=30, verbose_name='Отчество')
    about = models.TextField(default='', blank=True, max_length=300, verbose_name='Дополнительная информация')
    avatar = models.ImageField(upload_to='images/users', verbose_name='Изображение')
    phone_number = models.CharField(default='', blank=True, max_length=20, verbose_name='Номер  телефона')

    def __unicode__(self):
        return self.user_id.__str__()

    class Meta:
        db_table = "UserProfile"
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
