# -*- coding: utf-8 -*-
import scrapy


class SaffroninternationalSpider(scrapy.Spider):
    name = "saffroninternational"
    start_urls = ['http://www.saffroninternational.com/Results/List/1/']

    def parse(self, response):
    	for href in response.path("//img[@alt='Property']/../@href").extract():
    		print href