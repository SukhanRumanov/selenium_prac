from telethon import events
import asyncio
import logging
from selenium_open import selenium_login

logger = logging.getLogger("tg")

user_states = {}

async def handle_login_input(event, state, text):
    state["login"] = text
    state["step"] = "password_waiting"
    await event.reply("Теперь введите пароль:")
    logger.info(f"Пользователь {event.sender_id} ввел логин")

async def handle_password_input(event, state, text):
    user_id = event.sender_id
    login = state["login"]
    password = text

    user_states[user_id] = {"step": "login_waiting"}

    await event.reply("Пытаюсь войти на сайт, подождите...")
    logger.info(f"Начинаем авторизацию для пользователя {login}")

    try:
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(None, selenium_login, login, password)

        if success:
            await event.reply("Вход выполнен успешно")
            logger.info(f"Авторизация {login} успешна.")
        else:
            await event.reply("Не удалось войти. Проверьте логин и пароль.\nПопробуйте снова — отправьте логин:")
            logger.warning(f"Авторизация {login} не удалась.")

    except Exception as e:
        await event.reply("Произошла ошибка при авторизации. Попробуйте снова — отправьте логин:")
        logger.error(f"Ошибка при авторизации {login}: {e}")

async def setup_handlers(client):
    @client.on(events.NewMessage(pattern="/start"))
    async def start_handler(event):
        user_id = event.sender_id
        user_states[user_id] = {"step": "login_waiting"}
        await event.reply("Отправь мне свой логин:")
        logger.info(f"Пользователь {user_id} начал диалог")

    @client.on(events.NewMessage)
    async def message_handler(event):
        user_id = event.sender_id
        text = (event.raw_text or "").strip()

        if text.lower() == '/start':
            return

        logger.info(f"Получено сообщение от {user_id}: {text}")

        state = user_states.get(user_id)

        if not state:
            user_states[user_id] = {"step": "login_waiting"}
            await event.reply("Введите ваш логин:")
            return

        step = state["step"]

        if step == "login_waiting":
            await handle_login_input(event, state, text)
        elif step == "password_waiting":
            await handle_password_input(event, state, text)