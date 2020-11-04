import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from imutils import paths
from os import listdir
import argparse
import os
import time
from pathlib import Path
from PIL import Image
import sys

mode = ['LINK', 'IMAGE', 'ALL']
ap = argparse.ArgumentParser()
ap.add_argument('-s', '--text_search', default='' ,help='the text file to search')
ap.add_argument('-d', '--dest', type=str, required=True, 
    default='./urls.txt', help='the file name to save')
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
ap.add_argument("-t", '--total', default=1,
	help="start image name")
ap.add_argument("-f", "--fillzero", default=6, 
    help="fills zeros to name of image")
ap.add_argument("-g", '--chromedriver', default='',
    help="use chrome driver")
ap.add_argument('-m', '--mode', default='ALL')
args = vars(ap.parse_args())

google_image_engine = 'https://www.google.com.vn/imghp?hl=en&tab=wi&authuser=0&ogbl'
driver = None

def get_page_search(url):
    global driver
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome(executable_path=args['chromedriver'], options=option)
    driver.get(url)

def enter_search_text():
    input_search = driver.find_element_by_xpath("//input[@class='gLFyf gsfi']")
    input_search.send_keys(args['text_search'])
    input_search.submit()
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'rg_i')))
    
def save_url_file():
    folder = os.path.dirname(os.path.abspath(__file__))
    scroll_page()
    driver.execute_script(open('{}/js_console.js'.format(folder)).read())
    if args['dest']:
        time.sleep(0.5)
        try:
            os.rename('{}/urls.txt'.format(folder), args['dest'])
        except:
            os.rename('urls.txt', args['dest'])

def scroll_page():
    SCROLL_PAUSE_TIME = 0.6
    last_height = driver.execute_script("return document.body.scrollHeight")
    check = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            more = driver.find_element_by_xpath("//input[@type='button' and @value='Show more results']")
            if more:
                check += 1
                if check > 1:
                    break
                try:
                    more.click()
                    time.sleep(SCROLL_PAUSE_TIME * 2)
                except:
                    break
        last_height = new_height

def dowload_image():
    rows = open(args["dest"]).read().strip().split("\n")
    total = args['total']
    if not os.path.isdir(args['output']):
        Path(args['output']).mkdir(parents=True, exist_ok=True)

    for url in rows:
        try:
            r = requests.get(url, timeout=30)
            p = os.path.sep.join([args["output"], "{}.jpg".format(
                str(total).zfill(args['fillzero']))])
            f = open(p, "wb")
            f.write(r.content)
            f.close()
            print("[INFO] downloaded: {}".format(p))
            total += 1

        except:
            print("[INFO] downloaded: {} error ===> skipping".format(p))

    imagePaths = sorted(listdir(args["output"]))
    for imagePath in imagePaths:
        delete = False
        imagePath = '{}/{}'.format(args['output'], imagePath)
        try:
            image = Image.open(imagePath)
            if image is None:
                delete = True
            else:
                w, h = image.size
                if w and h:
                    pass
                else:
                    delete = True
        except:
            delete = True
        if delete:
            print("[INFO] deleting {}".format(imagePath))
            os.remove(imagePath)

def main():
    get_link()
    dowload_image()

def get_link():
    search = args['text_search']
    dr = args['chromedriver']
    if search and dr:
        get_page_search(google_image_engine)
        enter_search_text()
        save_url_file()
    else:
        print('[INFO] error must have search image text and chrome driver!!!')
        sys.exit()

if __name__ == '__main__':
    mode = args['mode']
    if mode == 'LINK':
        get_link()
    elif mode == 'IMAGE':
        dowload_image()
    else:
        main()

