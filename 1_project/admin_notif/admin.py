from django.contrib import admin
from .models import Notification, NotificationHistory, NotificationType

# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ('text', 'created_at', 'user', 'status', 'send_at')

admin.site.register(NotificationType)
admin.site.register(Notification)
admin.site.register(NotificationHistory)
# Register your models here.
