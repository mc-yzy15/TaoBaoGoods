# main.py

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
import os
import tkinter as tk
from tkinter import messagebox

class TaoBaoAutoBuyer:
    def __init__(self, config, root):
        self.config = config
        self.root = root
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
        self.update_status("正在登录...")
        username_input = self.driver.find_element(By.ID, "fm-login-id")
        password_input = self.driver.find_element(By.ID, "fm-login-password")
        username_input.send_keys(self.config['username'])
        password_input.send_keys(self.config['password'])
        password_input.send_keys(Keys.RETURN)
        time.sleep(5)  # 等待登录完成
        self.update_status("登录完成")

    def add_to_cart(self, url, quantity):
        self.driver.get(url)
        self.update_status(f"正在添加 {url} 到购物车...")
        add_to_cart_button = self.driver.find_element(By.ID, "J_AddToCart")
        for _ in range(quantity):
            add_to_cart_button.click()
            time.sleep(random.uniform(1, 2))  # 随机间隔
        self.update_status(f"已添加 {url} 到购物车")

    def checkout(self):
        self.driver.get("https://cart.taobao.com/cart.htm")
        self.update_status("正在结算...")
        select_all_checkbox = self.driver.find_element(By.ID, "J_SelectAllCbx1")
        checkout_button = self.driver.find_element(By.ID, "J_Go")
        select_all_checkbox.click()
        checkout_button.click()
        time.sleep(2)
        self.update_status("结算完成")

    def place_order(self):
        self.update_status("正在提交订单...")
        submit_order_button = self.driver.find_element(By.ID, "J_Go")
        submit_order_button.click()
        time.sleep(2)
        self.update_status("订单提交完成")

    def run(self):
        self.login()
        for item in self.config['items']:
            self.add_to_cart(item['url'], item['quantity'])
        self.checkout()
        self.place_order()

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

def load_config(file_path):
    if not os.path.exists(file_path):
        create_default_config(file_path)
        messagebox.showinfo("配置文件创建", f"默认配置文件已创建在 {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config

def create_default_config(file_path):
    default_config = """
# config.yaml
# 默认配置文件
window_size: "1280,720"
proxy: ""
driver_path: "chromedriver.exe"
username: "your_username"
password: "your_password"
items:
  - url: "https://example.com/item1"
    quantity: 1
  - url: "https://example.com/item2"
    quantity: 2
"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(default_config)

def main(root):
    config_file_path = 'DefaultConfig.yaml'
    config = load_config(config_file_path)
    buyer = TaoBaoAutoBuyer(config, root)
    buyer.run()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("淘宝自动购买器")
    root.geometry("400x300")

    status_label = tk.Label(root, text="初始化...", font=("Helvetica", 14))
    status_label.pack(pady=20)

    root.status_label = status_label
    main(root)
    root.mainloop()