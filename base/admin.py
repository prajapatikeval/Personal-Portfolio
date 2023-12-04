from django.contrib import admin
from .models import Project, Skill, Tag, Message, AboutMe, ProfilePicture
# Register your models here.

admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(Tag)
admin.site.register(Message) 
admin.site.register(AboutMe)  
admin.site.register(ProfilePicture)  