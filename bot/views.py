from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import vonage
import json

# Fonction d'envoi de message WhatsApp via Vonage
def send_whatsapp_message(to_number, text):
    client = vonage.Client(
        application_id="9540d430-f9fd-44db-ad68-c13df17462a2",
        private_key="private.key"  # Assure-toi que ce fichier est bien dans ton dossier projet
    )
    whatsapp = vonage.Messages(client)

    whatsapp.send_message({
        "to": str(to_number),  # Convertir en chaîne
        "from": "+14157386102",  # Ton numéro WhatsApp Vonage
        "message": {
            "content": {
                "type": "text",
                "text": text
            }
        }
    })

# Webhook principal pour recevoir les messages WhatsApp
@csrf_exempt
def webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", {}).get("content", {}).get("text", "")
        from_number = data.get("from", "")

        print(f"Message reçu de {from_number}: {message}")

        response_text = "Bienvenue chez Le Délice ! Tapez 'menu' pour voir nos plats."
        if "menu" in message.lower():
            response_text = (
                "🍽️ Menu du jour :\n"
                "1️⃣ Poulet braisé - 2500 FCFA\n"
                "2️⃣ Riz sauce tomate - 2000 FCFA\n"
                "3️⃣ Jus de bissap - 500 FCFA\n"
                "Répondez par le numéro du plat pour commander."
            )

        # ✅ Envoi actif via Vonage
        send_whatsapp_message(from_number, response_text)

        return JsonResponse({"status": "Message envoyé"})
    return JsonResponse({"status": "Webhook actif"})

# Webhook pour recevoir les statuts des messages
@csrf_exempt
def status_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message_id = data.get("message_uuid", "")
        status = data.get("status", "")
        to_number = data.get("to", "")

        print(f"Statut du message {message_id} vers {to_number} : {status}")

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "Webhook actif"})