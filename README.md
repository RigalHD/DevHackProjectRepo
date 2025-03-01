# DevHackProject: кейс ЮФУ

## Установка проекта

### 1. Установка зависимостей: 

```cmd
pip install -e .
pip install -e .[lint]
```

### 2. Создание .env файла:

Для корректной работы проекта вам потребуется создать в корневой папке проекта файл .env по следующему шаблону:
```env
BOT_TOKEN=<Токен Telegram бота>
VK_TOKEN=<Toкен мини-приложения VK>
LLM_TOKEN=<Токен LLM Yandex GPT>
LLM_FOLDER_ID=<Folder ID LLM Yandex GPT>

VK_OWNER_ID=<ID Вашего профиля VK (будет использоваться для парсинга)>
VK_GROUP_ID=<ID Группы VK, парсинг которой будет произведен>
VK_GROUP_DOMAIN=<Domain VK группы>
```

## Запуск проекта

### Для запуска введите в консоль:

```cmd
python -m telegram_assistant.bot
```