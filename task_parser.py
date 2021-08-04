import os.path
import time
import json
import selenium.common.exceptions

from config import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# читаем список id задач
with open('tasks_id.txt', 'r') as file:
    task_id_list = file.read().split()

# указываем путь для драйвера браузера и открываем его
driver_path = os.path.abspath('chromedriver.exe')
driver = webdriver.Chrome(driver_path)
waiter = WebDriverWait(driver, timeout)
print('Начинаю работу...')
print('Авторизация на Bitrix24.')
# АВТОРИЗАЦИЯ
# открываем страницу авторизации
driver.get(bitrix_auth_url)
# находим элементы формы и заполняем их
# логин
login_input = driver.find_element_by_id('login')
login_input.send_keys(user_login)
time.sleep(timeout)
login_input.send_keys(Keys.ENTER)
# пароль
password_input = waiter.until(
    EC.presence_of_element_located((By.ID, 'password'))
)
password_input.send_keys(user_password)
password_input.send_keys(Keys.RETURN)
time.sleep(timeout)
print('Авторизация прошла успешно.')
print('Начинается парсинг задач')
# парсим страницы с задачами
depends_ids = {}
for task_id in task_id_list:
    driver.get(bitrix_url + bitrix_task_view_url + task_id + "/")
    depends_ids[task_id] = []
    try:
        # ищем все теги-ссылки на предшествующие задачи
        depends_tags = waiter.until(
            EC.presence_of_all_elements_located((By.XPATH, ".//div[text()='Предшествующие задачи']/..//a"))
        )
        # из каждого тега вычленяем его ID и записываем
        for depends_tag in depends_tags:
            depends_id = depends_tag.get_attribute('href').split("/")[-2]
            depends_ids[task_id].append(depends_id)
    except selenium.common.exceptions.TimeoutException:
        continue
with open('data.json', 'w') as outfile:
    json.dump(depends_ids, outfile)
# закрываем драйвер
driver.close()
print('Работа драйвера завершена.')
