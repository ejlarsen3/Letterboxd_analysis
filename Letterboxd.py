import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup as bs
import requests

def scrape_movie(url, driver): 
    sub_dict = {}
    # Scrape data immediately on page (Title, Director, Year, Total Views, Avg Rating, Each rating #, Runtime, etc.)
    # returns None if any errors occur


    # start BeautifulSoup
    r = requests.get(url)
    r.raise_for_status()
    movie_html = bs(r.text, "html.parser")
    try:
    # Instantiate webdriver
        driver.get(url)
        driver.implicitly_wait(8)
        title = driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/section[1]/h1[1]").text


        year = int(movie_html.find('small', attrs= {"class": "number"}).text)
        director = movie_html.find("span", attrs= {"class": "prettify"}).text
        desc = movie_html.find("div", attrs= {"class": "truncate"}).text.strip()
        # rtgs = movie_html.findAll(attrs= {"class": "rating-histogram-bar"})
        runtime = movie_html.find('p', attrs= {"class": "text-link text-footer"}).text.strip().split("\xa0")[0]
        
        cast_raw = movie_html.findAll(attrs= {"class": "text-slug tooltip"})[:10]
        cast = []
        for c in cast_raw:
            cast.append(c.text)
        cast = ", ".join(cast)
        driver.implicitly_wait(8)   
        watched = driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[1]/section[1]/ul[1]/li[1]/a[1]").text
        lists = driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[1]/section[1]/ul[1]/li[2]/a[1]").text
        liked = driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[1]/section[1]/ul[1]/li[3]/a[1]").text
        
        point5 = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[1]/a[1]").text.strip().split(" ")[0].replace(",",""))
        one = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[2]/a[1]").text.strip().split(" ")[0].replace(",",""))
        one5 = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[3]/a[1]").text.strip().split(" ")[0].replace(",",""))
        two = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[4]/a[1]").text.strip().split(" ")[0].replace(",",""))
        two5 = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[5]/a[1]").text.strip().split(" ")[0].replace(",",""))
        three = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[6]/a[1]").text.strip().split(" ")[0].replace(",",""))
        three5 = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[7]/a[1]").text.strip().split(" ")[0].replace(",",""))
        four = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[8]/a[1]").text.strip().split(" ")[0].replace(",",""))
        four5 = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[9]/a[1]").text.strip().split(" ")[0].replace(",",""))
        five = int(driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/aside[1]/section[2]/div[1]/ul[1]/li[10]/a[1]").text.strip().split(" ")[0].replace(",",""))
        
        genre_url = url + "genres/"
        
        r2 = requests.get(genre_url)
        genre_html = bs(r2.text, "html.parser")
        
        genres_raw = genre_html.find("div", attrs = {"class": "text-sluglist capitalize"}).findChildren()
        genres = []
        for tag in genres_raw[1:]:   # the first genre tag text is a combination of all of the genres, we don't want this
            genres.append(tag.text.strip())
        
        genres = ", ".join(genres)
        themes_raw = genre_html.findAll("div", attrs = {"class": "text-sluglist capitalize"})[1].findChildren()
        themes = []
        for t in themes_raw[1:-1]:
            themes.append(t.text)
        
        themes = ", ".join(themes)
        rel_url = url + "releases/" 
        
        r3 = requests.get(rel_url)
        rel_html = bs(r3.text, "html.parser")
        
        premiere_date = rel_html.find("h5", {"class": "date"}).text
            
        
        
        tot_ratings = point5 + one + one5 + two + two5 + three + three5 + four + four5 + five
        avg_rtg = round((point5*.5 + one + one5*1.5 + 2*two + 2.5*two5 + 3*three + 3.5*three5 + 4*four + 4.5*four5 + 5*five)/ tot_ratings, 3)
    except(ElementClickInterceptedException, NoSuchElementException, AttributeError, IndexError):
        print(driver.current_url)
        return [None, None]

    # return title, year, director, desc, runtime, cast, watched, lists, liked, point5, one, one5, two, two5, three, three5, four, four5, five, avg_rtg, tot_ratings, genres, themes, premiere_date

    # add to sub_dict, then add sub_dict to movie_dict
    sub_dict = {"Year": year,
               "Director": director,
               "Desc.": desc,
               "Runtime": runtime,
               "Cast": cast,
               "Watched": watched,
               "Lists": lists,
               "Liked": liked,
               "0.5": point5,
               "1": one,
               "1.5": one5,
               "2": two,
               "2.5": two5,
               "3": three,
               "3.5": three5,
               "4": four,
               "4.5": four5,
               "5": five,
               "Average Rating": avg_rtg,
               "Total Rated": tot_ratings,
               "Genres": genres,
               "Themes": themes,
               "Premiere Date": premiere_date}
    return title, sub_dict

full_movie_dict = {}
driver = webdriver.Chrome()
driver.get("https://letterboxd.com/films/popular/")
driver.implicitly_wait(5)

# find and click each movie on the page by its xpath
for j in range(28):
    # instantiate a new webdriver for each new page of movies, prevents timeouts and chrome from crashing
    if j==0:
        driver = webdriver.Chrome()
        driver.get("https://letterboxd.com/films/popular/")
        driver.implicitly_wait(5)
    else:
        driver = webdriver.Chrome()
        driver.get(f"https://letterboxd.com/films/popular/page/{j+1}/")
        driver.implicitly_wait(5)

    for i in range(72):
        try:
            xpath = f"/html[1]/body[1]/div[2]/div[1]/section[1]/div[2]/ul[1]/li[{i+1}]"
            driver.find_element(By.XPATH, xpath).click()
            # except possible errors to continue, would just be missing data
        except (ElementClickInterceptedException, NoSuchElementException, AttributeError):
            driver.implicitly_wait(2)
            continue
        url = driver.current_url
        driver.implicitly_wait(10)
        try:
            full_movie_dict[scrape_movie(url, driver)[0]] = scrape_movie(url, driver)[1]
        except WebDriverException:
            driver = webdriver.Chrome()
            print(j, i)
            driver.get("https://letterboxd.com/films/popular/")
            break
        driver.implicitly_wait(8)
        driver.back()

df = pd.DataFrame(full_movie_dict)

df = df.T

df.to_csv("Letterboxd.csv")
