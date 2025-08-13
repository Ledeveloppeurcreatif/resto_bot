from django.urls import path
from .views import webhook
from .views import status_webhook


urlpatterns = [
    path('webhook/', webhook),
    path('status/', status_webhook)
]