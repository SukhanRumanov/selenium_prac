import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger("selenium")


def selenium_login(LOGIN: str, PASSWORD: str) -> bool:
    driver = None
    try:
        logger.info(f"Selenium: попытка входа для {LOGIN}")

        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)

        driver.get("https://forum.optina.ru/login/")

        login_field = wait.until(
            EC.presence_of_element_located((By.ID, "auth"))
        )
        password_field = wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        submit_button = wait.until(
            EC.element_to_be_clickable((By.ID, "elSignIn_submit"))
        )

        login_field.send_keys(LOGIN)
        password_field.send_keys(PASSWORD)
        submit_button.click()

        wait.until(
            EC.url_changes("https://forum.optina.ru/login/")
        )

        current_url = driver.current_url
        logger.info(f"URL после входа: {current_url}")

        if current_url != "https://forum.optina.ru/login/":
            logger.info("Авторизация успешна")
            return True
        else:
            try:
                error_message = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ipsMessage_error"))
                )
                logger.warning(f"Ошибка авторизации: {error_message.text}")
            except TimeoutException:
                logger.warning("Авторизация не удалась, сообщение об ошибке не найдено.")
            return False

    except TimeoutException as e:
        logger.warning(f"Таймаут при ожидании элемента: {e}")
        return False
    except Exception as e:
        logger.exception(f"Ошибка Selenium: {e}")
        return False
    finally:
        if driver:
            driver.quit()