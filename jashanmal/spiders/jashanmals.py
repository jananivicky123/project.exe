import scrapy
import pandas as pd

class ProductSpider(scrapy.Spider):
    name = "jashanmals"
    
    def start_requests(self):
        # Read product URLs from the Excel file
        df = pd.read_excel("C:/Users/JANANI/Python/selenium/products.xlsx")
        for index, row in df.iterrows():
            url = row['product_url']
            yield scrapy.Request(url=url, callback=self.parse_product)
    

    def parse_product(self, response):
        product_url = response.url
        img_url = response.xpath('//*[@class="aspect-ratio"]/img/@srcset').extract_first()
        name = response.xpath('//*[@class="product-meta__title heading h1"]/text()').extract_first()
        sku = response.xpath('//*[@class="product-meta__sku-number"]/text()').extract_first()
        
        normal_price = response.xpath('//*[@class="price price--compare"]/text()').extract_first()
        discount_price = response.xpath('//*[@class="price price--highlight"]/text()').extract_first()
        normal_price = normal_price.strip() if normal_price else discount_price
        discount_price = discount_price.strip() if discount_price else normal_price


        stock = response.xpath('//*[@class="product-form__inventory inventory inventory--low"]/text()').extract_first()
        stock = stock.strip() if stock else 'Out of stock'

        description = response.xpath('//*[@class="rte text--pull"]/p/text()').extract_first()

        data = {
            "product_url": product_url,
            "img_url": img_url,
            "name": name,
            "sku": sku,
            "normal_price": normal_price,
            "discount_price": discount_price,
            "stock": stock,
            "description": description
        }

        yield data


