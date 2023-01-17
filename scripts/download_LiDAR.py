import time
import os
import logging

from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import sys

argv = sys.argv
argv = [element if "--" not in element else "" for element in argv]
argv = [x for x in argv if x != ""]

method = argv[1]
GPS_file = argv[2]
latitude = argv[3]
longitude = argv[4]
output = argv[6]
output_folder = argv[7]
#change the path of output folder from forward slash to backslash 
dir_output = output_folder.replace('/', '\\')

word = latitude + ' ' + longitude

url = "https://pcrs.ign.fr/version3"
options = Options()
#change the default directory when dowloading
p = {'download.default_directory': dir_output}
options.add_experimental_option('prefs', p)
#options.headless = True
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver.get(url)

timeout = 60
try:    
    data_present = EC.visibility_of_element_located((By.ID, 'nb_dalles'))
    WebDriverWait(driver, timeout).until(data_present) 
except TimeoutException:
    print("Timed out waiting for database zip to load")

search = driver.find_element(By.XPATH, '//*[@id="map"]/div[2]/div[2]/div[2]/button')
search.click()

search_input = driver.find_element(By.XPATH, '//*[@id="map"]/div[2]/div[2]/div[2]/div[1]/input')
wait = WebDriverWait(driver, 10)
search_input.send_keys(latitude + ' ' + longitude)
search_input.send_keys(Keys.ENTER)
tile = driver.find_element(By.ID, 'map')

#TODO FIX
tile.click() #doesn't work anymore
time.sleep(2) 

try:
    zip_present = EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[3]/ul/li/a'))
    WebDriverWait(driver, timeout).until(zip_present) 

except TimeoutException:
    print("Timed out waiting for lidar zip to load")
    
las = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/ul/li/a')
print(las.text)
las.click()

time.sleep(2)

dl_wait = True
while dl_wait:
    time.sleep(1)
    dl_wait = True
    for fname in os.listdir(output_folder):
        if fname.endswith('.7z'):
            dl_wait = False
            old_name = fname
            os.rename(dir_output+r'/'+old_name, dir_output+r'/lidar.7z')
            
#close browser
driver.quit()
