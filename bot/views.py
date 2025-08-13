from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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
