from django.contrib import admin
from .models import Room,Message,Topic

class TopicAdmin(admin.ModelAdmin):
    list_display = ['title']

class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'description', 'topic', 'owner', 'created_at']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['body', 'user', 'room', 'created_at']

# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)