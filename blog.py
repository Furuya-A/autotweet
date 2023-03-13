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


def reload_newest_post(member):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')
    driver.get(member['blog_url'])

    newest_post = driver.find_element(By.CLASS_NAME, 'bl--card')
    time.sleep(3)

    if member['newest_title'] != newest_post.find_element(By.CLASS_NAME, 'bl--card__ttl').text:
        member['newest_title'] = newest_post.find_element(By.CLASS_NAME, 'bl--card__ttl').text
        member['newest_url'] = newest_post.get_attribute("href")
        member['newest_date'] = newest_post.find_element(By.CLASS_NAME, 'bl--card__date').text[:10]
        member['exists_new_post'] = True
    else:
        member['exists_new_post'] = False

    return member


def save_images(member):
    with open('newest.txt', 'r', encoding='utf-8') as f:
        txt = f.readlines()
        title = txt[0].rstrip('\n')
        url = txt[1].rstrip('\n')
        date = txt[2].rstrip('\n')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')
    driver.get(member['newest_url'])
    time.sleep(5)

    content = driver.find_element(By.CLASS_NAME, 'bd--edit')
    images = content.find_elements(By.TAG_NAME, 'img')

    path = 'images/' + member['name'] + '/' + member['newest_date'] + '(' + member['newest_title'] + ')'
    os.mkdir(path)

    for i, image in enumerate(images):
        image_url = image.get_attribute('src')
        with urllib.request.urlopen(image_url) as rf:
            img_data = rf.read()

        with open(path + '/' + str(i) + '.png', mode="wb") as wf:
            wf.write(img_data)
