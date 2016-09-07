# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class EllisandcoSpider(scrapy.Spider):
	name = "ellisandco"
	start_urls = [
		'http://www.ellisandco.co.uk/property/for-sale/',
		'http://www.ellisandco.co.uk/property/to-rent']


	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):

		self._list_of_posts = "//li[@class='property__link property__link--details']/a/@href"

		self._title_xpath = "//h1[@class='summary__heading']/text()"

		self._description_xpath = "//h2[text()='Full description']/following-sibling::p/text()"

		self._location_xpath = "//span[@class='page--property__snapshot__location']/text()"

		self._prize_xpath = "//span[@class='page--property__snapshot__price']/text()"

		self._next_page_pagination = "//a[@class='pagination__next']/@href"

	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

		next_page = response.xpath(self._next_page_pagination)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)

	def parse_info(self,response):

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))


		ObjectType = title
		ObjectType = ObjectType.split(" ")[2]


		uurl = str(response.url)
		Type = uurl.split("/")[4]
		Type = Type.replace("-"," ")

		item = DarkmatterItem()

		item['url']                 = response.url
		item['title']               = title
		item['description']         = description
		item['location_address']    = location
		item['zipCode']             = ''
		item['Type']                = Type                       
		item['ObjectType']          = ObjectType
		item['Price']               = prize
		item['PriceType']           = ''
		item['Rooms']               = ''
		item['Bathrooms']           = ''
		item['Bedrooms']            = ''
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
