from os import environ

BOT_TOKEN = environ.get('BOT_TOKEN', None)
ADMIN_ID = int(environ.get('ADMIN_ID', 0))
WEBHOOK_URL = environ.get('WEBHOOK_URL', None)
