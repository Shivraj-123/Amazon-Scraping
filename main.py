from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

f = open("scraping.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(f)

driver = webdriver.Chrome()
driver.get("https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1")
driver.maximize_window()

for i in range(0, 18):
    product_URL = []
    product_Name = []
    Product_Price = []
    Number_of_review = []
    Rating = []

    divs = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    for div in divs:
        product_URL.append(
            div.find_element(By.XPATH, ".//h2/a").get_attribute("href"))
        product_Name.append(
            div.find_element(By.XPATH, ".//h2/a/span").text)
        Product_Price.append(
            div.find_element(By.XPATH, ".//span[@class='a-price-whole']").text)
        try:
            Number_of_review.append(
                div.find_element(By.XPATH, ".//div[@class='a-row a-size-small']").find_element(By.XPATH,
                                                                                               ".//span[last()]/a/span").text)
        except Exception as e:
            Number_of_review.append("NULL")
        try:
            Rating.append(
                div.find_element(By.XPATH, ".//div[@class='a-row a-size-small']").find_element(By.XPATH,
                                                                                               ".//span/span").text)
        except Exception as e:
            Rating.append("NULL")

    for i in range(len(product_Name)):
        if Rating[i] != "NULL" and  Number_of_review[i] != "NULL":
            t = (product_URL[i], product_Name[i], Product_Price[i], Rating[i], Number_of_review[i])
            writer.writerow(t)

    driver.get(driver.find_elements(By.XPATH,
                                    "//a[@class='s-pagination-item s-pagination-next s-pagination-button "
                                    "s-pagination-separator']")[
                   -1].get_attribute("href"))
driver.quit()
f.close()