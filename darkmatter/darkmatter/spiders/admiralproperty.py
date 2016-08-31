# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class AdmiralpropertySpider(scrapy.Spider):
	name = "admiralproperty"
	allowed_domains = ["admiral-property.co.uk"]
	start_urls = ['http://www.admiral-property.co.uk/results.asp']


	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()


	def declare_xpath(self):
		self._list_of_posts_xpath = "//img[@class='img-responsive thumbnail']/../@href"
		self._title_xpath = "//h1/a//text()"
		self._description_xpath = "//div[@class='col-md-9']/p/text()"

		self._bedrooms_xpath = "//span[@class='bedroom']/text()"
		self._bathrooms_xpath = "//span[@class='bathroom']/text()"

		self._prize_xpath = "//span[@class='priceask']/text()"

		self._pagination_xpath = "//ul[@class='pagination']//li[last()]/a/@href"


	def parse(self, response):
		for href in response.xpath(self._list_of_posts_xpath):
			full_url = response.urljoin(href.extract())
			yield  scrapy.Request(full_url, callback=self.parse_info)

		next_page = response.xpath(self._pagination_xpath)
		if next_page:
			url = str(response.urljoin(next_page[0].extract()))
			currenturl = str(response.url)

			if currenturl == url:
				pass
			else:
				yield scrapy.Request(url, self.parse)

	def parse_info(self,response):
		item = DarkmatterItem()


		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		url = str(response.url)

		location = str(url.split("/")[4])
		location = location.replace("-"," ")

		Bedrooms = response.xpath(self._bedrooms_xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))

		Bathrooms = response.xpath(self._bathrooms_xpath).extract()
		Bathrooms = self.cleanText(self.parseText(self.listToStr(Bathrooms)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))



		item['url'] 				= response.url
		item['title']				= title
		item['description'] 		= description
		item['location_address'] 	= location
		item['zipCode']				= ''
		item['Type']				= ''	
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

