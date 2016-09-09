# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class ElroihomesSpider(scrapy.Spider):
	name = "elroihomes"
	start_urls = ['http://www.elroihomes.co.uk/property-list.htm?trans_type_id=2&price_min=0&price_max=7500000'
	,'http://www.elroihomes.co.uk/property-list.htm?trans_type_id=1&price_min=0&price_max=7500000']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._list_of_posts = "//div[@class='propText']/h2/a/@href"

		self._title_xpath = "//h1/text()"

		self._prize_xpath = "//a[@class='feeLink']/../text()"

		self._some_data_xpath = "//div[@id='propertyHeader']/div[@class='right']/text()"


	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

	def parse_info(self,response):

		Typo = 'sale'

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		location = title

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		somedata = response.xpath(self._some_data_xpath).extract()
		somedata = self.cleanText(self.parseText(self.listToStr(somedata)))

		ObjectType = somedata.split("|")[0]

		Bedrooms = somedata.split("|")[1]
		Bedrooms = Bedrooms.replace("Bedrooms","")


		item = DarkmatterItem()

		item['url']                 = response.url
		item['title']               = title
		item['description']         = ''
		item['location_address']    = location
		item['zipCode']             = ''
		item['Type']                = Typo                       
		item['ObjectType']          = ''
		item['Price']               = prize
		item['PriceType']           = ''
		item['Rooms']               = ''
		item['Bathrooms']           = ''
		item['Bedrooms']            = Bedrooms
		item['Square']              = ''
		yield item




	def listToStr(self,MyLst):
		_dumm = ""
		for i in MyLst:_dumm = "%s %s"%(_dumm,i)
		return _dumm


	def parseText(self, str):
		soup = BeautifulSoup(str, 'html.parser')
		return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0",' ',soup.get_text()).strip()

	def cleanText(self,text):
		soup = BeautifulSoup(text,'html.parser')
		text = soup.get_text();
		text = re.sub("( +|\n|\r|\t|\0|\x0b|\xa0|\xbb|\xab)+",' ',text).strip()
		return text 

