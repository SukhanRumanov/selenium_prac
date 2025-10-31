import asyncio
import logging
from telethon import TelegramClient
from tg import setup_handlers
from params import API_ID, API_HASH, BOT_TOKEN


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )
    logging.getLogger("telethon").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


async def main():
    configure_logging()
    logger = logging.getLogger("main")
    logger.info("Запускаем бота")

    client = TelegramClient('bot_session', API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    await setup_handlers(client)

    logger.info("бот запущен")
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Программа остановлена')
    except Exception as e:
        logging.error(f'Ошибка при запуске: {e}')
