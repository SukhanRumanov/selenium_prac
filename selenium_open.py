import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger("selenium")

def selenium_login(LOGIN: str, PASSWORD: str) -> bool:
    driver = None
    try:
        logger.info(f"Selenium: попытка входа для {LOGIN}")

        chrome_options = Options()

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://forum.optina.ru/login/")
        time.sleep(2)

        driver.find_element(By.ID, "auth").send_keys(LOGIN)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.ID, "elSignIn_submit").click()
        time.sleep(3)

        current_url = driver.current_url
        logger.info(f"URL после входа: {current_url}")

        if current_url != "https://forum.optina.ru/login/":
            logger.info("Авторизация успешна")
            return True
        else:
            try:
                err_text = driver.find_element(By.CLASS_NAME, "ipsMessage_error").text
                logger.warning(f"Ошибка авторизации: {err_text}")
            except NoSuchElementException:
                logger.warning("Авторизация не удалась, сообщение об ошибке не найдено.")
            return False

    except Exception as e:
        logger.exception(f"Ошибка Selenium: {e}")
        return False

    finally:
        if driver:
            driver.quit()
