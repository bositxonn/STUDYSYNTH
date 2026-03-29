from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tariff(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Free, Basic, Premium")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField(default=30)
    features = models.TextField(help_text="Line-separated features list")

    def __str__(self):
        return f"{self.name} (${self.price})"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    tariff = models.ForeignKey(Tariff, on_delete=models.PROTECT)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.tariff.name}"
