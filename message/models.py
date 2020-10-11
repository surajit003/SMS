from django.db import models
from django.utils.translation import ugettext_lazy as _


class Gateway(models.Model):
    name = models.CharField(max_length=120)
    account_number = models.CharField(
        max_length=100, help_text=_("accountnumber,username,accountid,apikey")
    )
    password = models.CharField(max_length=100)
    configured_sender = models.CharField(max_length=120)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Gateway Detail")
        verbose_name_plural = _("Gateway Details")

    def __str__(self):
        return "{}{}".format(self.name, self.active)
