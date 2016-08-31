# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class ChestertonsSpider(scrapy.Spider):
	name = "chestertons"
	start_urls = ['http://www.chestertons.com/property-to-rent/search-results/',
				'http://www.chestertons.com/property-to-buy/search-results/']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._list_posts_xpath = "//ul[@id='listSearchResults']//div[@class='property-details']/h3/a/@href"


		self._title_xpath = "//h1/text()"
		self._description_xpath = "//div[@class='content-block-left']/p//text()"
		self._address_xpath = "//h2[@itemprop='address']//text()"
		self._zipcode_xpath = "//span[@itemprop='postalCode']/text()"

		self._property_price_xpath = "//p[@class='property-price']//span[@class='price-conversion']/text()"
		self._bedrooms_Xpath = "//span[@class='icon-beds']/../text()"
		self._bathrooms_xpath = "//span[@class='icon-baths']/../text()"
		self._pagination_xpath = "//div[@class='navigation']/a/@href"

	def parse(self, response):
		for href in response.xpath(self._list_posts_xpath):
			full_url = response.urljoin(href.extract())
			yield  scrapy.Request(full_url, callback=self.parse_info)

		next_page = response.xpath(self._pagination_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)


	def parse_info(self,response):
		item = DarkmatterItem()

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._address_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		zipcode = response.xpath(self._zipcode_xpath).extract()
		zipcode = self.cleanText(self.parseText(self.listToStr(zipcode)))

		Type = self.getType(response.url)

		prize = response.xpath(self._property_price_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		Bedrooms = response.xpath(self._bedrooms_Xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))

		Bathrooms = response.xpath(self._bedrooms_Xpath).extract()
		Bathrooms = self.cleanText(self.parseText(self.listToStr(Bathrooms)))

		item['url'] 				= response.url
		item['title']				= title
		item['description'] 		= description
		item['location_address'] 	= location
		item['zipCode']				= zipcode
		item['Type']				= Type	
		item['ObjectType']			= ''
		item['Price'] 				= prize
		item['PriceType'] 			= ''
		item['Rooms']	 			= ''
		item['Bathrooms']			= Bathrooms
		item['Bedrooms']			= Bedrooms
		item['Square'] 				= ''
		yield item

	def getType(self,urll):
		url = str(urll)
		dumm = url.split("/")[3]
		cont = ""
		if dumm == 'property-to-buy':
			cont = "Buy"
		else:
			cont = "Sale"
		return cont


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

