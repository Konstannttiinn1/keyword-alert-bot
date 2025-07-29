from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import getpass

api_id = int(input("Введите api_id: "))
api_hash = input("Введите api_hash: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("👉 Введите номер телефона:")
    client.sign_in()

    if not client.is_user_authorized():
        code = input("👉 Введите код из Telegram: ")
        try:
            client.sign_in(code=code)
        except Exception as e:
            print("⚠️ Требуется двухфакторная авторизация")
            password = getpass.getpass("🔒 Введите пароль: ")
            client.sign_in(password=password)

    print("✅ Успешно! Вот session_string:")
    print(client.session.save())
