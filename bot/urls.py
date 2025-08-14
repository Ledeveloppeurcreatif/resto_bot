from django.urls import path
from .views import bot, health_check


urlpatterns = [
    path('', health_check),
    path('webhook/', bot),
    #path('status/', status_webhook)
]