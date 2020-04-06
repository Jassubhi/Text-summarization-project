from django.urls import path
from django.conf.urls.static import static
from . import views
from text_project import settings

urlpatterns = [
    path('', views.home, name='text-home'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
