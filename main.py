import chromedriver_binary
import datetime
from dotenv import load_dotenv
import glob
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib.parse
import time

import blog


def login(TWITTER_BASE, LOGIN_ID, PASSWORD):
    twitter_base = TWITTER_BASE + "login/"
    account = LOGIN_ID
    password = PASSWORD

    driver.get(twitter_base)
    time.sleep(2)

    element_account = driver.find_element(By.NAME, 'text')
    element_account.send_keys(account)

    element_login_next = driver.find_element(By.XPATH, '//div/span/span[text()="次へ"]')

    element_login_next.click()
    time.sleep(5)

    element_pass = driver.find_element(By.NAME, "password")
    element_pass.send_keys(password)

    element_login = driver.find_element(By.XPATH, '//div/span/span[text()="ログイン"]')

    element_login.click()
    time.sleep(5)
    driver.refresh()
    time.sleep(5)


def tweet():
    with open('newest.txt', 'r') as f:
        txt = f.readlines()
        title = txt[0].rstrip('\n')
        url = txt[1].rstrip('\n')
        date = txt[2].rstrip('\n')

    headline = title + '(' + date + ')'
    currentDir = os.getcwd()
    files = glob.glob(os.path.join(currentDir + '/' + headline, '*'))

    elm_create_tweet_btn = driver.find_element(By.XPATH, '//a[@data-testid="SideNav_NewTweet_Button"]')
    elm_create_tweet_btn.click()
    time.sleep(5)

    for i, image in enumerate(files):
        if i % 4 == 0:
            if i == 0:
                text_area = driver.find_element(By.XPATH, r'//div[@data-testid="tweetTextarea_0"]')
                text_area.send_keys(headline + '\n' + url + '\n1/' + str(len(files) // 4 + 1)
                                    + str(random.randint(1, 1000)))
            else:
                elem_add_btn = driver.find_element(By.XPATH, '//div[@data-testid="addButton"]')
                elem_add_btn.click()
                time.sleep(3)
                text_area = 'tweetTextarea_' + str(i // 4)
                text_area = driver.find_element(By.XPATH, r'//div[@data-testid="' + text_area + r'"]')
                text_area.send_keys(str(i // 4 + 1) + '/' + str(len(files) // 4 + 1) + str(random.randint(1, 1000)))

        elm_upload_img = driver.find_element(By.XPATH, '//input[@data-testid="fileInput"]')
        elm_upload_img.send_keys(image)
        time.sleep(1)

    elem_tweet_btn = driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]')

    with open("log.txt", mode='a') as f:
        try:
            elem_tweet_btn.click()
            time.sleep(10)
            f.write("\n『" + title + "』" + "投稿完了 (" + str(datetime.datetime.now()) + ")")

        except:
            f.write("\n『" + title + "』" + "投稿失敗 (" + str(datetime.datetime.now()) + ")")

    driver.close()


if __name__ == "__main__":
    print("開始")
    load_dotenv()
    TWITTER_BASE = os.getenv('TWITTER_BASE')
    LOGIN_ID = os.getenv('LOGIN_ID')
    PASSWORD = os.getenv('PASSWORD')
    print(f"LOGIN_ID:::{LOGIN_ID}")

    options = webdriver.ChromeOptions()

    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.set_window_size('1200', '1000')

    if blog.exists_new_post():
        print(f"new_postあり")
        with open("newest.txt", mode='r') as f:
            txt = f.readlines()
            title = txt[0].rstrip('\n')

        blog.save_images()
        print(f"save_images終了")

        login(TWITTER_BASE, LOGIN_ID, PASSWORD)
        print(f"ログイン終了")
        tweet()
        print(f"tweet終了")
    else:
        print(f"new_postなし")
        with open("log.txt", mode='a') as f:
            f.write("\n更新なし (" + str(datetime.datetime.now()) + ")")