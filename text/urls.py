from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin

from text import views
from text_project import settings

urlpatterns = [
    path('', views.home, name='text-home'),
    path('welcome/', views.welcome, name='text-welcome'),
    path('text_home/reload/', views.reload, name='reload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


