import time
import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select

driver = webdriver.Firefox()
driver.maximize_window()
driver.implicitly_wait(10)
driver.get('https://172.16.3.205:1182/OPC/GFSOrder/index')
driver.find_element_by_id('account').send_keys('rebecca')
driver.find_element_by_id('password').send_keys('888')
driver.find_element_by_id('loginNewBtn').click()
time.sleep(1)
driver.find_element_by_xpath('//*[@id="pageHeader"]/div[2]/div/div/ul/li[7]/a').click() # 点击平台同步
time.sleep(2)
driver.find_element_by_xpath('//*[@id="pageHeader"]/div[1]/div/div[1]').click() # 点击账号
time.sleep(1)
driver.find_element_by_xpath('//*[@id="pageMainContent"]/div[2]/div/dl[2]/dd/ul/li[3]/a').click() # 点击未发货
driver.find_element_by_link_text('高级搜索').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="advancedSearch"]/div[2]/div/div[2]/div/ul').click() # 点击收件人国家
time.sleep(2)
driver.find_element_by_xpath('//*[@id="advancedSearch"]/div[2]/div/div[2]/div/div/ul/li[3]').click() # 选择阿富汗
# time.sleep(2)
driver.close()