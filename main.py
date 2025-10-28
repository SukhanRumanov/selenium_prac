from selenium import webdriver
from selenium.webdriver.common.by import By
import time

LOGIN = "roman1"
PASSWORD = "Romka1234"

driver = webdriver.Chrome()

try:
    driver.get("https://forum.optina.ru/login/")
    time.sleep(2)

    username_field = driver.find_element(By.ID, "auth")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys(LOGIN)
    password_field.send_keys(PASSWORD)

    login_button = driver.find_element(By.ID, "elSignIn_submit")
    login_button.click()

finally:
    driver.quit()