from pathlib import Path
from urllib.parse import urljoin
import scrapy
from site_encheres.items import V1Item
from scrapy.loader import ItemLoader

class EncheresSpider(scrapy.Spider) :
    name = "v1"
    start_urls = [
        "https://www.car-encheres.fr/"
    ]

    
 
    def parse(self,response):
        # to access right url
        url = response.css("ul.home-categories  li.product-type-simple a::attr(href)").get()
        
        yield scrapy.Request(url=url, callback=self.parse_cars)

    def parse_cars(self,response):
        products = response.css('li.product')
        for i, product in enumerate(products, start=1):
            loader = ItemLoader(item=V1Item(), selector=product)
            try:
                # id = i
                # loader.add_css('id', id)

                title = product.css('h2.woocommerce-loop-product__title')
                # loader.add_css('title', 'h2.woocommerce-loop-product__title')
                # print(f"title: {title}")

                brand = title.css('span.text-uppercase::text').get('').strip()
                loader.add_css('brand', 'span.text-uppercase::text')
                print(f"Brand: {brand}")

                model = title.xpath('./text()[normalize-space()]').get('').strip()
                loader.add_value('model', model)
                # loader.add_css('model', './text()[normalize-space()]')
                print(f"Model: {model}")

                # Extract fuel type 
                fuel = product.xpath(
                    './/li[contains(., "Carburant")]/text()[normalize-space()]'
                ).get('').replace('Carburant', '').strip()
                loader.add_value('fuel', fuel)
                # loader.add_css('fuel', './/li[contains(., "Carburant")]/text()[normalize-space()]')
                print(f"Fuel: {fuel}")

                # Extract mileage 
                mileage = product.xpath(
                    './/li[contains(., "Kilométrage")]/text()[normalize-space()]'
                ).get('').replace('Kilométrage', '').strip()
                loader.add_value('mileage', mileage)
                # loader.add_css('mileage',  './/li[contains(., "Kilométrage")]/text()[normalize-space()]')
                print(f"Mileage: {mileage}")

                # Extract price
                price = product.css('span.price bdi::text').get('').strip()
                # loader.add_css('price', 'span.price bdi::text')
                loader.add_value('price', price)
                print(f"Price: {price}")

                # Extract image URL
                # Get the first <a> tag
                first_a = product.css('a:first-of-type')
            
                # Get all images in this <a> tag
                images = first_a.css('img')
            
                # Find the first non-SVG image
                image_url = None
                for img in images:
                    src = img.attrib.get('src', '')
                
                    # Skip SVG placeholders
                    if src.startswith('data:image/svg+xml'):
                        continue
                    
                    # Use first valid image found
                    if src:
                        image_url = src
                        break

                # loader.add_css('image_url', image_url)
                loader.add_value('image_url', image_url)
                print(f"Image_url: {image_url}")

                # Extract product URL
                product_url = product.css('a.woocommerce-LoopProduct-link::attr(href)').get('')
                # loader.add_css('product_url', 'a.woocommerce-LoopProduct-link::attr(href)')
                loader.add_value('product_url', product_url)
                print(f"Product_url: {product_url}")

                # yield {
                #     'id': str(i),  # Ensure id is string if needed
                #     'image_url': image_url if image_url else None,
                #     'brand': str(product.css('h2.woocommerce-loop-product__title span.text-uppercase::text').get('')).strip(),
                #     'model': str(product.css('h2.woocommerce-loop-product__title::text').getall()[-1]).strip(),
                #     'fuel': str(self.extract_attribute(product, "Carburant")),
                #     'mileage': str(self.extract_attribute(product, "Kilométrage")),
                #     'price': str(product.css('span.price bdi::text').get('')).strip(),
                #     'product_url': urljoin(response.url, str(product.css('a.woocommerce-LoopProduct-link::attr(href)').get('')))
                # }
                # yield {
                #     'id': id,
                #     'brand': brand,
                #     'model': model,
                #     'fuel': fuel,
                #     'mileage': mileage,
                #     'price': price,
                #     'image_url': image_url,
                #     'product_url': product_url,
                # }
                
            except Exception as e:
                self.logger.error(f"Error processing product #{i}: {str(e)}")
                continue
                       # Print extracted information
            # print(f"Id: {i}")     

            # print(f"title: {title}")      
            # print(f"Brand: {brand}")
            # print(f"Model: {model}")
            # print(f"Fuel: {fuel}")
            # print(f"Mileage: {mileage}")
            # print(f"Price: {price}")
            # print(f"Image_url: {image_url}")
            # print(f"Product_url: {product_url}")
            # print("-" * 50)

            yield loader.load_item()



        # yield from response.follow_all(css="ul.page-numbers a", callback=self.parse)
        # # pagination support
        # next_page = response.css('a.next::attr(href)').get()
        # if next_page:
        #     # yield
        #     # response.follow(next_page, self.parse_cars)page-numbers
        #     yield from response.follow_all(css="ul.pager a", callback=self.parse)

            

