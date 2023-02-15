from django.db import models
from django.contrib.auth.models import User


class NotificationType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Notification(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    recipients = models.ManyToManyField(User)
    status = models.CharField(max_length=255)
    send_at = models.DateTimeField(auto_now=True)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=10)


class NotificationHistory(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user_id_auth = models.UUIDField(editable=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
