import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class EbayProductScraper:
    def __init__(self, product_url):
        self.product_url = product_url
        self.driver = self.driver_init()
        self.driver.get(self.product_url)

    def driver_init(self):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        service = Service('C:\Program Files (x86)\chromedriver\chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def get_product_data(self):
        product_data = {}

        # Extract product name
        product_data['name'] = self.driver.find_element(By.XPATH,
                                                        '/html/body/div[2]/main/div[1]/div[1]/div[5]/div/div/div[2]/div/div[1]/div[1]/h1/span').text.strip()

        # Extract product image link
        product_data['photo_link'] = self.driver.find_element(By.XPATH,
                                                              '/html/body/div[2]/main/div[1]/div[1]/div[5]/div/div/div[2]/div/div[1]/div[1]/h1/span').get_attribute(
            'src')

        # Product URL
        product_data['product_link'] = self.product_url

        # Extract price
        price_tag = self.driver.find_element(By.XPATH,
                                             '/html/body/div[2]/main/div[1]/div[1]/div[5]/div/div/div[2]/div/div[1]/div[3]/div/div/div/span')
        product_data['price'] = price_tag.text.strip()

        # Extract seller information
        product_data['seller'] = self.driver.find_element(By.XPATH,
                                                          '/html/body/div[2]/main/div[1]/div[1]/div[5]/div/div/div[2]/div/div[1]/div[2]/div/div/div/a/span').text.strip()

        # Extract delivery price
        try:
            shipping_info = self.driver.find_element(By.XPATH,
                                                     '/html/body/div[2]/main/div[1]/div[1]/div[5]/div/div/div[2]/div/div[1]/div[10]/div/div/div/div[1]/div/div/div[2]/div/div[1]/span[1]')
            product_data['delivery_price'] = shipping_info.text.strip()
        except:
            product_data['delivery_price'] = 'Free Shipping'

        return product_data

    def to_json(self, output_file=None):
        product_data = self.get_product_data()
        product_data_json = json.dumps(product_data, indent=4)
        if output_file:
            with open(output_file, 'w') as f:
                f.write(product_data_json)
        else:
            print(product_data_json)

    def close(self):
        self.driver.quit()


# Example usage
if __name__ == "__main__":
    product_url = "https://www.ebay.com/itm/256116383719"  # Replace with a valid eBay product URL
    scraper = EbayProductScraper(product_url)
    scraper.to_json("product_data.json")  # Save to a file
    scraper.to_json()  # Print to console
    scraper.close()
