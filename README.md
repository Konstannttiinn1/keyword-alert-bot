# Telegram Keyword Alert Bot

[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Telethon](https://img.shields.io/badge/library-telethon-orange)](https://github.com/LonamiWebs/Telethon)
[![GitHub stars](https://img.shields.io/github/stars/Konstannttiinn1/keyword-alert-bot.svg?style=social)](https://github.com/Konstannttiinn1/keyword-alert-bot/stargazers)

---

<details>
<summary><strong>🇷🇺 Читать на русском</strong></summary>

### 📌 Бот для отслеживания ключевых слов

Бот для отслеживания ключевых слов в Telegram-группах и пересылки сообщений с совпадениями админам в личку. Поддерживает интерактивное управление через Telegram-интерфейс.

#### 🚀 Возможности

- 📥 Отслеживание ключевых слов в указанных чатах
- 🧠 Поддержка добавления чатов по ссылке, юзернейму или ID
- ⚙️ Управление через Telegram-интерфейс (кнопки и команды)
- 📋 Меню управления словами и чатами
- 🔄 Тест активности слежки по чатам
- 📡 Поддержка нескольких администраторов
- 📎 Уведомления содержат ссылку на сообщение, юзернейм автора и ID чата
- 🧼 Удаление чатов и слов с подтверждением

#### 🚀 Быстрый запуск (Docker)

```bash
git clone https://github.com/Konstannttiinn1/keyword-alert-bot.git
cd keyword-alert-bot
docker compose up --build -d
```

#### 📦 Конфигурация

Создай или отредактируй `config.json`:
```json
{
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
```

#### 📲 Команды Telegram

- `/start` — главное меню  
- `/menu` — меню управления  
- 🔑 Ключевые слова  
- 💬 Мониторинг чатов

#### 💡 Автор: [Константин](https://t.me/L_Konstantinn)

</details>

---

<details open>
<summary><strong>🇬🇧 Read in English</strong></summary>

### 📌 Keyword Alert Bot

A Telegram bot that monitors messages in selected groups for specific keywords and forwards matching messages to admins via private messages. Features a full interactive Telegram-based management interface.

#### 🚀 Features

- 📥 Keyword tracking in selected chats
- 🧠 Add chats by link, username, or ID
- ⚙️ Telegram interface management (buttons + commands)
- 📋 Keyword and chat management menus
- 🔄 Monitoring test for selected chats
- 📡 Multi-admin support
- 📎 Notifications include message link, author username, and chat ID
- 🧼 Safe deletion of words and chats with confirmation

#### 🐳 Quick Start (Docker)

```bash
git clone https://github.com/Konstannttiinn1/keyword-alert-bot.git
cd keyword-alert-bot
docker compose up --build -d
```

#### 📦 Configuration

Create or edit `config.json`:

```json
{
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
```

#### 📲 Telegram Commands

- `/start` — open main menu  
- `/menu` — open management menu  
- 🔑 Keywords  
- 💬 Chat monitoring

#### 💡 Author: [Konstantin](https://t.me/L_Konstantinn)

</details>