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
    print(f"=== REQUÊTE REÇUE ===")
    print(f"Méthode: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Body: {request.body}")
    print(f"=====================")
   
    # Vérifier si la requête contient du JSON
    if request.method == 'POST' and request.body:
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(f"Données JSON reçues: {data}")
           
            message = data.get('text', '')
            sender_name = data.get('profile', {}).get('name', 'Client')
            sender_number = data.get('from', '')
           
            print(f"Message: {message}")
            print(f"Expéditeur: {sender_name}")
            print(f"Numéro: {sender_number}")
           
        except json.JSONDecodeError as e:
            print(f"Erreur JSON: {e}")
            return HttpResponse("Erreur: Données JSON invalides", status=400)
    else:
        # Si ce n'est pas une requête POST ou si le corps est vide
        print("Requête GET ou corps vide - affichage de la page d'accueil")
        return HttpResponse("Bot WhatsApp e-pinta restaurant est actif!", status=200)
   
    if message.lower() == "menu":
        # Essayer plusieurs formats jusqu'à ce que l'un fonctionne
        message_text = "Bienvenue chez e-pinta restaurant {} ! voilà notre menu:\n1. Pate + baobab".format(sender_name)
        
        # Format 1: Structure custom (recommandé par certaines docs)
        try:
            response = client.messages.send({
                "from": "14157386102",
                "to": sender_number,
                "channel": "whatsapp",
                "message_type": "custom",
                "custom": {
                    "type": "text",
                    "text": {
                        "body": message_text
                    }
                }
            })
            print(f"Message envoyé avec format custom: {response}")
        except Exception as e:
            print(f"Erreur format custom: {e}")
            
            # Format 2: Structure text simple
            try:
                response = client.messages.send({
                    "from": "14157386102",
                    "to": sender_number,
                    "channel": "whatsapp",
                    "message_type": "text",
                    "text": {
                        "body": message_text
                    }
                })
                print(f"Message envoyé avec format text/body: {response}")
            except Exception as e:
                print(f"Erreur format text/body: {e}")
                
                # Format 3: Structure directe (dernière tentative)
                try:
                    response = client.messages.send({
                        "from": "14157386102",
                        "to": sender_number,
                        "channel": "whatsapp",
                        "text": message_text
                    })
                    print(f"Message envoyé avec format direct: {response}")
                except Exception as e:
                    print(f"Erreur format direct: {e}")
                    print("Tous les formats ont échoué!")
   
    elif message.lower() == "bonjour" or message.lower() == "salut":
        try:
            response = client.messages.send({
                "from": "14157386102",
                "to": sender_number,
                "channel": "whatsapp",
                "message_type": "custom",
                "custom": {
                    "type": "text",
                    "text": {
                        "body": "Bonjour {} ! Bienvenue chez e-pinta restaurant. Tapez 'menu' pour voir nos plats.".format(sender_name)
                    }
                }
            })
            print(f"Message envoyé: {response}")
        except Exception as e:
            print(f"Erreur envoi message: {e}")
   
    elif message.lower() == "aide" or message.lower() == "help":
        try:
            response = client.messages.send({
                "from": "14157386102",
                "to": sender_number,
                "channel": "whatsapp",
                "message_type": "custom",
                "custom": {
                    "type": "text",
                    "text": {
                        "body": "Voici les commandes disponibles:\n- 'menu' : Voir notre carte\n- 'bonjour' : Salutation\n- 'aide' : Cette liste"
                    }
                }
            })
            print(f"Message envoyé: {response}")
        except Exception as e:
            print(f"Erreur envoi message: {e}")
   
    return HttpResponse("Bonjour! Votre message a été reçu.")