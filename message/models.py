from django.db import models
from django.utils.translation import ugettext_lazy as _
from .utils import format_comment


class Gateway(models.Model):
    name = models.CharField(max_length=120)
    account_number = models.CharField(
        max_length=100, help_text=_("accountnumber,username,accountid,apikey")
    )
    api_url = models.URLField(null=True, blank=True)
    password = models.CharField(max_length=100)
    configured_sender = models.CharField(max_length=120)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Gateway Detail")
        verbose_name_plural = _("Gateway Details")

    def __str__(self):
        return "{}{}".format(self.name, self.active)


class Message(models.Model):
    SUCCESS = "1"
    FAILURE = "0"

    status_message = ((SUCCESS, "success"), (FAILURE, "failure"))
    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=status_message)
    partner_message_id = models.CharField(max_length=80)
    status_code = models.IntegerField()
    recipient = models.CharField(max_length=40)
    response = models.TextField()

    def __str__(self):
        return self.partner_message_id

    def append_comment(self, prefix, comment):
        self.comments = format_comment(self.comments, prefix, comment)
