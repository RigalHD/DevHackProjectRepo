# DevHackProject: кейс ЮФУ

## Установка проекта

### 1. Установка зависимостей: 

```cmd
pip install -e .
pip install -e .[lint]
```

### 2. Установка СУБД PostgreSQL:

Вам потребуется установить данную СУБД и создать в ней базу данных
**https://www.postgresql.org/**

### 3. Создание .env файла:

Для корректной работы проекта вам потребуется создать в корневой папке проекта файл .env по следующему шаблону:
```env
BOT_TOKEN=<Токен Telegram бота>
VK_TOKEN=<Toкен мини-приложения VK>
LLM_TOKEN=<Токен LLM Yandex GPT>

VK_OWNER_ID=<ID Вашего профиля VK (будет использоваться для парсинга)>
VK_GROUP_ID=<ID Группы VK, парсинг которой будет произведен>
VK_GROUP_DOMAIN=<Domain VK группы>

DATABASE_HOST=<Хост базы данных (обычно localhost)>
DATABASE_PORT=<Порт базы данных (обычно 5432)>
DATABASE_NAME=<Название, которые вы дали базе данных>
DATABASE_PASSWORD=<Пароль от базы данных>
DATABASE_USER=<Имя пользователя базы данных>
```

## Запуск проекта

### Для запуска введите в консоль:

```cmd
python -m telegram_assistant.bot
```