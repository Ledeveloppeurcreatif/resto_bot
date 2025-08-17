# Configuration des Variables d'Environnement

Ce guide vous explique comment configurer les variables d'environnement pour votre bot WhatsApp Twilio.

## 📋 Prérequis

- Un compte Twilio avec un numéro WhatsApp Business
- Les clés d'authentification Twilio (Account SID et Auth Token)

## 🔧 Configuration

### 1. Créer le fichier .env

Créez un fichier `.env` à la racine de votre projet avec le contenu suivant :

```env
# Variables d'environnement pour Twilio
TWILIO_ACCOUNT_SID=votre_account_sid_ici
TWILIO_AUTH_TOKEN=votre_auth_token_ici
TWILIO_WHATSAPP_NUMBER=whatsapp:+votre_numero_whatsapp

# Clé secrète Django (à changer en production)
DJANGO_SECRET_KEY=votre_cle_secrete_django

# Configuration Django
DEBUG=True
ALLOWED_HOSTS=*
```

### 2. Remplacer les valeurs

Remplacez les valeurs suivantes par vos vraies informations Twilio :

- `votre_account_sid_ici` : Votre Account SID Twilio (commence par "AC...")
- `votre_auth_token_ici` : Votre Auth Token Twilio
- `votre_numero_whatsapp` : Votre numéro WhatsApp Business (format: +1234567890)
- `votre_cle_secrete_django` : Une clé secrète pour Django (générez-en une nouvelle pour la production)

### 3. Où trouver vos clés Twilio

1. Connectez-vous à votre [Console Twilio](https://console.twilio.com/)
2. Allez dans la section "Account" → "API Keys & Tokens"
3. Copiez votre Account SID et Auth Token

### 4. Numéro WhatsApp Business

Pour obtenir un numéro WhatsApp Business :
1. Dans votre Console Twilio, allez dans "Messaging" → "Try it out" → "Send a WhatsApp message"
2. Suivez les instructions pour configurer votre numéro WhatsApp

## 🔒 Sécurité

⚠️ **IMPORTANT** : 
- Ne commettez JAMAIS le fichier `.env` dans Git
- Le fichier `.env` est déjà dans `.gitignore` pour éviter les fuites
- Changez vos clés si elles ont été exposées
- Utilisez des clés différentes pour le développement et la production

## 🚀 Test

Après avoir configuré le fichier `.env`, redémarrez votre serveur Django :

```bash
python manage.py runserver
```

Votre bot devrait maintenant fonctionner avec les variables d'environnement !

## 🆘 Dépannage

Si vous obtenez une erreur "Variables d'environnement Twilio manquantes" :

1. Vérifiez que le fichier `.env` existe à la racine du projet
2. Vérifiez que les noms des variables sont corrects (en majuscules)
3. Vérifiez qu'il n'y a pas d'espaces autour du signe `=`
4. Redémarrez votre serveur Django

## 📝 Exemple de fichier .env

```env
# Variables d'environnement pour Twilio
TWILIO_ACCOUNT_SID=AC3148c104d32bcba312db227f955357de
TWILIO_AUTH_TOKEN=d176110a320abe18eac79c59e72ea99d
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Clé secrète Django (à changer en production)
DJANGO_SECRET_KEY=django-insecure-tvdp2m4@ua2@$1+tep14+_a=!l=b@@hnk*99@t%ou&3tg*8p*4

# Configuration Django
DEBUG=True
ALLOWED_HOSTS=*
```
