from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Room(models.Model):
    STATUS_CHOICES = [
        ('available', '可预订'),
        ('maintenance', '维护中'),
        ('busy', '忙碌'),
    ]
    name = models.CharField(max_length=100, unique=True, verbose_name="会议室名称")
    area = models.CharField(max_length=50, verbose_name="区域")
    floor = models.IntegerField(verbose_name="楼层")
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name="状态"
    )

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=100, verbose_name="参会人员姓名")

    def __str__(self):
        return self.name
