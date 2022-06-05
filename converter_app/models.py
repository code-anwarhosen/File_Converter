from statistics import mode
from urllib import request
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import uuid
from PIL import Image
import os

# Create your models here.
class Movies(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    link = models.URLField(max_length=700, blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

# Image compressor start here 
def file_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    return "compressor/compressed_{filename}{extension}".format(filename=basefilename, extension=file_extension)

class Image_Compress(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to=file_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if self.image:
            if img.height >= 2000 or img.width >= 2000:
                _width, _height = img.size
                img = img.resize((_width//2, _height//2), Image.ANTIALIAS)
                img.save(self.image.path)
            elif img.height >= 1000 or img.width >= 1000:
                image_size = (1000, 1500)
                img.thumbnail(image_size, Image.LANCZOS)
                img.save(self.image.path)
            else:
                img.save(self.image.path)
    def __str__(self):
        basefilename, file_extension= os.path.splitext(self.image.path)
        return basefilename.split('\\')[-1]+ f'_({self.id})'  +file_extension

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    todo = models.CharField(max_length=250, blank=False, null=False)
    is_complete = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.todo
    def save(self, *args, **kwargs):
        self.slug = slugify(uuid.uuid4())
        self.user = request.user
        return super().save(*args, **kwargs)