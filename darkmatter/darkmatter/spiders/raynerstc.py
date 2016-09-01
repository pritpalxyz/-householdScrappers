# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class RaynerstcSpider(scrapy.Spider):
	name = "raynerstc"
	start_urls = ['http://www.raynerstc.com/sold-properties',
		'http://www.raynerstc.com/properties-for-sale']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):

		self._list_of_posts = "//a[@class='readmoreBtn']/@href"

		self._title_xpath = "//h1/text()"

		self._description_xpath = "//div[@id='propdescription']//p//text()"

		self._location_xpath = "//div[@id='propdetails']//address//text()"

		self._zipcode_xpath = "//div[@id='propdetails']//address/text()"

		self._Type_xpath = "//div[@id='propdescription']//b[text()='Sale Type']/../text()"

		self._prize_xpath = "//h1/small/text()"

		self._Bedrooms_xpath = "//img[@src='/images/bedrooms.png']/following-sibling::strong[1]/text()"

		self._Bathrooms_xpath = "//img[@src='/images/bathrooms.png']/following-sibling::strong[1]/text()"

		self._next_page_xpath = "//li/a[@title='Next']/@href"

	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			req =  scrapy.Request(full_url, callback=self.parse_info)

		next_page = response.xpath(self._next_page_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)


	def parse_info(self,response):

		item = DarkmatterItem()

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		zipcode = response.xpath(self._zipcode_xpath).extract()
		zipcode = self.cleanText(self.parseText(self.listToStr(zipcode)))

		Type  = response.xpath(self._Type_xpath).extract()

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		Bedrooms = response.xpath(self._Bedrooms_xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))

		Bathrooms = response.xpath(self._Bathrooms_xpath).extract()
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






