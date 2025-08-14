import requests
import json

# URL de votre bot
url = "http://localhost:8000/webhook/"

# Données simulées de Vonage WhatsApp
test_data = {
    "text": "menu",
    "from": "+1234567890",
    "profile": {
        "name": "Test User"
    },
    "timestamp": "2024-01-01T12:00:00Z"
}

# Envoyer la requête POST
response = requests.post(url, json=test_data, headers={'Content-Type': 'application/json'})

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
