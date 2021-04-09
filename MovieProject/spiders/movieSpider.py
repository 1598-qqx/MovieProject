import scrapy
import json
from urllib import parse
from ..items import MovieprojectItem
import re

class MoviespiderSpider(scrapy.Spider):
    name = 'movieSpider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/']
    header = {
        'Accept': 'application/json,text/plain,*/*',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://movie.douban.com/tag/',
        'Host': 'movie.douban.com'
    }
    startPage = [20]
    type_url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&"
    type_name = '电影'
    initStart = 0
    requestParam={
        'tags': str(type_name),
        'start': initStart
    }
    meta_dict ={
        'name': "",
        "rate": ""
    }
    complete_search_url = type_url +parse.urlencode(requestParam,encoding="utf-8")
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, headers=self.header)

    def parse(self, response):
        yield scrapy.Request(self.complete_search_url, headers=self.header,method="GET",callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        # url从每次的响应里分解出来的，不是实时的在线响应
        data_list = json.loads(str(response.text))['data']
        for json_dict in data_list:
            url = json_dict['url']
            self.meta_dict["name"] = json_dict['title']
            self.meta_dict['rate'] = json_dict['rate']
            yield scrapy.Request(url, callback=self.parse_movie_info,headers=self.header,method='GET',meta=self.meta_dict)
        for start in self.startPage:
            self.requestParam['start'] = start
            complete_search_list = self.type_url+parse.urlencode(self.requestParam,encoding="utf-8")
            yield scrapy.Request(complete_search_list,headers=self.header,method="GET",callback=self.parse_movie_list)

    def parse_movie_info(self,response):
        intro_list = response.xpath('//span[@property="v:summary"]/text()')
        category_list = response.xpath('//div[@id="info"]//span[@property="v:genre"]/text()').extract()
        if len(intro_list)>0:
            intro = re.compile("[\n\u3000 ]*").sub('',intro_list[0].extract())
        else:
            intro = ""
        if len(category_list)>0:
            category = '&'.join(category_list)
        else:
            category = ''
        item = MovieprojectItem()
        item['title'] = response.meta['name']
        item['rate'] = response.meta['rate']
        item['category'] = category
        item['intro'] = intro
        yield item


