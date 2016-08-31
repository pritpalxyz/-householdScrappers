# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class ChilternpropertySpider(scrapy.Spider):
	name = "chilternproperty"
	start_urls = [
				'http://chilternproperty.com/listings.php?sale=1&list=1',
				   'http://chilternproperty.com/listings.php?sale=2&list=1']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._list_of_posts_xpath = "//p[@class='display_address']/a/@href"
		self._header_xpath = "//title/text()"
		self._description_xpath = "//div[@id='details_description_wrapper']/text()"
		self._location_xpath = "//div[@class='details_office_address']/text()"
		self._prize_xpath = "//div[@class='display_price']/text()"
		self._bedrooms_xpath = "//img[@src='images/listings-button-bedrooms-transparent.gif']/../text()"
		self._bathrooms_xpath = "//img[@src='images/listings-button-bathrooms-transparent.gif']/../text()"
		self._next_xpath = "//div[@class='pagin']/a[last()]/@href"


	def parse(self, response):
		for href in response.xpath(self._list_of_posts_xpath):
			full_url = response.urljoin(href.extract())
			yield  scrapy.Request(full_url, callback=self.parse_info)

		next_page = response.xpath(self._next_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)

	def parse_info(self,response):
		item = DarkmatterItem()

		title = response.xpath(self._header_xpath).extract()[0]

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))


		Type = str(response.url)
		Type = self.getType(Type)

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

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
		item['ObjectType']			= ''
		item['Price'] 				= prize
		item['PriceType'] 			= ''
		item['Rooms']	 			= ''
		item['Bathrooms']			= Bathrooms
		item['Bedrooms']			= Bedrooms
		item['Square'] 				= ''
		yield item

	def getType(self,urll):
		url = urll
		url = int(url.split("&")[-2].split("=")[1])
		tt= ""
		if url == 1:
			tt = "Sale"
		else:
			tt = "Let"
		return tt

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


