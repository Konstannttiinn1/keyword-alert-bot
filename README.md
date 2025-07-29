# Telegram Keyword Alert Bot

[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Telethon](https://img.shields.io/badge/library-telethon-orange)](https://github.com/LonamiWebs/Telethon)
[![GitHub stars](https://img.shields.io/github/stars/Konstannttiinn1/keyword-alert-bot.svg?style=social)](https://github.com/Konstannttiinn1/keyword-alert-bot/stargazers)

📌 Keyword Alert Bot

Бот для отслеживания ключевых слов в Telegram-группах и пересылки сообщений с совпадениями админам в личку. Поддерживает интерактивное управление через Telegram-интерфейс.

---



🚀 Возможности

- Мониторинг групп на наличие заданных ключевых слов

- Пересылка совпавших сообщений в личку

- Работа от имени пользователя (через session_string)

- Управление через бота: добавление/удаление слов и чатов

- Поддержка нескольких админов (через config.json)

- Удобное меню с кнопками (вложенные панели)

---

## 🚀 Быстрый запуск (через Docker)

1. Убедись, что у тебя установлен [Docker](https://docs.docker.com/get-docker/)
2. Склонируй проект и перейди в его папку:

   ```bash
   git clone https://github.com/Konstannttiinn1/keyword-alert-bot.git
   cd keyword-alert-bot
   ```

3. Создай `config.json` вручную или запусти проект один раз, он создастся сам.
4. Заполни `config.json`:
   ```json
   {
     "api_id": 123456,
     "api_hash": "your_api_hash",
     "session_string": "your_session_string",
     "user_id": 123456789,
     "keywords": ["vpn", "бот"],
     "chats": ["@examplegroup1", "@examplegroup2"]
   }
   ```

5. Запусти в контейнере:

   ```bash
   docker compose up --build -d
   ```

✅ Бот запустится в фоне и начнёт слушать чаты. Логи можно посмотреть так:

```bash
docker compose logs -f
```

---

## 📦 Локальный запуск (без Docker)

1. Установи зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запусти:
   ```bash
   python Keyword-alert.py
   ```


---

## ⚙️ Настройка

- `api_id`, `api_hash` — получи на [my.telegram.org](https://my.telegram.org)
- `session_string` — можно сгенерировать отдельно
- `keywords` — ключевые слова для фильтрации
- `chats` — username чатов для отслеживания
- `admin_ids` - id админов (можно узнать у [@userinfobot](https://t.me/userinfobot))
- `bot_token` - ''


🧪 Как получить session_string

Создай отдельный файл generate_session.py со следующим содержимым:

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 123456
api_hash = 'your_api_hash'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("session string:")
    print(client.session.save())

Запусти его и пройди авторизацию по номеру телефона

Скопируй строку сессии и вставь в config.json

📲 Telegram-команды

/start — открыть главное меню

/menu — открыть меню управления

Кнопки в меню:

🔑 Слова: добавить/удалить/посмотреть ключевые слова

💬 Чаты: добавить/удалить/посмотреть ID чатов для мониторинга
---

## 🧠 Требования

- Python 3.8+
- Библиотека [Telethon](https://github.com/LonamiWebs/Telethon)

---

## 💡 Автор

Константин | [Telegram](https://t.me/L_Konstantinn)

---

> ❤️ Буду рад звезде (⭐) на GitHub!
