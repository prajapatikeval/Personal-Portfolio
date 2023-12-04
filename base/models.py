from django.db import models
import uuid
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(null=True)
    body = RichTextUploadingField()
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    live_website = models.CharField(max_length=200,blank=True)
    source_code = models.CharField(max_length=200,blank=True)
    languages = models.ManyToManyField(Language)
    Technologies = models.ManyToManyField(Technology)

    def __str__(self):
        return self.title

class ProfilePicture(models.Model):
    photo = models.ImageField(null=True)
    resume = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo has Been created on {self.created_at}"

class AboutMe(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    body = RichTextUploadingField()

    def __str__(self):
        return self.body

class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    logo = models.ImageField(null=True, default="Skill_image.png")
    body = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    subject = models.CharField(max_length=200,null=True)
    body = models.TextField()
    is_read = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    