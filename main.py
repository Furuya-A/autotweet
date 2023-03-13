import chromedriver_binary
import csv
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


def login(LOGIN_ID, PASSWORD):
    login_url = "https://twitter.com/login/check?lang=en"
    account = LOGIN_ID
    password = PASSWORD

    driver.get(login_url)
    time.sleep(2)

    element_account = driver.find_element(By.NAME, 'text')
    element_account.send_keys(account)
    element_login_next = driver.find_element(By.XPATH, '//div/span/span[text()="Next"]')
    element_login_next.click()
    time.sleep(5)

    element_pass = driver.find_element(By.NAME, "password")
    element_pass.send_keys(password)
    elm_login_btn = driver.find_element(By.XPATH, '//div[@data-testid="LoginForm_Login_Button"]')
    elm_login_btn.click()

    time.sleep(5)
    driver.refresh()
    time.sleep(5)


def tweet(member):
    title = member['newest_title']
    print(title)
    url = member['newest_url']
    print(url)
    date = member['newest_date']
    print(date)
    print( member['name'])

    text = title + '(' + date + ')'
    currentDir = os.getcwd()
    files = glob.glob(os.path.join(currentDir + '/' + 'images/' + member['name'] + '/' +
                                   date + '(' + title + ')', '*'))
    print(files)

    elm_create_tweet_btn = driver.find_element(By.XPATH, '//a[@data-testid="SideNav_NewTweet_Button"]')
    elm_create_tweet_btn.click()
    time.sleep(5)

    for i, image in enumerate(files):
        if i % 4 == 0:
            if i == 0:
                text_area = driver.find_element(By.XPATH, r'//div[@data-testid="tweetTextarea_0"]')
                text_area.send_keys(text + '\n' + url + '\n1/' + str(len(files) // 4 + 1))
            else:
                elem_add_btn = driver.find_element(By.XPATH, '//div[@data-testid="addButton"]')
                elem_add_btn.click()
                time.sleep(3)
                text_area = 'tweetTextarea_' + str(i // 4)
                text_area = driver.find_element(By.XPATH, r'//div[@data-testid="' + text_area + r'"]')
                text_area.send_keys(str(i // 4 + 1) + '/' + str(len(files) // 4 + 1))

        elm_upload_img = driver.find_element(By.XPATH, '//input[@data-testid="fileInput"]')
        elm_upload_img.send_keys(image)
        time.sleep(1)

    elem_tweet_btn = driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]')
    elem_tweet_btn.click()

    time.sleep(10)


if __name__ == "__main__":
    load_dotenv()
    members = []

    with open("config.csv", "r", encoding="utf-8_sig") as csvfile:
        # CSVファイルを辞書型で読み込む
        old_data = csv.DictReader(csvfile, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                           skipinitialspace=True)
        for member in old_data:
            members.append(member)

    for i in range(len(members)):
        print(members[i])

        options = webdriver.ChromeOptions()

        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        driver.set_window_size('1200', '1000')

        member = blog.reload_newest_post(members[i])
        print(members[i])

    field_name = members[0].keys()

    with open(r'config.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_name)
        writer.writeheader()
        writer.writerows(members)

    for member in members:
        if member['exists_new_post']:
            # blog.save_images(member)
            options = webdriver.ChromeOptions()

            # options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=options)
            driver.set_window_size('1200', '1000')
            login(member['id'], member['password'])
            print(member)
            tweet(member)

            driver.close()

            with open("log.txt", mode='a', encoding='utf-8') as f:
                f.write(f"\n{member['name']}: 更新完了 (" + str(datetime.datetime.now()) + ")")
        else:
            with open("log.txt", mode='a', encoding='utf-8') as f:
                f.write(f"\n{member['name']}: 更新なし (" + str(datetime.datetime.now()) + ")")

# def test():
#     currentDir = os.getcwd()
#     files = glob.glob(os.path.join(currentDir + '/' + 'images/' + '一ノ瀬美空' + '/' +
#                                    '2023.03.12' + '(' + 'ありがとうと！一ノ瀬美空' + ')', '*'))
#     print(files)
#
# test()
