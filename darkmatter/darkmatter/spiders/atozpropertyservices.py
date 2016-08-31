# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class AtozpropertyservicesSpider(scrapy.Spider):
	name = "atozpropertyservices"
	start_urls = ['http://atozpropertyservices.co.uk/properties/?filter_location=&filter_type=&filter_bedrooms=&filter_bathrooms=&filter_price_from=&filter_price_to=']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._post_list_xpath = "//div[@class='properties-grid']//div[@class='span3']//div[@class='property']/div[@class='title']//a/@href"
		self._title_xpath = "//h1/text()"
		self._description_xpath = "//div[@class='property-detail']/p/text()"

		self._location_xpath = "//th[text()='Location:']/following-sibling::td/text()"

		self._type_xpath = "//th[text()='Contract:']/following-sibling::td/text()"

		self._OrderType_xpath = "//th[text()='Type:']/following-sibling::td/text()"

		self._prize_xpath  = "//th[text()='Price:']/following-sibling::td/text()"

		self._prize_type_xpath = "//th[text()='Price:']/following-sibling::td/span/text()"

		self._bedrooms_xpath = "//th[text()='Bedrooms:']/following-sibling::td/text()"

		self._bathrooms_xpath = "//th[text()='Bathrooms:']/following-sibling::td/text()"

		self._pagination_xpath = "//li[@class='active']/following-sibling::li[1]/a/@href"


	def parse(self, response):
		for href in response.xpath(self._post_list_xpath):
			full_url = response.urljoin(href.extract())
			yield  scrapy.Request(full_url, callback=self.parse_info)

		next_page = response.xpath(self._pagination_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)


	def parse_info(self,response):
		item = DarkmatterItem()

		# Some of Items not Availabe on site so i am leaving it blank
		
		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		Type = response.xpath(self._type_xpath).extract()
		Type = self.cleanText(self.parseText(self.listToStr(Type)))

		ObjectType = response.xpath(self._OrderType_xpath).extract()
		ObjectType = self.cleanText(self.parseText(self.listToStr(ObjectType)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize_type = response.xpath(self._prize_type_xpath).extract()
		prize_type = self.cleanText(self.parseText(self.listToStr(prize_type)))


		Bedrooms = response.xpath(self._bedrooms_xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))

		Bathrooms = response.xpath(self._bathrooms_xpath).extract()
		Bathrooms = self.cleanText(self.parseText(self.listToStr(Bathrooms)))

		item['url'] 				= response.url
		item['title']				= title
		item['description'] 		= description
		item['location_address'] 	= location
		item['zipCode']				= ''
		item['Type']				= Type	
		item['ObjectType']			= ObjectType
		item['Price'] 				= prize
		item['PriceType'] 			= prize_type
		item['Rooms']	 			= ''
		item['Bathrooms']			= Bathrooms
		item['Bedrooms']			= Bedrooms
		item['Square'] 				= ''
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

