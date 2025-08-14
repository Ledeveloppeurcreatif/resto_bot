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
    # Vérifier que c'est une requête POST
    if request.method != 'POST':
        return HttpResponse("Méthode non autorisée", status=405)
    
    try:
        # Récupérer les données avec une valeur par défaut
        message = request.POST.get("Body", "")
        sender_name = request.POST.get("ProfileName", "Utilisateur")
        sender_number = request.POST.get("From", "")
        
        # Vérifier que nous avons les données nécessaires
        if not sender_number:
            print("Numéro d'expéditeur manquant")
            return HttpResponse("Données manquantes", status=400)
        
        print(f"Message reçu: '{message}' de {sender_name} ({sender_number})")
        
        if message.lower() == "menu":
            Client.messages.create(
                from_=whatsapp_from,
                to=sender_number,        
                body="Bienvenue chez e-pinta restaurant {} ! voilà notre menu:\n1. Pate + baobab".format(sender_name)
            )
            print(f"Menu envoyé à {sender_number}")
        else:
            # Réponse par défaut
            Client.messages.create(
                from_=whatsapp_from,
                to=sender_number,
                body=f"Bonjour {sender_name} ! Tapez 'menu' pour voir nos plats."
            )
            print(f"Message de bienvenue envoyé à {sender_number}")
            
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
        return HttpResponse("Erreur interne", status=500)
    
    return HttpResponse("Message traité avec succès", status=200)