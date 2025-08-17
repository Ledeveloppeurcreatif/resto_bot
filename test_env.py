#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration des variables d'environnement
"""

import os
from dotenv import load_dotenv

def test_env_configuration():
    """Teste la configuration des variables d'environnement"""
    
    # Charger les variables d'environnement
    load_dotenv()
    
    print("🔍 Test de configuration des variables d'environnement")
    print("=" * 60)
    
    # Variables à vérifier
    variables = {
        'TWILIO_ACCOUNT_SID': 'Account SID Twilio',
        'TWILIO_AUTH_TOKEN': 'Auth Token Twilio', 
        'TWILIO_WHATSAPP_NUMBER': 'Numéro WhatsApp',
        'DJANGO_SECRET_KEY': 'Clé secrète Django',
        'DEBUG': 'Mode Debug',
        'ALLOWED_HOSTS': 'Hôtes autorisés'
    }
    
    all_good = True
    
    for var_name, description in variables.items():
        value = os.getenv(var_name)
        
        if value:
            # Masquer les valeurs sensibles
            if 'TOKEN' in var_name or 'SECRET' in var_name or 'AUTH' in var_name:
                display_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            else:
                display_value = value
                
            print(f"✅ {description}: {display_value}")
        else:
            print(f"❌ {description}: MANQUANT")
            all_good = False
    
    print("\n" + "=" * 60)
    
    if all_good:
        print("🎉 Toutes les variables d'environnement sont configurées !")
        print("Votre bot est prêt à fonctionner.")
    else:
        print("⚠️  Certaines variables d'environnement sont manquantes.")
        print("Veuillez créer un fichier .env avec toutes les variables requises.")
        print("Consultez le fichier README_ENV_SETUP.md pour plus d'informations.")
    
    return all_good

if __name__ == "__main__":
    test_env_configuration()
