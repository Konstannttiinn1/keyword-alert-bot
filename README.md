# Telegram Keyword Alert Bot

[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Telethon](https://img.shields.io/badge/library-telethon-orange)](https://github.com/LonamiWebs/Telethon)
[![GitHub stars](https://img.shields.io/github/stars/Konstannttiinn1/keyword-alert-bot.svg?style=social)](https://github.com/Konstannttiinn1/keyword-alert-bot/stargazers)

> Telegram-бот, который отслеживает сообщения в выбранных группах и пересылает тебе только те, что содержат нужные ключевые слова.

---

## 🔧 Возможности

- Добавление чатов для отслеживания по `@username`
- Добавление ключевых слов прямо через Telegram
- Уведомления со ссылкой на сообщение
- Поддержка нескольких чатов и ключевых слов
- Полностью автономен, можно развернуть на своём сервере или в Docker

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

## 📬 Команды бота

Пиши команды боту в ЛС:

- `/addword vpn` — добавить ключевое слово `vpn`
- `/addchat @chatname` — добавить чат для отслеживания

---

## ⚙️ Настройка

- `api_id`, `api_hash` — получи на [my.telegram.org](https://my.telegram.org)
- `session_string` — можно сгенерировать отдельно
- `user_id` — свой Telegram ID (можно узнать у [@userinfobot](https://t.me/userinfobot))
- `keywords` — ключевые слова для фильтрации
- `chats` — username чатов для отслеживания

---

## 🧠 Требования

- Python 3.8+
- Библиотека [Telethon](https://github.com/LonamiWebs/Telethon)

---

## 💡 Автор

Константин | [Telegram](https://t.me/L_Konstantinn)

---

> ❤️ Буду рад звезде (⭐) на GitHub!
