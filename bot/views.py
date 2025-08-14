import os
from django.http import HttpResponse
from vonage import Vonage, Auth
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Configuration Vonage pour WhatsApp
api_key = 'b86393e9'
api_secret = 'zEKWLvneh75ocpMD'
application_id = '9540d430-f9fd-44db-ad68-c13df17462a2'
private_key_path = os.path.join(settings.BASE_DIR, 'private_key.key')

# Initialisation du client Vonage avec les credentials d'application
auth = Auth(api_key, api_secret)
client = Vonage(auth)

@csrf_exempt
def bot(request):
    # Vérifier si la requête contient du JSON
    if request.method == 'POST' and request.body:
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            message = data.get('text', '')
            sender_name = data.get('profile', {}).get('name', 'Client')
            sender_number = data.get('from', '')
        except json.JSONDecodeError:
            return HttpResponse("Erreur: Données JSON invalides", status=400)
    else:
        # Si ce n'est pas une requête POST ou si le corps est vide
        return HttpResponse("Bot WhatsApp e-pinta restaurant est actif!", status=200)
    
    if message.lower() == "menu":
        # Messages API pour WhatsApp dans Vonage 4.x
        try:
            response = client.messages.send_message({
                "from": "+14157386102",  # Votre numéro WhatsApp Business
                "to": sender_number,
                "message_type": "text",
                "text": "Bienvenue chez e-pinta restaurant {} ! voilà notre menu:\n1. Pate + baobab".format(sender_name),
                "channel": "whatsapp"
            })
            print(f"Message envoyé: {response}")
        except Exception as e:
            print(f"Erreur envoi message: {e}")
    
    return HttpResponse("Bonjour! Votre message a été reçu.")