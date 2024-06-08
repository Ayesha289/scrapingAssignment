import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/"

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI does not appear
        self.driver = webdriver.Chrome(options=chrome_options)

    def _fetch_coin_data(self, acronym):
        search_url = f"{self.BASE_URL}currencies/{acronym}/"
        self.driver.get(search_url)
        
        data = {}

        try:
            data['price'] = self.driver.find_element(By.CSS_SELECTOR, '.priceValue').text
            data['price_change'] = self.driver.find_element(By.CSS_SELECTOR, '.priceChange').text
            data['market_cap'] = self.driver.find_element(By.XPATH, '//div[contains(text(), "Market Cap")]/following-sibling::div').text
            data['volume'] = self.driver.find_element(By.XPATH, '//div[contains(text(), "Volume")]/following-sibling::div').text
            data['circulating_supply'] = self.driver.find_element(By.XPATH, '//div[contains(text(), "Circulating Supply")]/following-sibling::div').text
        except Exception as e:
            data['error'] = str(e)
        
        return data

    def scrape(self, acronyms):
        result = {}
        for acronym in acronyms:
            result[acronym] = self._fetch_coin_data(acronym)
        return result

    def __del__(self):
        self.driver.quit()
