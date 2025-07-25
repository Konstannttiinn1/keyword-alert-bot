from telethon import TelegramClient, events
from telethon.sessions import StringSession
import json
import os
import asyncio

# === Конфигурация ===
CONFIG_FILE = 'config.json'

# Загружаем конфиг
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    config = {
        "api_id": 123456,
        "api_hash": "your_api_hash",
        "session_string": "",
        "user_id": 123456789,
        "keywords": ["vpn", "бот"],
        "chats": []
    }
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("⚠️ Заполни config.json и перезапусти бота")
    exit()

# === Инициализация клиента ===
if config.get("session_string"):
    session = StringSession(config['session_string'])
else:
    session = config.get("session_name", "session")

client = TelegramClient(session, config['api_id'], config['api_hash'])

# === Разрешение чатов по username и chat_id ===
async def resolve_chats():
    resolved = []
    for chat in config['chats']:
        try:
            entity = await client.get_entity(chat)
            resolved.append(entity)
            print(f"✅ Добавлен чат: {chat} -> ID: {entity.id}")
        except Exception as e:
            print(f"❌ Не удалось подключиться к чату {chat}: {e}")
    return resolved

# === Основной запуск ===
async def main():
    resolved_chats = await resolve_chats()
    resolved_ids = [int(e.id) for e in resolved_chats]

    if not resolved_ids:
        print("⚠️ Ни один чат не был добавлен. Проверь config['chats'] и доступность username!")

    print(f"🟢 Отслеживаемые чаты (ID): {resolved_ids}")

    @client.on(events.NewMessage(chats=resolved_ids))
    async def handler(event):
        print(f"📨 Сообщение в отслеживаемом чате {event.chat_id}: {event.message.message}")

        msg_text = event.message.message.lower()
        for keyword in config['keywords']:
            if keyword.lower() in msg_text:
                sender = await event.get_sender()
                chat_id = str(event.chat_id)

                if chat_id.startswith("-100"):
                    link = f"https://t.me/c/{chat_id[4:]}/{event.message.id}"
                else:
                    link = "🔗 (ссылка недоступна)"

                alert_text = (
                    f"🚨 <b>Обнаружено совпадение</b>\n"
                    f"👤 <b>Автор:</b> {sender.first_name or 'Без имени'} (@{sender.username or 'без_юзернейма'})\n"
                    f"💬 <b>Сообщение:</b> {event.message.text[:400]}\n"
                    f"🔗 <a href=\"{link}\">Перейти к сообщению</a>"
                )

                await client.send_message(config['user_id'], alert_text, parse_mode='html')
                break

    # Команды
    @client.on(events.NewMessage(from_users=config['user_id'], pattern='/addword (.+)'))
    async def add_keyword(event):
        word = event.pattern_match.group(1).strip().lower()
        if word not in config['keywords']:
            config['keywords'].append(word)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            await event.respond(f"✅ Ключевое слово '{word}' добавлено.")
        else:
            await event.respond(f"⚠️ Слово '{word}' уже есть в списке.")

    @client.on(events.NewMessage(from_users=config['user_id'], pattern=r'/addchat (.+)'))
    async def add_chat(event):
        chat_id = event.pattern_match.group(1).strip()
        if chat_id not in config['chats']:
            config['chats'].append(chat_id)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            await event.respond(f"✅ Чат {chat_id} добавлен для отслеживания.")
        else:
            await event.respond(f"⚠️ Чат {chat_id} уже отслеживается.")

    print("🚀 Бот запущен. Ожидаю сообщения...")
    await client.run_until_disconnected()

# === Запуск клиента ===
with client:
    client.loop.run_until_complete(main())