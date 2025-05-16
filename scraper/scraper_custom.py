import random
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scraper.webcam import Webcam

query = "webcam"
url = f"https://www.google.fr/shopping"

def scrap_all() -> list[Webcam]:
    webcams = []

    # Configuration de selenium
    options = Options()
    options.add_argument("--headless")
    user_agent = "Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(options=options)
    
    # Créer un objet wait avec un timeout de 10 secondes
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(url)

        # Attendre et refuser les cookies
        cookie_button = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div/div[2]/div[1]/div[3]/form[1]/input[11]')))
        cookie_button.submit()

        # Attendre la barre de recherche et taper la recherche
        search_bar = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/c-wiz[1]/span/div/div/div[2]/c-wiz/form/div[2]/div[1]/input')))
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.ENTER)

        next = True

        iter = 0
        while next and iter < 50:
            iter += 1
            time.sleep(1.5)
            # Parsing de la page de recherche
            soup = BeautifulSoup(driver.page_source, "html.parser")
            products = soup.find_all("div", class_="P8xhZc")

            for product in products:
                name = product.find('div', class_="rgHvZc").find('a').text.strip()
                price = product.find('span', class_="HRLxBb").text.strip().translate(str.maketrans('', '', '+€\u202f\xa0()azertyuiopqsdfghjklmwxcvbnàèé')).replace(',', '.')
                price_type = product.find('span', class_="HRLxBb").text.strip().split('\xa0')[1].split(' ')[0]
                product_url = product.find('div', class_="rgHvZc").find('a')['href'].strip()
                rating = product.find("div", class_="m0amQc DApVsf")['aria-label'].split(' ')[0]
                rating_count = product.find("div", class_="dD8iuc d1BlKc").find("span").text.strip().translate(str.maketrans('', '', '()\u202f'))
                vendor = product.find_all("div", class_="dD8iuc")[1].text.strip().split(' ')[2:]

                webcams.append(Webcam(name, "https://google.com" + product_url, float(price), price_type, float(rating), int(rating_count), " ".join(vendor)))

            try :
                next_element = driver.find_element(By.PARTIAL_LINK_TEXT, "Suivant")
                next = next_element is not None
                next_element.click()
            except NoSuchElementException:
                next = False

    finally:
        driver.quit()

    return webcams

if __name__ == "__main__":
    success = False
    max_retries = 3
    retry_count = 0

    webcams = []
    while not success and retry_count < max_retries:
        try:
            webcams = scrap_all()
        except Exception as e:
            retry_count += 1
            print(f"Tentative {retry_count}/{max_retries} échouée : {e}")
            waiting_time = random.randint(1, 10)
            print(f"Attente de {waiting_time} secondes avant le prochain essai")
            time.sleep(waiting_time)
            continue
        else:
            success = True

    for webcam in webcams:
        print(webcam)