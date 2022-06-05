from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("latest_movie/", views.movie_mining),

    path('image-compressor/', views.image_compressor, name='image_compressor'),
    path("to_do/", views.to_do, name='to-do'),
]