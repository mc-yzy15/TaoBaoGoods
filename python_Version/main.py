from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import yaml

class TaoBaoAutoBuyer:
    def __init__(self, config):
        self.config = config
        self.driver = self.setup_driver()

    def setup_driver(self):
        options = Options()
        options.add_argument(f"--window-size={self.config['window_size']}")
        if self.config['proxy']:
            options.add_argument(f"--proxy-server={self.config['proxy']}")
        driver = webdriver.Chrome(service=Service(self.config['driver_path']), options=options)
        return driver

    def login(self):
        self.driver.get("https://login.taobao.com")
        # 这里需要根据实际情况填写用户名和密码输入框的定位方式
        username_input = self.driver.find_element(By.ID, "fm-login-id")
        password_input = self.driver.find_element(By.ID, "fm-login-password")
        username_input.send_keys(self.config['username'])
        password_input.send_keys(self.config['password'])
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # 等待登录完成

    def add_to_cart(self, url, quantity):
        self.driver.get(url)
        # 这里需要根据实际情况填写添加到购物车按钮的定位方式
        add_to_cart_button = self.driver.find_element(By.ID, "J_AddToCart")
        for _ in range(quantity):
            add_to_cart_button.click()
            time.sleep(random.uniform(1, 2))  # 随机间隔

    def checkout(self):
        self.driver.get("https://cart.taobao.com/cart.htm")
        # 这里需要根据实际情况填写全选和结算按钮的定位方式
        select_all_checkbox = self.driver.find_element(By.ID, "J_SelectAllCbx1")
        checkout_button = self.driver.find_element(By.ID, "J_Go")
        select_all_checkbox.click()
        checkout_button.click()
        time.sleep(2)

    def place_order(self):
        # 这里需要根据实际情况填写提交订单按钮的定位方式
        submit_order_button = self.driver.find_element(By.ID, "J_Go")
        submit_order_button.click()
        time.sleep(2)

    def run(self):
        self.login()
        for item in self.config['items']:
            self.add_to_cart(item['url'], item['quantity'])
        self.checkout()
        self.place_order()

def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

if __name__ == "__main__":
    config = load_config('config.yaml')
    buyer = TaoBaoAutoBuyer(config)
    buyer.run()