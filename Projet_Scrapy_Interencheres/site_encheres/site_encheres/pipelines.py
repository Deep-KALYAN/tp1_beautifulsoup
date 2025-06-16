# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import csv

class V1Pipeline:
    def open_spider(self,spider):
        self.file = open('products.csv','w',newline='',encoding='utf-8')
        self.writer = csv.DictWriter(self.file,fieldnames=['brand','model','fuel', 'mileage', 'price', 'image_url', 'product_url'])
        self.writer.writeheader

    def close_spider(self,spider):
        self.file.close()
 
    def process_item(self, item, spider):
        print(item)
        self.writer.writerow(item)
        return item
