from django.db import models
from django.utils import timezone

from users.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    trans_id = models.CharField(max_length=20, null=True, blank=True, verbose_name='Transaction ID')
    trans_ref = models.CharField(max_length=100, null=True, blank=True, verbose_name="Transaction Reference")
    status = models.CharField(max_length=20, default='not completed', blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    amount = models.CharField(null=True, blank=True, max_length=20)

    def __str__(self):
        return self.trans_ref or f"{self.user} - pending transaction"
