from django.urls import path
from .views import bot, health_check


urlpatterns = [
    path('webhook/', bot),
]