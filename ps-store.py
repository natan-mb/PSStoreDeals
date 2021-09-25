from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

filename = 'GamesUnder20Sale.csv'
f = open(filename, 'w')
f.write('Name, Price, % Off\n')

# enter number of pages on the ps store website for the specific deal 
pages = 10

#link to the first page of a ps store sale
url_to_scrape = "https://store.playstation.com/en-us/category/30826e82-088f-4cc2-aaa4-81507aa31353/1"
driver.get(url_to_scrape)

i = 0
while i <= pages:

    games = []

    time.sleep(3)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#main > section > div > div > div > div.psw-l-w-3\/4 > div.psw-l-w-1\/1 > ul > li:nth-child(5) > div > a > div > section > span"))
        )
        games = driver.find_elements_by_css_selector("#main > section > div > div > div > div.psw-l-w-3\/4 > div.psw-l-w-1\/1 > ul > li:nth-child(4) > div > a > div > section")
    except:
        print("Time limit exceeded: could not find element")
        driver.quit()
        break;

    
    i = -1  # counter variable, doubles as a tracker to advance to the next game entry
    j = 1   # adjusts xpath because price and percent_off have inconisistent xpath values between games
    isFinished = 1

    # run while i < (number of results per page - 1)
    while i < 23:

        #NOTE: I made the choice to select elements by xpath because class name didn't seem to work, and css selector returned inconsistent values
        
        isFinished += 1
        i += 1
        try:
           
            try:    # xpath sometimes selects "add-on" or other game tags instead of the actual game name
                game_name = games[0].find_element_by_xpath('//*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[' + str(i+1) + ']/div/a/div/section/span[2]').text
            except NoSuchElementException:
                game_name = games[0].find_element_by_xpath('//*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[' + str(i+1) + ']/div/a/div/section/span').text

            price = games[0].find_element_by_xpath('//*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[' + str(i+1) + ']/div/a/div/section/div[' + str(j+1) + ']/div/span[1]').text

            percent_off = games[0].find_element_by_xpath('//*[@id="main"]/section/div/div/div/div[2]/div[2]/ul/li[' + str(i+1) + ']/div/a/div/section/div[' + str(j) + ']/span').tex


            if "," in game_name:    #comma in name leads to inconsistencies when writing to csv
                game_name = game_name.replace(",", "-")

            #optional, removes the minus sign (e.g. -80% -> 80%)
            percent_off = percent_off.replace("-", "")

            f.write(game_name + "," + price + "," + percent_off + "\n")

        except NoSuchElementException:
            if j == 1:
                j += 1
            elif j == 2:
                j -= 1

            if isFinished > 40:    # protects against infinite loop, loop runs at most 40 times per page
                break

            i -= 1
            continue

        except:
            print("an unexpected error has occurred")
            break
    
    #advance to next page
    driver.find_element_by_css_selector('#main > section > div > div > div > div.psw-l-w-3\/4 > div.psw-l-w-1\/1 > div > nav > button:nth-child(3) > span > span > svg').click()
    
    i += 1

f.close()
driver.quit()

