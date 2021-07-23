from django.apps import apps
from django.contrib import admin

from .models import User_profile, Tutor, Room, Message

class User_profileModelAdmin(admin.ModelAdmin):
	list_display = ('user', 'location')
	list_search_fields = ('user', 'location')
    
class TutorModelAdmin(admin.ModelAdmin):
	list_display = ('user', 'location', 'resume', 'degree', 'verify')
	list_search_fields = ('user', 'location', 'resume', 'degree', 'verify')

class RoomModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'user1', 'user2')
    list_search_fields = ('name', 'user1', 'user2')
    
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ('room', 'author', 'content')
    list_search_fields = ('room', 'author', 'content')
    
admin.site.register(User_profile, User_profileModelAdmin)
admin.site.register(Tutor, TutorModelAdmin)
admin.site.register(Room,RoomModelAdmin)
admin.site.register(Message, MessageModelAdmin)