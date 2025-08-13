from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import vonage

# Configuration Vonage
VONAGE_APPLICATION_ID = "9540d430-f9fd-44db-ad68-c13df17462a2"
VONAGE_FROM_NUMBER = "+14157386102"

# Clé privée en mémoire (⚠️ à ne jamais exposer en production)
VONAGE_PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCS+EbuRcXFQDQ7
AvwiDJlfw0B+OK6C+k4a7vgRTWYe21UjAa5ivWtLboRtlw7+/THQMlzwIqZgITB4
zRpXpXEb7qCICzBLg3oQBsCU3x5gdB2tQmN4Fv4k3SVyTCl+fAnHU8rQJLbYrX7O
OwIgMroiAqe3ZKrVhKN3vMnK9/RExM6wb6rU9MDmF5OmqqNA6sWUufvHe4Lj5jFM
ZoFwTT5IWdwzpyOpZAIZVRqfMkHqwlCx3xpOVkC5XYRmq7vVCR+iz4LJjwB8nsM+
LpJhweYVBiqX8FcChqaEMSkD8FhNDueldXFnkWe8IpO+hfCU3FXmLH1PBHuTqpJp
f4Z/dqD7AgMBAAECggEAIICawygYCDreMizDUM5jfuuh0Cg948ZyTn+Jyd3Jl0pf
RiohhEGqwFhVHh1ZmiephAcXSZ4IGFtOqnCFgluaq5g21U9QI2sUrAWqQmIjiCY1
x/LWJ6FCHCnyFZhlVs0cpoHP6P8tlrarw/UFz9QYGNxodeTj6Ot38UuFfwcd9LUR
o0wKsLqBcN8hJJoOG0klWJvyHRdj9IU9dCAJYOl/jFoSv/tqe1g//rLS4PyFVuNw
lnvBGdCxUkHps+lTQExdDSQy0Gp1YwjmHBjsRrwnB2czQnX+oeNtPbNqCKtJnvci
ni1ZR2CvjMir50FG1AmPjDiaO2jf/4/TgZpVg8cKzQKBgQDODQOpCHRcRd1fXrWX
VeQZhR4/eYFAnHClV1fRFoAluvzX7rAhr+j8HL4i9PuxLHIQcp6NP31u+WN9pWFm
rQ8oVYR4b3aipGiCsvyPqkl6iteRHvQRaGmNUUcywaADsNGGiR/9mGzQyziun6ER
crp3NmdFmfeX7GvyuX9IH/XQ5wKBgQC2mNjtO/YEdhvFPOxROxjjpqqxOGkuqnUU
P3+nMYFHHWCQrmARg3FfkyTu48LiUm5kuQP0z0x+FKrDk5qyY3s6KBldIMPKVNZv
prkDCCXXKPXYWbDXCr3G+9izcmndwDuMu6WJoL4cEX1DgTQf2qtd36A5HHmE1sUw
VzPcqKvozQKBgFkuPtBRLXOmdWrKphPLA/+bovzcDPo2+3ZEeGixsWMjLD4VO7xI
07ESi6S7nZgQYYoG4eLGgPagD9SY2LBE5NOTN9Ocgp9gQy+WYkOX81eLckOIPyCt
rUmRzRwFu8j9JaJyBRuQdkBkRLMnueHAYz4nmMkCG6xwkkQqzxEbbBwvAoGATdy7
k93fuGNM0Dx8YN8ca+bkHpH5eCbDqhCxtG/Nuq9yP/+7g3xTWff65ctFjRCtdlHW
uAu1iIXzk1Zbvvng0BnNRwLzulGW5yFm/z34NNmIi+sjF2/DIRi/fTWqox6Xxhk2
K4vZxUpH6gMsYPDz5iG3xuK3hse2ajilKtDaDXkCgYEAofwQjPN88Ssq1P0eMeco
QnM2w0IouxElrDP8pAlkwDr4SGbRueCRwCzKQnRrezTS6F9bwoMVgGs4HKJii+5J
3919K0ssI6eC5Mew9JXIlD4ga/1Cw3omidtw/PxXGe7dRwtqb6GkThdy0nxrFt9V
5GeeIFDKA0ADickQA0/lrh8=
-----END PRIVATE KEY-----"""

# Fonction pour envoyer un message WhatsApp
def send_whatsapp_message(to_number, text=None, interactive=None):
    client = vonage.Client(application_id=VONAGE_APPLICATION_ID, private_key=VONAGE_PRIVATE_KEY)
    whatsapp = vonage.Messages(client)

    message_payload = {
        "to": to_number,
        "from": VONAGE_FROM_NUMBER,
        "message": {}
    }

    if interactive:
        message_payload["message"]["content"] = {
            "type": "interactive",
            "interactive": interactive
        }
    else:
        message_payload["message"]["content"] = {
            "type": "text",
            "text": text
        }

    whatsapp.send_message(message_payload)

# Webhook principal
@csrf_exempt
def webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("Payload brut:", data)

        from_number = data.get("from", "")

        # Si c'est un message texte
        message_text = data.get("message", {}).get("content", {}).get("text", "")
        if message_text:
            print(f"Message reçu de {from_number}: {message_text}")

            if "menu" in message_text.lower():
                interactive_menu = {
                    "type": "button",
                    "body": {
                        "text": "🍽️ Menu du jour : Choisissez un plat"
                    },
                    "action": {
                        "buttons": [
                            {"type": "reply", "reply": {"id": "cmd_poulet", "title": "Poulet braisé"}},
                            {"type": "reply", "reply": {"id": "cmd_bissap", "title": "Jus de bissap"}}
                        ]
                    }
                }
                send_whatsapp_message(from_number, interactive=interactive_menu)
            else:
                send_whatsapp_message(from_number, text="Bienvenue chez Le Délice ! Tapez 'menu' pour voir nos plats.")

        # Si c'est une réponse à un bouton
        button_id = data.get("message", {}).get("content", {}).get("button", {}).get("reply", {}).get("id", "")
        if button_id:
            print(f"Réponse bouton reçue de {from_number}: {button_id}")
            if button_id == "cmd_poulet":
                send_whatsapp_message(from_number, text="✅ Vous avez choisi Poulet braisé. Merci !")
            elif button_id == "cmd_bissap":
                send_whatsapp_message(from_number, text="✅ Vous avez choisi Jus de bissap. Merci !")

        return JsonResponse({"status": "Message traité"})

    return JsonResponse({"status": "Webhook actif"})

# Webhook de statut (optionnel)
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