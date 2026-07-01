import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver.exe', options=chrome_options)


url = "https://www.zhihu.com/"
driver.get(url)
driver.find_element(By.XPATH, '//div[@class="SignFlow-tab"]').click() #密码登录
uname = driver.find_element(By.XPATH, '//input[@type="text"]')#用户名
uname.send_keys('18942940307')
upw = driver.find_element(By.XPATH, '//input[@type="password"]')#密码框
upw.send_keys('hy123456')
time.sleep(1)
driver.find_element(By.XPATH, '//button[@type="submit"]').click() #登录按钮
input("手动验证后输入任意键")
time.sleep(1)
src = driver.page_source
print(src)
print("学号：232226205122")