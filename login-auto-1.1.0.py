from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://github.com/login")

USUARIO = "SenaaTeste"
SENHA = "isaq20110319"

driver.find_element(By.ID, "login_field").send_keys(USUARIO)
driver.find_element(By.ID, "password").send_keys(SENHA)
driver.find_element(By.NAME, "commit").click()

driver.switch_to.new_window('tab')
driver.get("https://github.com")