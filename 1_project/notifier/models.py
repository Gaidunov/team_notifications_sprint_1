import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class NotificationType(UUIDMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Notification(UUIDMixin):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    recipients = ArrayField(models.UUIDField(default=uuid.uuid4, editable=False), blank=True)
    status = models.CharField(max_length=255)
    send_at = models.DateTimeField(auto_now=True)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    timezone = models.CharField(max_length=10)


class NotificationHistory(UUIDMixin):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user_id_auth = models.UUIDField(editable=False)
    adres = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
