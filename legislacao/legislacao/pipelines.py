from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
import base64
import csv
import scrapy
import uuid
import os

class LegislacaoPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if 'integra' in item:
            return [scrapy.Request(url='data:text/plain;base64,' 
                                   + base64.b64encode(item['integra'].encode('utf-8')).decode('ascii'))]

    def file_path(self, request, response=None, info=None):
        # Nome do arquivo baseado no URL ou outro critério
        return f'full_texts/{request.url.split("/")[-1]}.txt'

    def process_item(self, item, spider):
        with open('my_data.csv', 'a', newline='') as csvfile:
            header = [name for name in item.fields.keys() if name != 'integra']
            writer = csv.DictWriter(csvfile, fieldnames=header)
            
            if os.stat('my_data.csv').st_size == 0:
                writer.writeheader()
                
            row = dict(item)
            row.pop('integra')
            writer.writerow(row)
            
        # with open(f"full_texts/{uuid.uuid4()}.txt", 'w') as arquivo:
            # arquivo.write(item['integra'])

        return item




