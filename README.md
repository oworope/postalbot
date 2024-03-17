# Телеграм-бот для "портретов эпох"

Используется Kandinsky 3 через платформу FusionBrain

Структура:
```
handlers - обработчики команд
keyboards - простая клавиатура с кнопками
bot.py - основной файл
api.py - работа с Kandinsky
```

## Запуск

Склонируйте репозиторий, установите зависимости:
```
pip install -r requirements.txt
```

Затем создайте файл `.env`, он должен содержать в себе токены telegram, fusionbrain:
```
BOT_TOKEN = j3j1kc1O1393834m...
API_TOKEN = 00000000000000000000...
SECRET_API_TOKEN = 0000000000000000000000000000...
```

Запуск:
```
python bot.py
```
