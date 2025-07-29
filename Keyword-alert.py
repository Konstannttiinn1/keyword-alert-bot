# Keyword-alert.py

import json
import os
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.sync import TelegramClient as SyncTelegramClient

CONFIG_FILE = 'config.json'

# === Загрузка конфигурации ===
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
else:
    config = {
        "api_id": 123456,
        "api_hash": "your_api_hash",
        "session_name": "session",
        "session_string": "",
        "admin_ids": [123456789],
        "keywords": [],
        "chats": [],
        "bot_token": "your_bot_token"
    }
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("⚠️ Заполни config.json и перезапусти бота")
    exit()

# === Инициализация клиентов ===
session = StringSession(config['session_string']) if config.get("session_string") else config.get("session_name", "session")
user_client = TelegramClient(session, config['api_id'], config['api_hash'])
bot_client = TelegramClient("bot_session", config['api_id'], config['api_hash']).start(bot_token=config['bot_token'])

# === Помощники ===
def save_config():
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# === Обработка входящих сообщений от имени пользователя ===
@user_client.on(events.NewMessage())
async def keyword_alert_handler(event):
    if event.chat_id not in [int(c) if isinstance(c, int) or str(c).lstrip('-').isdigit() else c for c in config['chats']]:
        return
    msg_text = event.message.message.lower()
    for keyword in config['keywords']:
        if keyword.lower() in msg_text:
            sender = await event.get_sender()
            chat_id = str(event.chat_id)
            if chat_id.startswith('-100'):
                link = f"https://t.me/c/{chat_id[4:]}/{event.message.id}"
            else:
                link = "🔗 (не удалось создать ссылку)"

            alert = (
                f"🚨 <b>Обнаружено совпадение</b>\n"
                f"👤 <b>Автор:</b> {sender.first_name or 'Без имени'} (@{sender.username or 'без_юзернейма'})\n"
                f"💬 <b>Сообщение:</b> {event.message.text[:400]}\n"
                f"🔗 <a href=\"{link}\">Перейти к сообщению</a>"
            )
            for admin_id in config['admin_ids']:
                await bot_client.send_message(admin_id, alert, parse_mode='html')
            break

@bot_client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    if event.sender_id not in config['admin_ids']:
        return
    await menu_handler(event)

# === Главное меню команды /menu ===
@bot_client.on(events.NewMessage(pattern='/menu'))
async def menu_handler(event):
    if event.sender_id not in config['admin_ids']:
        return
    await event.respond(
        "📋 Главное меню:",
        buttons=[
            [Button.inline("🔑 Слова", b"menu_words")],
            [Button.inline("💬 Чаты", b"menu_chats")]
        ]
    )

# === Обработка инлайн-кнопок ===
@bot_client.on(events.CallbackQuery)
async def buttons_handler(event):
    sender = await event.get_sender()
    if sender.id not in config['admin_ids']:
        return
    data = event.data.decode('utf-8')

    if data == "back_to_main":
        await event.edit(
            "📋 Главное меню:",
            buttons=[
                [Button.inline("🔑 Слова", b"menu_words")],
                [Button.inline("💬 Чаты", b"menu_chats")]
            ]
        )

    elif data == "menu_words":
        await event.edit(
            "🔑 Работа с ключевыми словами:",
            buttons=[
                [Button.inline("➕ Добавить слово", b"add_word")],
                [Button.inline("➖ Удалить слово", b"del_word")],
                [Button.inline("📋 Показать слова", b"show_words")],
                [Button.inline("⬅️ Назад", b"back_to_main")]
            ]
        )

    elif data == "menu_chats":
        await event.edit(
            "💬 Работа с чатами:",
            buttons=[
                [Button.inline("➕ Добавить чат", b"add_chat")],
                [Button.inline("➖ Удалить чат", b"del_chat")],
                [Button.inline("📋 Показать чаты", b"show_chats")],
                [Button.inline("⬅️ Назад", b"back_to_main")]
            ]
        )

    elif data == "add_word":
        await event.respond("✍️ Введи слово для отслеживания:")
        bot_client._next_action = 'awaiting_word'

    elif data == "del_word":
        if not config['keywords']:
            await event.answer("❌ Нет слов для удаления.", alert=True)
            return
        buttons = [[Button.inline(word, f"remword:{word}")] for word in config['keywords']]
        buttons.append([Button.inline("⬅️ Назад", b"menu_words")])
        await event.edit("Выбери слово для удаления:", buttons=buttons)

    elif data == "add_chat":
        await event.respond("✍️ Введи @username или ID чата:")
        bot_client._next_action = 'awaiting_chat'

    elif data == "del_chat":
        if not config['chats']:
            await event.answer("❌ Нет чатов для удаления.", alert=True)
            return
        buttons = [[Button.inline(str(c), f"remchat:{c}")] for c in config['chats']]
        buttons.append([Button.inline("⬅️ Назад", b"menu_chats")])
        await event.edit("Выбери чат для удаления:", buttons=buttons)

    elif data == "show_words":
        text = "📋 Ключевые слова:\n" + ("\n".join(config['keywords']) or "(пусто)")
        await event.answer(text, alert=True)

    elif data == "show_chats":
        text = "📋 Чаты:\n" + ("\n".join(map(str, config['chats'])) or "(пусто)")
        await event.answer(text, alert=True)

    elif data.startswith("remword:"):
        word = data.split(":", 1)[1]
        if word in config['keywords']:
            config['keywords'].remove(word)
            save_config()
            await event.edit(f"❌ Слово '{word}' удалено.", buttons=[
                [Button.inline("⬅️ Назад", b"menu_words")]
            ])

    elif data.startswith("remchat:"):
        raw_chat = data.split(":", 1)[1].strip()
        try:
            chat_id = int(raw_chat) if raw_chat.lstrip('-').isdigit() else raw_chat
            found = next((c for c in config['chats'] if str(c) == str(chat_id)), None)
            if found is not None:
                config['chats'].remove(found)
                save_config()
                await event.edit(f"❌ Чат {chat_id} удалён.", buttons=[
                    [Button.inline("⬅️ Назад", b"menu_chats")]
                ])
            else:
                await event.answer(f"⚠️ Чат {chat_id} не найден.", alert=True)
        except Exception as e:
            await event.answer(f"❌ Ошибка: {e}", alert=True)

# === Обработка текстового ввода после кнопок ===
@bot_client.on(events.NewMessage())
async def user_input_handler(event):
    if event.sender_id not in config['admin_ids']:
        return

    if getattr(bot_client, '_next_action', None) == 'awaiting_word':
        word = event.raw_text.strip().lower()
        if word and word not in config['keywords']:
            config['keywords'].append(word)
            save_config()
            await event.respond(f"✅ Добавлено ключевое слово: {word}")
        else:
            await event.respond("⚠️ Слово уже есть или пустой ввод.")
        bot_client._next_action = None

    elif getattr(bot_client, '_next_action', None) == 'awaiting_chat':
        raw = event.raw_text.strip()
        try:
            if raw.startswith('@'):
                entity = await user_client.get_entity(raw)
                chat_id = entity.id
            else:
                chat_id = int(raw)
                if not str(chat_id).startswith('-100'):
                    chat_id = int(f"-100{chat_id}")

            if chat_id not in config['chats']:
                config['chats'].append(chat_id)
                save_config()
                await event.respond(f"✅ Добавлен чат: {chat_id}")
            else:
                await event.respond("⚠️ Чат уже в списке.")
        except Exception as e:
            await event.respond(f"❌ Ошибка при добавлении чата: {e}")

        bot_client._next_action = None

# === Запуск клиентов ===
print("🚀 Бот и мониторинг запущены. Ожидаю события...")
user_client.start()
bot_client.start()
user_client.run_until_disconnected()
bot_client.run_until_disconnected()