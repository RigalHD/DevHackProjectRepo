# DevHackProject: кейс ЮФУ

## Проект нацелен на помощь студентам, поступающим в ЮФУ🏫

Он выполнен в формате чат-бота в Telegram📨. Для ответов на вопросы
используется ИИ YandexGPT, который, получив актуальные данные,
дает общую информацию о различных аспектах поступления.👨‍🎓

Главное преимущество - бот всегда выдает актуальную информацию⚡ и
ничего не выдумывает💡, так как все данные автоматически парсятся с сайта ЮФУ
и их группы в ВК.


### 🧑‍💻Технологии📕:
- aiogram3: именно на ее основе создана чат-бот часть проекта,
- python-dotenv: позволяет удобно работать с .env файлами,
- requests и beautifulsoup4: благодаря им у чат-бота всегда есть актуальная информация,
- YandexGPT: Данная нейросеть выполняет ИИ-функции в проекте,
- ruff: отлично форматируе ваши проекты и помогает следить за его оформлением.

## Установка проекта

### 1. Установка зависимостей⬇️: 

```cmd
pip install -e .
pip install -e .[lint]
```

### 2. Создание .env файла🔐:

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

## Запуск проекта🌟

### Для запуска введите в консоль:

```cmd
python -m telegram_assistant.bot
```
