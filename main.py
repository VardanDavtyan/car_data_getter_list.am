from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np

option = webdriver.ChromeOptions()
option.add_argument("start-maximized")

start_path = 'https://www.list.am/category/23?type=1&n=&bid=0&price1=&price2=&crc=&_a27=0&_a2_1=&_a2_2=&_a15=0&_a28_1=&_a28_2=&_a13=0&_a23=0&_a1_1=&_a1_2=&_a109=0&_a43=0&_a16=0&_a17=0&_a22=0&_a105=0&_a106=0&_a102=0&_a103=0&_a104=0'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)
driver.get('https://www.list.am/en/')
driver.implicitly_wait(20)
driver.get(start_path)
pages = 50

df = pd.DataFrame(columns=['Make', 'Model', 'Body Type', 'Year', 'Engine Type', 'Engine Size', 'Transmission',
                                'Drive Type', 'Mileage', 'Condition', 'Steering Wheel',
                                'Cleared Customs', 'Color', 'Wheel Size', 'Headlights', 'Interior Color', 'Interior Material',
                                'Sunroof','Car Price'])

for current_page in range(pages):

    container = driver.find_elements("class name", 'gl')[1:]
    car_links = container[0].find_elements("tag name", "a")
    car_link_count_per_page = len(car_links)

    for i in range(car_link_count_per_page):

        car_links[i].click()
        driver.switch_to.window(driver.window_handles[2])

        arr = {}

        vi = driver.find_element("class name", "vi")
        for i in range(len(vi.find_elements(By.CLASS_NAME, 'c'))):

            data = vi.find_elements(By.CLASS_NAME, 'c')[i]

            for column_index in range(len(df.columns)):
                try:
                    if (data.find_element(By.CLASS_NAME, 't').text == df.columns[column_index]):
                        arr[df.columns[column_index]] = data.find_element(By.CLASS_NAME, 'i').text
                except NoSuchElementException:
                    arr[df.columns[column_index]] = "NaN"

        try:
            price_button = driver.find_element(By.CLASS_NAME, 'price.x')
            #if not ("֏" in price_button.text):
            arr["Car Price"] = price_button.text
        except NoSuchElementException:
            arr["Car Price"] = "NaN"
        print(arr)

        df.loc[len(df)] = arr

        driver.close()
        driver.switch_to.window(driver.window_handles[1])

    driver.get(start_path)
    driver.find_element("class name", "dlf").find_elements("tag name", "a")[-1].click()



df.to_csv('car_data.csv', index=False)


driver.close()