from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome()
driver.maximize_window()

f1 = open("scraping.csv", "r", newline="", encoding="utf-8")
reader = csv.reader(f1)
f2 = open("scraping1.csv", "w", newline="", encoding="utf-8")
writer = csv.writer(f2)
ASIN = []
Product_Description = []
Manufacturer = []
Description = []

i = 1
for line in reader:
    driver.get(line[0])

    try:
        Product_Description.append(driver.find_element(By.ID, "productDescription_feature_div").text)
    except:
        try:
            Product_Description.append(driver.find_element(By.ID, "aplus_feature_div").text)
        except:
            Product_Description.append("NULL")

    Description.append(driver.find_element(By.ID, "feature-bullets").text)
    m = 1
    try:
        list_items = driver.find_elements(By.TAG_NAME, "li")
        for item in list_items:
            if "ASIN" in item.text:
                asin = item.find_elements(By.TAG_NAME, "span")[-1].text
                ASIN.append(asin)
                m = 0
                break

    except Exception:
        try:

            table_headers = driver.find_element(By.ID, "productDetails_feature_div").find_elements(By.TAG_NAME, "th")
            for header in table_headers:
                if "ASIN" in header.text:
                    parent_row = header.find_element(By.XPATH, "./ancestor::tr")
                    asin = parent_row.find_element(By.TAG_NAME, "td").text
                    ASIN.append(asin)
                    m = 0
                    break
        except Exception:
            ASIN.append("NULL")
            m = 0
    if m == 1:
        ASIN.append("NULL")

    n = 1
    try:
        list_items = driver.find_element(By.ID, "productDetails_feature_div").find_elements(By.TAG_NAME, "li")
        for item in list_items:
            if "Manufacturer" in item.text:
                manufacturer = item.find_elements(By.TAG_NAME, "span")[-1].text
                Manufacturer.append(manufacturer)
                n = 0
                break

    except Exception:
        try:
            list_items = driver.find_element(By.ID, "detailBulletsReverseInterleaveContainer_feature_v2").find_elements(
                By.TAG_NAME, "li")
            for item in list_items:
                if "Manufacturer" in item.text:
                    manufacturer = item.find_elements(By.TAG_NAME, "span")[-1].text
                    Manufacturer.append(manufacturer)
                    n = 0
                    break

        except:
            Manufacturer.append("NULL")
            n = 0
    if n == 1:
        Manufacturer.append("NULL")

    i = i + 1
    if i > 250:
        break
t = ("Product_Description", "Description", "ASIN", "Manufacturer")
writer.writerow(t)
for i in range(len(Product_Description)):
    if Manufacturer[i] != "NULL" and ASIN[i] != "NULL":
        t = (Product_Description[i], Description[i], ASIN[i], Manufacturer[i])
        writer.writerow(t)

driver.quit()
f1.close()
f2.close()

