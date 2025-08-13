from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import vonage

import json
# Create your views here.


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", {}).get("content", {}).get("text", "")
        from_number = data.get("from", "")

        print(f"Message reçu de {from_number}: {message}")

        # Réponse simple
        response_text = "Bienvenue chez Le Délice ! Tapez 'menu' pour voir nos plats."
        if "menu" in message.lower():
            response_text = "🍽️ Menu du jour:\n1. Poulet braisé - 2500 FCFA\n2. Jus de bissap - 500 FCFA"

        return JsonResponse({"text": response_text})
    return JsonResponse({"status": "Webhook actif"})

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



def send_whatsapp_message(to_number, text):
    client = vonage.Client(application_id="913eb743-d029-463b-a4d3-a15451805827", private_key="b86393e9")
    whatsapp = vonage.Messages(client)

    whatsapp.send_message({
        "to": +22892596583,
        "from": "+14157386102",
        "message": {
            "content": {
                "type": "text",
                "text": text
            }
        }
    })
