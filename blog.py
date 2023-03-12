from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import chromedriver_binary
import time
import urllib.parse
import urllib.request
from dotenv import load_dotenv
import os
import random


def exists_new_post():
    with open('newest.txt', 'r') as f:
        posted_title = f.readlines()[0].rstrip('\n')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')
    driver.get('https://www.nogizaka46.com/s/n46/diary/MEMBER/list?ima=1109&ct=55397')

    newest_post = driver.find_element(By.CLASS_NAME, 'bl--card')
    time.sleep(3)
    newest_title = newest_post.find_element(By.CLASS_NAME, 'bl--card__ttl').text
    newest_date = newest_post.find_element(By.CLASS_NAME, 'bl--card__date').text[:10]

    if posted_title != newest_title:
        with open('newest.txt', 'w') as f:
            f.write(newest_title + '\n' + newest_post.get_attribute("href") + '\n' + newest_date)
        return True

    return False


def save_images():
    with open('newest.txt', 'r') as f:
        txt = f.readlines()
        title = txt[0].rstrip('\n')
        url = txt[1].rstrip('\n')
        date = txt[2].rstrip('\n')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')
    driver.get(url)
    time.sleep(5)

    content = driver.find_element(By.CLASS_NAME, 'bd--edit')
    images = content.find_elements(By.TAG_NAME, 'img')

    path = title + '(' + date + ')'
    os.mkdir(path)

    for i, image in enumerate(images):
        image_url = image.get_attribute('src')
        with urllib.request.urlopen(image_url) as rf:
            img_data = rf.read()

        with open(path + '/' + str(i) + '.png', mode="wb") as wf:
            wf.write(img_data)
