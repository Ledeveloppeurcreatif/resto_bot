import os
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from vonage import Vonage, Auth
from vonage_messages import WhatsappText

# Configuration minimale (mettez vos vraies valeurs ou utilisez des variables d'environnement)
VONAGE_APPLICATION_ID = os.getenv('VONAGE_APPLICATION_ID', '9540d430-f9fd-44db-ad68-c13df17462a2')
VONAGE_PRIVATE_KEY = os.getenv('VONAGE_PRIVATE_KEY', os.path.join(settings.BASE_DIR, 'private_key.key'))
WHATSAPP_SENDER_ID = os.getenv('WHATSAPP_SENDER_ID', '14157386102')  # sans le +

def get_vonage_client() -> Vonage:
    """Create a Vonage client using a private key path or private key content.

    Prefers the path provided by VONAGE_PRIVATE_KEY when it exists on disk.
    Otherwise tries VONAGE_PRIVATE_KEY_CONTENT (PEM content).
    """
    private_key_input = VONAGE_PRIVATE_KEY
    private_key: bytes | str

    # If the env var points to an existing file, use the path directly
    if isinstance(private_key_input, str) and os.path.isfile(private_key_input):
        private_key = private_key_input
    else:
        # Fallback to PEM content from env var
        private_key_content = os.getenv('VONAGE_PRIVATE_KEY_CONTENT')
        if not private_key_content:
            raise FileNotFoundError(
                f"Clé privée introuvable. Fournissez un fichier à '{private_key_input}' ou définissez VONAGE_PRIVATE_KEY_CONTENT."
            )
        private_key = private_key_content.encode('utf-8')

    return Vonage(Auth(application_id=VONAGE_APPLICATION_ID, private_key=private_key))


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
	except Exception as e:
		print(f"Envoi échoué: {e}")

	return HttpResponse('OK', status=200)