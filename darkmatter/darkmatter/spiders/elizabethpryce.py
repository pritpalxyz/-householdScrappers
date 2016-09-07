# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class ElizabethpryceSpider(scrapy.Spider):
	name = "elizabethpryce"
	start_urls = ('http://www.elizabethpryce.co.uk/sales/','http://www.elizabethpryce.co.uk/lettings/')

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._post_titles_xpath = "//a[@class='property_image']/@href"

		self._title_xpath = "//div[@class='title']//h1"

		self._description_xpath = "//div[@class='description']/div[@class='row']/div[@class='col-md-8']/p/text()"

		self._prize_xpath = "//p[@class='price']/text()"

		self._prize_type_xpath = "//p[@class='price']/span/text()"

		self._bedrooms_xpath = "//li[@class='bedrooms']/text()"

		self._bathrooms_xpath = "//li[@class='bathrooms']/text()"

		self._next_page_xpath = "//a[@class='next']/@href"

	def parse(self, response):
		uurl = str(response.url)
		uurl = uurl.split("/")[3]
		for href in response.xpath(self._post_titles_xpath):
			full_url = response.urljoin(href.extract())
			req =  scrapy.Request(full_url, callback=self.parse_info)
			req.meta['Type'] = uurl
			yield req
		next_page = response.xpath(self._next_page_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)

	def parse_info(self,response):

		Type = response.meta['Type']

		item = DarkmatterItem()

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

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
		item['location_address'] 	= ''
		item['zipCode']				= ''
		item['Type']				= Type		 			
		item['ObjectType']			= ''
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