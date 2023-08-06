import selenium
from selenium.webdriver import Chrome
driver = Chrome()
from webdriver_manager.chrome import ChromeDriverManager
driver = Chrome(ChromeDriverManager().install())
driver.get("https://www.johnpacker.co.uk")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import uuid

cookies_button = driver.find_element_by_xpath('//*[@id="cookie_banner_all"]')
cookies_button.click()

search_bar = driver.find_element_by_xpath('//*[@id="header_search_search_for"]')
search_bar.click()
search_bar.send_keys('Trumpet')
search_bar.send_keys(Keys.ENTER)

container = driver.find_element_by_xpath('//div[@class="row prod_wrapper"]')
trumpet_list = container.find_elements_by_xpath('./div')
data = {"UUID": [],"Name": [],"Key": [],"Bell_size": [],"Pistons": [],"Bore": [],"Water_key": [],"Body": [],"Lyre_box": [],"Mouth_piece": [],"Warranty": [],"Price": []}
num_trumpet = len(trumpet_list)
new_id = uuid.uuid4()
for i in range(num_trumpet):
    container = driver.find_element_by_xpath('//div[@class="row prod_wrapper"]')
    trumpet = container.find_elements_by_xpath('./div')[i]
    trumpet.click()
    time.sleep(10)
    data['UUID'].append(new_id)
    try:
        Name = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[1]').text
        data['Name'].append(Name)
    except NoSuchElementException:
        data['Name'].append(None)  
    try:
        Key = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[2]').text
        data['Key'].append(Key)
    except NoSuchElementException:
        data['Key'].append(None)
    try:
        Bell_size = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[3]').text
        data['Bell_size'].append(Bell_size)
    except NoSuchElementException:
        data['Bell_size'].append(None)
    try:
        Pistons = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[4]').text
        data['Pistons'].append(Pistons)
    except NoSuchElementException:
        data['Pistons'].append(None)
    try:
        Bore = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[5]').text
        data['Bore'].append(Bore)
    except NoSuchElementException:
        data['Bore'].append(None)
    try:
        Water_key = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[6]').text
        data['Water_key'].append(Water_key)
    except NoSuchElementException:
        data['Water_key'].append(None)
    try:
        Body = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[7]').text
        data['Body'].append(Body)
    except NoSuchElementException:
        data['Body'].append(None)
    try:
        Lyre_box = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[9]').text
        data['Lyre_box'].append(Lyre_box)
    except NoSuchElementException:
        data['Lyre_box'].append(None)
    try:
        Mouth_piece = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[10]').text
        data['Mouth_piece'].append(Mouth_piece)
    except NoSuchElementException:
        data['Mouth_piece'].append(None)
    try:
        Warranty = driver.find_element_by_xpath('//*[@id="prod_det_get_body"]/section/div[2]/span/ul/li[11]').text
        data['Warranty'].append(Warranty)
    except NoSuchElementException:
        data['Warranty'].append(None)
    try:
        Price = driver.find_element_by_xpath('//*[@id="price_details"]/div/p/span[2]').text
        data['Price'].append(Price)
    except NoSuchElementException:
        data['Price'].append(None)
    driver.back()
    time.sleep(5)
data
import pandas as pd
df = pd.DataFrame.from_dict(data)
print(df)