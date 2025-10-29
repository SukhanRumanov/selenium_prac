from telethon import events
import asyncio
import logging
from selenium_open import selenium_login

logger = logging.getLogger("tg")

user_states = {}


async def setup_handlers(client):
    @client.on(events.NewMessage)
    async def handler(event):
        user_id = event.sender_id
        text = (event.raw_text or "").strip()
        logger.info(f"Получено сообщение от {user_id}: {text}")

        if text.lower() in ["/start", "/cancel"]:
            user_states[user_id] = {"step": "login_waiting"}
            await event.reply("Отправь мне свой логин:")
            return

        state = user_states.get(user_id)
        if not state:
            user_states[user_id] = {"step": "login_waiting"}
            await event.reply("Введите ваш логин:")
            return

        step = state["step"]

        if step == "login_waiting":
            state["login"] = text
            state["step"] = "password_waiting"
            await event.reply("Теперь введите пароль:")
            return

        if step == "password_waiting":
            login = state["login"]
            password = text
            user_states[user_id] = {"step": "login_waiting"}

            await event.reply("Пытаюсь войти на сайт, подождите...")
            logger.info(f"Начинаем авторизацию для пользователя {login}")

            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(None, selenium_login, login, password)

            if success:
                await event.reply("Вход выполнен успешно")
                logger.info(f"Авторизация {login} успешна.")
            else:
                await event.reply("Не удалось войти. Проверьте логин и пароль.\nПопробуйте снова — отправьте логин:")
                logger.warning(f"Авторизация {login} не удалась.")