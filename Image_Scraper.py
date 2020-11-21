################################ Import Packages################################################

from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import requests
import shutil
import random
import math
import uuid
import time
import os


##################################################################################################
######################################## Scraping Image ##########################################
##################################################################################################

def scroll_webpage(driver, n_images):

    print("Scrolling the web page...")

    if n_images > 20:

        i = 0
        while i < 5:
            # for scrolling page
            driver.execute_script(
                "window.scrollBy(0,document.body.scrollHeight)")

            try:
                # for clicking show more results button
                driver.find_element_by_xpath(
                    "/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
            except Exception as e:
                pass

            time.sleep(5)
            i += 1

    else:
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

    print("Scrolling End!")

    return None

############################################################################################


def scrap_images(url, n_images, driver_path):

    driver = webdriver.Chrome(driver_path)

    print("Opening the browser...")
    driver.get(url)

    scroll_webpage(driver, n_images)
    # Parsing
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Close the driver
    driver.close()
    print("Browser Closed!")

    img_tags = soup.find_all("img", class_="rg_i", limit=n_images)
    #imgs = soup.select('img[src^="data:image/jpeg"]')

    return img_tags

##########################################################################################################


def download_images(img_tags, save_directory):

    # Check the directory
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    else:
        pass

    # Downloading iamges
    print("Start downloading.....")

    for img in img_tags:

        path1 = save_directory

        try:
            name = str(uuid.uuid4())
            path2 = name+".jpg"
            file_path = os.path.join(path1, path2)
            urllib.request.urlretrieve(img['src'], file_path)
        except:
            pass

    # Check the number of downloaded image
    n_downloded_image = len(os.listdir(save_directory))

    print("Download finished!")
    print("{} image downloaded.".format(n_downloded_image))

    return None


##########################################################################################################
######################################## Main Function ###################################################
##########################################################################################################


def main():

    image_name = input("What do you want to download? ")
    n_images = int(input("How many images? "))
    url = 'https://www.google.com/search?tbm=isch&q='+image_name
    driver_path = "readonly/chromedriver.exe"
    image_directory = "readonly/images"+"_"+image_name

    tic = time.time()

    img_tags = scrap_images(url, n_images, driver_path)

    download_images(img_tags=img_tags, save_directory=image_directory)

    toc = time.time()

    elapsed_time = toc-tic

    print("Time elapsed {} seconds".format(elapsed_time))

    return None


#############################################################################################################


if __name__ == '__main__':

    main()
