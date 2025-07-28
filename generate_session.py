from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 
api_hash = ''

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("👉 Введите номер телефона и пройдите авторизацию...")
    session_str = client.session.save()
    print("\n✅ Готово! Вот session_string:")
    print(session_str)
    print("\n📌 Вставь это значение в config.json вместо \"session_string\": \"\"")
