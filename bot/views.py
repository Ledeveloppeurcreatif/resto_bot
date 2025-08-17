
import os
from twilio.rest import Client
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Récupération des variables d'environnement Twilio
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Vérification que les variables d'environnement sont définies
if not account_sid or not auth_token or not whatsapp_number:
    raise ValueError(
        "Variables d'environnement Twilio manquantes. "
        "Veuillez définir TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN et TWILIO_WHATSAPP_NUMBER dans votre fichier .env"
    )

client = Client(account_sid, auth_token)

# Etat utilisateur en mémoire (clé: numéro WhatsApp "From")
USER_STATE = {}

MAIN_MENU_TEXT = (
    "Bonjour, bienvenue au restaurant e-pinta 🍽️ ! Que puis-je faire pour vous aujourd’hui ?\n"
    "1️⃣ Voir le Menu\n"
    "2️⃣ Passer une commande\n"
    "3️⃣ Voir nos horaires\n"
    "4️⃣ Voir nos promotions"
)

MENU_TEXT = (
    "Voici nos plats disponibles :\n"
    "1. Riz + sauce d'arachide + viande de mouton\n"
    "2. Riz + sauce d'arachide + poisson\n"
    "3. Riz + sauce d'arachide + viande de pintade\n"
    "4. Foufou + sauce d'arachide + viande de mouton"
)

ORDER_MENU_PROMPT = (
    MENU_TEXT + "\n\nVeuillez choisir un plat (1, 2, 3 ou 4).\n(Envoyez 'M' pour le menu, 'A' pour annuler)"
)

HOURS_TEXT = "🕒 Nous sommes ouverts tous les jours de 8h à 22h."

PROMOTIONS = []  # Renseigner ici s'il y a des promotions actives

def send_message(to, body):
    client.messages.create(
        from_=whatsapp_number,
        body=body,
        to=to
    )

@csrf_exempt
def bot(request):
    message = (request.POST.get("Body") or "").strip()
    sender_number = request.POST.get("From")

    if not sender_number:
        return HttpResponse("OK")

    state = USER_STATE.get(sender_number)
    if not state:
        state = {"stage": "MAIN_MENU", "selected_item": None}
        USER_STATE[sender_number] = state

    stage = state.get("stage")
    normalized = message.lower()

    # Raccourcis globaux disponibles à tout moment
    if normalized in {"m", "menu"}:
        send_message(sender_number, MAIN_MENU_TEXT)
        state["stage"] = "AWAIT_MAIN_CHOICE"
        return HttpResponse("OK")

    if normalized in {"1", "2", "3", "4"}:
        if normalized == "1":
            send_message(sender_number, MENU_TEXT)
            return HttpResponse("OK")
        if normalized == "2":
            send_message(sender_number, ORDER_MENU_PROMPT)
            state["stage"] = "ORDER_SELECT"
            return HttpResponse("OK")
        if normalized == "3":
            send_message(sender_number, HOURS_TEXT)
            return HttpResponse("OK")
        if normalized == "4":
            if PROMOTIONS:
                promos = "\n".join(f"- {p}" for p in PROMOTIONS)
                send_message(sender_number, promos)
            else:
                send_message(sender_number, "🎉 Aucune promotion disponible pour le moment.")
            return HttpResponse("OK")

    if normalized in {"a", "annuler"}:
        state["selected_item"] = None
        send_message(sender_number, "Commande annulée.\n\n" + MAIN_MENU_TEXT)
        state["stage"] = "AWAIT_MAIN_CHOICE"
        return HttpResponse("OK")

    if normalized in {"r", "retour"}:
        send_message(sender_number, MAIN_MENU_TEXT)
        state["stage"] = "AWAIT_MAIN_CHOICE"
        return HttpResponse("OK")

    # 1) Première interaction ou retour au menu principal
    if stage == "MAIN_MENU":
        send_message(sender_number, MAIN_MENU_TEXT)
        state["stage"] = "AWAIT_MAIN_CHOICE"
        return HttpResponse("OK")

    # 2) Choix principal
    if stage == "AWAIT_MAIN_CHOICE":
        if normalized == "1":
            send_message(sender_number, MENU_TEXT)
            return HttpResponse("OK")
        if normalized == "2":
            send_message(sender_number, ORDER_MENU_PROMPT)
            state["stage"] = "ORDER_SELECT"
            return HttpResponse("OK")
        if normalized == "3":
            send_message(sender_number, HOURS_TEXT)
            return HttpResponse("OK")
        if normalized == "4":
            if PROMOTIONS:
                promos = "\n".join(f"- {p}" for p in PROMOTIONS)
                send_message(sender_number, promos)
            else:
                send_message(sender_number, "🎉 Aucune promotion disponible pour le moment.")
            return HttpResponse("OK")

        # Entrée invalide sur le menu principal
        send_message(sender_number, "Veuillez choisir un nombre parmi la liste ci-dessous\n\n" + MAIN_MENU_TEXT)
        return HttpResponse("OK")

    # 3) Sélection du plat (commande)
    if stage == "ORDER_SELECT":
        items = {
            "1": "Riz + sauce d'arachide + viande de mouton",
            "2": "Riz + sauce d'arachide + poisson",
            "3": "Riz + sauce d'arachide + viande de pintade",
            "4": "Foufou + sauce d'arachide + viande de mouton",
        }
        if normalized in items:
            state["selected_item"] = items[normalized]
            send_message(
                sender_number,
                f"Vous avez choisi: {state['selected_item']}.\nConfirmez-vous la commande ? (oui/non)\n(Envoyez 'M' pour le menu, 'A' pour annuler)"
            )
            state["stage"] = "ORDER_CONFIRM"
            return HttpResponse("OK")

        send_message(sender_number, "Veuillez choisir un nombre parmi la liste ci-dessous\n\n" + ORDER_MENU_PROMPT)
        return HttpResponse("OK")

    # 4) Confirmation de la commande
    if stage == "ORDER_CONFIRM":
        if normalized == "oui":
            send_message(sender_number, "Veuillez envoyer votre localisation ou votre adresse.\n(Envoyez 'M' pour le menu, 'A' pour annuler)")
            state["stage"] = "ORDER_LOCATION"
            return HttpResponse("OK")
        if normalized == "non":
            state["selected_item"] = None
            send_message(sender_number, "Commande annulée.\n\n" + MAIN_MENU_TEXT)
            state["stage"] = "AWAIT_MAIN_CHOICE"
            return HttpResponse("OK")

        send_message(sender_number, "Veuillez répondre par 'oui' ou 'non'.")
        return HttpResponse("OK")

    # 5) Réception de la localisation / adresse
    if stage == "ORDER_LOCATION":
        location_text = message or "Localisation non précisée"
        selected = state.get("selected_item")
        print({
            "event": "NEW_ORDER",
            "from": sender_number,
            "item": selected,
            "location": location_text,
        })
        state["selected_item"] = None
        state["stage"] = "AWAIT_MAIN_CHOICE"
        send_message(sender_number, "Votre commande a été envoyée au gérant. Merci !")
        return HttpResponse("OK")

    # Par défaut, renvoyer le menu principal
    send_message(sender_number, MAIN_MENU_TEXT)
    state["stage"] = "AWAIT_MAIN_CHOICE"
    return HttpResponse("OK")
