from django.urls import path
from .views import bot


urlpatterns = [
    path('webhook/', bot),
    #path('status/', status_webhook)
]