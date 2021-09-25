from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv
#from ProfObj import *


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

filename = 'GamesUnder20Sale.csv'
f = open(filename, 'w')
f.write('Name, Price, % Off\n')

page = 1
url_to_scrape = "https://store.playstation.com/en-us/category/30826e82-088f-4cc2-aaa4-81507aa31353/1"
#url_to_scrape = 'https://store.playstation.com/en-us/category/fc08491d-94a7-4252-96dd-9d4f54b56041/'+ str(page) + '/'
#url_to_scrape = "https://store.playstation.com/en-us/category/b81cc589-d207-44dd-81ad-a63e15e05790/" + str(page) + "/"
driver.get(url_to_scrape)

while page <= 13:

    games = []

    time.sleep(3)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#main > section > div > div > div > div.psw-l-w-3\/4 > div.psw-l-w-1\/1 > ul > li:nth-child(5) > div > a > div > section > span"))
        )
        games = driver.find_elements_by_css_selector("#main > section > div > div > div > div.psw-l-w-3\/4 > div.psw-l-w-1\/1 > ul > li:nth-child(4) > div > a > div > section")
        #games = driver.find_elements_by_xpath('/html/body/div[3]/main/section/div/div/div/div[2]/div[2]/ul/li[4]/div/a/div/section')
    except:
        driver.quit()

    j = 1
    i = -1
    isFinished = 1

    while i < 23:

        isFinished += 1
        i += 1
        try:

            try:
                game_name = games[0].find_element_by_xpath('//*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[' + str(i+1) + ']/div/a/div/section/span[2]').text
                                                          # //*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[       14       ]/div/a/div/section/span
                                                          # //*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[       19       ]/div/a/div/section/span
            except NoSuchElementException:
                game_name = games[0].find_element_by_xpath('//*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[' + str(i + 1) + ']/div/a/div/section/span').text
                                                          # //*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[        1         ]/div/a/div/section/span

            price = games[0].find_element_by_xpath('//*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[' + str(i+1) + ']/div/a/div/section/div[' + str(j+1) + ']/div/span[1]').text
                                                  # //*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[      14        ]/div/a/div/section/div[        3       ]/div/span[1]
                                                  # //*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[      15        ]/div/a/div/section/div[        2       ]/div/span[1]
                                                  # //*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[      19        ]/div/a/div/section/div[        2       ]/div/span[1]
            percent_off = games[0].find_element_by_xpath('//*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[' + str(i+1) + ']/div/a/div/section/div[' + str(j) + ']/span').text
                                                        # //*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[      14        ]/div/a/div/section/div[      2       ]/span
                                                        # //*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[      19        ]/div/a/div/section/div[      1       ]/span


            if "," in game_name:
                game_name = game_name.replace(",", "-")

            percent_off = percent_off.replace("-", "")

            #print(game_name + ", " + price + ", " + percent_off + "\n")
            f.write(game_name + "," + price + "," + percent_off + "\n")

        except NoSuchElementException:
            if j == 1:
                j += 1
            elif j == 2:
                j -= 1

            if isFinished >= 40:
                break

            i -= 1
            continue

        except:
            print("an unexpected error has occurred")
            break

    driver.find_element_by_css_selector('#main > section > div > div > div > div.psw-l-w-3\/4 > div.psw-l-w-1\/1 > div > nav > button:nth-child(3) > span > span > svg').click()
    #time.sleep(5)
    page += 1

f.close()
driver.quit()

