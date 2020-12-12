import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """
    Setups default class representation and adds created_date and
    modified_date database fields.
    """
    id = models.UUIDField(_("id"), primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    modified_date = models.DateTimeField(_("modified date"), auto_now=True)

    class Meta:
        abstract = True

    @property
    def is_new(self):
        return not self.created_date


def _get_default_sensitive_data():
    return SensitiveData.objects.create().id


class SensitiveData(BaseModel):
    data = models.CharField(blank=True, null=True, max_length=255)


class User(AbstractUser, BaseModel):
    sensitive_data = models.OneToOneField(to='myapp.SensitiveData',
                                          on_delete=models.CASCADE,
                                          default=_get_default_sensitive_data,
                                          related_name='user',
                                          verbose_name=_('Sensitive Data'))

