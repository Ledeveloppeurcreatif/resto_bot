import os
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from vonage import Vonage, Auth
from vonage_messages import WhatsappText

# Configuration minimale (mettez vos vraies valeurs ou utilisez des variables d'environnement)
VONAGE_APPLICATION_ID = os.getenv('VONAGE_APPLICATION_ID', '9540d430-f9fd-44db-ad68-c13df17462a2')
WHATSAPP_SENDER_ID = os.getenv('WHATSAPP_SENDER_ID', '14157386102')  # sans le +

# Clé privée Vonage (pour test - en production, utilisez des variables d'environnement)
VONAGE_PRIVATE_KEY_CONTENT = """-----BEGIN PRIVATE KEY-----
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

def get_vonage_client() -> Vonage:
    """Create a Vonage client using a private key content."""
    try:
        # Utilise la clé privée directement depuis le code (pour test)
        private_key = VONAGE_PRIVATE_KEY_CONTENT.encode('utf-8')
        print("Utilisation de la clé privée depuis le code")
        
        return Vonage(Auth(application_id=VONAGE_APPLICATION_ID, private_key=private_key))
    except Exception as e:
        error_msg = f"Erreur lors de la création du client Vonage: {e}"
        print(error_msg)
        raise Exception(error_msg)


def health_check(request):
    """Simple health check endpoint for the root URL."""
    return HttpResponse('OK', status=200)


@csrf_exempt
def bot(request):
	# Healthcheck simple
	if request.method != 'POST' or not request.body:
		return HttpResponse('OK', status=200)

	# Parse du JSON entrant (webhook Vonage)
	try:
		data = json.loads(request.body.decode('utf-8'))
	except json.JSONDecodeError:
		return HttpResponse('Bad Request', status=400)

	incoming_text = (data.get('text') or '').strip().lower()
	to_number = data.get('from')
	if not to_number:
		return HttpResponse('OK', status=200)

	reply_text = "Bienvenue chez e-pinta ! Tapez 'menu' pour voir nos plats."
	if incoming_text == 'menu':
		reply_text = "Bienvenue chez e-pinta !\nMenu:\n1. Pate + baobab"

	# Envoi de la réponse WhatsApp
	try:
		client = get_vonage_client()
		msg = WhatsappText(to=to_number, from_=WHATSAPP_SENDER_ID, text=reply_text)
		client.messages.send(msg)
		print(f"Message WhatsApp envoyé avec succès à {to_number}")
	except Exception as e:
		print(f"Erreur lors de l'envoi du message WhatsApp: {e}")
		# On continue même en cas d'erreur pour ne pas casser le webhook

	return HttpResponse('OK', status=200)