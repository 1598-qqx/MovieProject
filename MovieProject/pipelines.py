# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class MovieprojectPipeline:
    def process_item(self, item, spider):
        json_str = json.dumps(dict(item), ensure_ascii=False)
        with open('D:/scrapyProjects/MovieProject/video/video.json',"a",encoding='gb18030', errors='ignore') as f:
            f.write(str((str(json_str)+"\n")))
        return item