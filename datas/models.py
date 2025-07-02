from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _

from devices.models import Device


class Data(models.Model):
    """
    """
    device = models.ForeignKey(Device, related_name='device_data', on_delete=models.CASCADE)
    field_1 = models.CharField(_('Поле 1'), max_length=10, null=True, blank=False)
    field_2 = models.CharField(_('Поле 2'), max_length=10, null=True, blank=False)
    field_3 = models.CharField(_('Поле 3'), max_length=10, null=True, blank=False)
    field_4 = models.CharField(_('Поле 4'), max_length=10, null=True, blank=False)
    field_5 = models.CharField(_('Поле 5'), max_length=10, null=True, blank=False)
    field_6 = models.CharField(_('Поле 6'), max_length=10, null=True, blank=False)
    field_7 = models.CharField(_('Поле 7'), max_length=10, null=True, blank=False)
    field_8 = models.CharField(_('Поле 8'), max_length=10, null=True, blank=False)
    field_9 = models.CharField(_('Поле 9'), max_length=10, null=True, blank=False)
    field_10 = models.CharField(_('Поле 10'), max_length=10, null=True, blank=False)
    api_key = models.CharField(_('Api key'), max_length=200, null=True, blank=True)  # api key
    remote_address = models.CharField(_('Ip адрес'), max_length=255)
    pub_date = models.DateTimeField(_('Дата добавления'), auto_now=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.device.name
