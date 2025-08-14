import os
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from vonage import Client, Messages

# Configuration Vonage
application_id = '9540d430-f9fd-44db-ad68-c13df17462a2'
private_key_path = os.path.join(settings.BASE_DIR, 'private_key.key')
whatsapp_number = '14157386102'  # Ton numéro WhatsApp Business

# Initialisation du client Vonage avec authentification JWT
vonage_client = Client(application_id=application_id, private_key=private_key_path)
messages_api = Messages(vonage_client)

@csrf_exempt
def bot(request):
    print("=== REQUÊTE REÇUE ===")
    print(f"Méthode: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Body: {request.body}")
    print("=====================")

    if request.method == 'POST' and request.body:
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(f"Données JSON reçues: {data}")

            message = data.get('text', '').lower()
            sender_name = data.get('profile', {}).get('name', 'Client')
            sender_number = data.get('from', '')

            print(f"Message: {message}")
            print(f"Expéditeur: {sender_name}")
            print(f"Numéro: {sender_number}")

            # Réponse personnalisée selon le message reçu
            if message == "menu":
                text_body = f"Bienvenue chez e-pinta restaurant {sender_name} ! Voilà notre menu:\n1. Pâte + baobab\n2. Riz sauce arachide\n3. Akoumé + viande"
            elif message in ["bonjour", "salut"]:
                text_body = f"Bonjour {sender_name} ! Bienvenue chez e-pinta restaurant. Tapez 'menu' pour voir nos plats."
            elif message in ["aide", "help"]:
                text_body = "Voici les commandes disponibles:\n- 'menu' : Voir notre carte\n- 'bonjour' : Salutation\n- 'aide' : Cette liste"
            else:
                text_body = f"Bonjour {sender_name}, je n’ai pas compris votre message. Tapez 'aide' pour voir les commandes disponibles."

            # Envoi du message via Vonage Messages API
            response = messages_api.send_message({
                "to": sender_number,
                "from": whatsapp_number,
                "channel": "whatsapp",
                "message_type": "text",
                "text": {
                    "body": text_body
                }
            })

            print(f"Message envoyé: {response}")
            return HttpResponse("Message envoyé avec succès.", status=200)

        except json.JSONDecodeError as e:
            print(f"Erreur JSON: {e}")
            return HttpResponse("Erreur: Données JSON invalides", status=400)
        except Exception as e:
            print(f"Erreur envoi message: {e}")
            return HttpResponse("Erreur lors de l'envoi du message.", status=500)

    else:
        return HttpResponse("Bot WhatsApp e-pinta restaurant est actif!", status=200)