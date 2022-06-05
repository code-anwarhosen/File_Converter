from re import T
from django.contrib import admin
from .models import Movies, Image_Compress, Task
# Register your models here.
admin.site.register(Movies)
admin.site.register(Image_Compress)
admin.site.register(Task)