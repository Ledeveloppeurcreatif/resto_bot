import os
from django.http import HttpResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Create your views here.
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+254115123456')
Client = Client(account_sid, auth_token)

@csrf_exempt
def bot(request):
    message = request.POST["Body"]
    sender_name = request.POST["ProfileName"]
    sender_number = request.POST["From"]
    if message == "Menu":
        Client.messages.create(
            from_=whatsapp_from,
            to=sender_number,        
            body="Bienvenue chez e-pinta restaurant {} ! voilà notre menu:\n1. Pate + baoab".format(sender_name)
        )
    return HttpResponse("Bonjour!  Votre message a été reçu.")