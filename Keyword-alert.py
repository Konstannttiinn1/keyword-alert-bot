# Keyword-alert.py — Полностью обновлённый и исправленный с учётом удаления чатов и команды /start

import json
import os
import re
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession
from telethon.errors import ChatAdminRequiredError

CONFIG_FILE = 'config.json'

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
        "bot_token": "your_bot_token",
        "usernames": {}
    }
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("⚠️ Заполни config.json и перезапусти бота")
    exit()

if 'usernames' not in config:
    config['usernames'] = {}

session = StringSession(config['session_string']) if config.get("session_string") else config.get("session_name", "session")
user_client = TelegramClient(session, config['api_id'], config['api_hash'])
bot_client = TelegramClient("bot_session", config['api_id'], config['api_hash']).start(bot_token=config['bot_token'])

def save_config():
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

async def resolve_chat_id(raw):
    if raw.startswith("https://t.me/"):
        raw = raw.rstrip('/').split("/")[-1]
    if raw.startswith('@'):
        raw = raw[1:]
    # Если ввели числовой ID
    if raw.isdigit() or (raw.startswith('-100') and raw[4:].isdigit()):
        try:
            entity = await user_client.get_entity(int(raw))
        except:
            raise ValueError("Чат с таким ID не найден")
    else:
        entity = await user_client.get_entity(raw)

    chat_id = f"-100{entity.id}" if not str(entity.id).startswith("-100") else str(entity.id)
    username = getattr(entity, 'username', '')
    return chat_id, username

def get_paginated_chats(page=0, per_page=10):
    start = page * per_page
    end = start + per_page
    sliced = config['chats'][start:end]
    buttons = []
    for chat_id in sliced:
        username = config.get("usernames", {}).get(str(chat_id), "")
        label = f"{chat_id} (@{username})" if username else str(chat_id)
        buttons.append([Button.inline(label, f"remchat:{chat_id}")])
    nav_buttons = []
    if start > 0:
        nav_buttons.append(Button.inline("⬅️", f"page_chats:{page-1}"))
    if end < len(config['chats']):
        nav_buttons.append(Button.inline("➡️", f"page_chats:{page+1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    buttons.append([Button.inline("⬅️ Назад", b"menu_chats")])
    return buttons

@bot_client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    if event.sender_id in config['admin_ids']:
        await menu_handler(event)

@bot_client.on(events.NewMessage(pattern='/menu'))
async def menu_handler(event):
    if event.sender_id not in config['admin_ids']:
        return
    await event.respond(
        "📋 Главное меню:",
        buttons=[
            [Button.inline("🔑 Слова", b"menu_words")],
            [Button.inline("💬 Чаты", b"menu_chats")],
            [Button.inline("✅ Тест слежки", b"test_tracking")]
        ]
    )

@bot_client.on(events.CallbackQuery)
async def buttons_handler(event):
    sender = await event.get_sender()
    if sender.id not in config['admin_ids']:
        return
    data = event.data.decode('utf-8')

    if data == "back_to_main":
        await menu_handler(event)
        return

    if data.startswith("page_chats:"):
        page = int(data.split(":")[1])
        buttons = get_paginated_chats(page)
        await event.edit("💬 Список чатов:", buttons=buttons)
        return

    if data == "test_tracking":
        result_lines = []
        for chat_id in config['chats']:
            try:
                await user_client.get_messages(int(chat_id), limit=1)
                result_lines.append(f"✅ Работает: {chat_id}")
            except ChatAdminRequiredError:
                result_lines.append(f"⚠️ Нет прав в: {chat_id}")
            except Exception as e:
                result_lines.append(f"❌ Ошибка в: {chat_id} — {e.__class__.__name__}")
        await event.respond("🔍 Проверка слежки:\n" + "\n".join(result_lines))
        return

    if data == "menu_words":
        await event.edit("🔑 Работа с ключевыми словами:", buttons=[
            [Button.inline("➕ Добавить слово", b"add_word")],
            [Button.inline("➖ Удалить слово", b"del_word")],
            [Button.inline("📋 Показать слова", b"show_words")],
            [Button.inline("⬅️ Назад", b"back_to_main")]
        ])

    elif data == "menu_chats":
        await event.edit("💬 Работа с чатами:", buttons=[
            [Button.inline("➕ Добавить чат", b"add_chat")],
            [Button.inline("➖ Удалить чат", b"del_chat")],
            [Button.inline("📋 Показать чаты", b"show_chats")],
            [Button.inline("⬅️ Назад", b"back_to_main")]
        ])

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
        await event.respond("✍️ Введи @username или ссылку на чат:")
        bot_client._next_action = 'awaiting_chat'

    elif data == "del_chat":
        if not config['chats']:
            await event.answer("❌ Нет чатов для удаления.", alert=True)
            return
        buttons = get_paginated_chats(0)
        await event.edit("Выбери чат для удаления:", buttons=buttons)

    elif data == "show_words":
        text = "📋 Ключевые слова:\n" + ("\n".join(config['keywords']) or "(пусто)")
        await event.respond(text)

    elif data == "show_chats":
        text = "📋 Чаты:\n"
        for chat in config['chats']:
            chat_id = str(chat)
            username = config.get("usernames", {}).get(chat_id, "")
            if username:
                text += f"{chat_id} (@{username})\n"
            else:
                text += f"{chat_id}\n"
        await event.respond(text or "(пусто)")

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
        matched = [c for c in config['chats'] if str(c) == raw_chat]
        if matched:
            config['chats'] = [c for c in config['chats'] if str(c) != raw_chat]
            config['usernames'].pop(str(raw_chat), None)
            save_config()
            await event.respond(f"❌ Чат {raw_chat} удалён.")
        else:
            await event.answer(f"⚠️ Чат {raw_chat} не найден.", alert=True)

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
            chat_id, username = await resolve_chat_id(raw)
            if chat_id not in config['chats']:
                config['chats'].append(chat_id)
                config['usernames'][chat_id] = username or ""
                save_config()
                await event.respond(f"✅ Добавлен чат: {chat_id} (@{username})")
            else:
                await event.respond("⚠️ Чат уже в списке.")
        except Exception as e:
            await event.respond(f"❌ Ошибка при добавлении чата: {e}")
        bot_client._next_action = None

@user_client.on(events.NewMessage())
async def keyword_alert_handler(event):
    if str(event.chat_id) not in map(str, config['chats']):
        return
    msg_text = event.message.message.lower()
    for keyword in config['keywords']:
        if keyword.lower() in msg_text:
            try:
                sender = await event.get_sender()
            except:
                sender = None
            chat_id = str(event.chat_id)
            username = config.get("usernames", {}).get(chat_id, "")
            link = f"https://t.me/c/{chat_id[4:]}/{event.message.id}" if chat_id.startswith('-100') else "(нет ссылки)"
            chat_label = f"{chat_id} (@{username})" if username else chat_id
            sender_name = sender.first_name if sender and sender.first_name else 'Неизвестно'
            sender_username = f"@{sender.username}" if sender and sender.username else 'не_указан'

            alert = (
                f"🚨 <b>Обнаружено совпадение</b> в чате <b>{chat_label}</b>\n"
                f"👤 <b>Автор:</b> {sender_name} ({sender_username})\n"
                f"💬 <b>Сообщение:</b> {event.message.text[:400]}\n"
                f"🔗 <a href=\"{link}\">Перейти к сообщению</a>"
            )
            for admin_id in config['admin_ids']:
                await bot_client.send_message(admin_id, alert, parse_mode='html')
            break

print("🚀 Бот и мониторинг запущены. Ожидаю события...")
user_client.start()
bot_client.start()
user_client.run_until_disconnected()
bot_client.run_until_disconnected()
