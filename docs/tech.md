# Техническая документация Telegram-бота "Vibe Tracker"

## 1. Технический стек

- **Язык:** Python 3.11+
- **Telegram Framework:** `aiogram` 3.x (современный, асинхронный, на базе `Router`).
- **ORM (Работа с БД):** `Tortoise ORM` (асинхронная, интуитивно понятная).
- **База данных:** `SQLite` (файловая, не требует установки сервера, подходит для MVP).
- **Конфигурация:** `pydantic-settings` или чтение `.env` файла.

## 2. Модель данных (Схема БД)

### Таблица `User`
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | UUID / AutoField | Primary Key |
| `telegram_id` | BigInt | Уникальный ID пользователя Telegram |
| `username` | String | Никнейм пользователя |
| `created_at` | Datetime | Дата регистрации |

### Таблица `MoodLog`
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | UUID / AutoField | Primary Key |
| `user` | ForeignKey | Ссылка на таблицу `User` |
| `value` | Int | Оценка состояния (1-10) |
| `note` | Text | Текстовый комментарий (опционально) |
| `created_at` | Datetime | Дата создания записи |

## 3. Структура проекта

Проект организован для удобной навигации (Context-First Architecture):

```text
vibe-bot/
├── .env                # Токены и секреты
├── requirements.txt
├── src/
│   └── vibe_tracker_bot/
│       ├── main.py             # Точка входа
│       ├── database/
│       │   ├── models.py       # Описание таблиц
│       │   └── core.py         # Инициализация БД
│       ├── handlers/
│       │   ├── common.py       # Роутер базовых команд
│       │   └── tracking.py     # Роутер трекинга
│       └── services/           # Бизнес-логика
```
