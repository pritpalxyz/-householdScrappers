# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class ElkaypropertiesSpider(scrapy.Spider):
	name = "elkayproperties"
	start_urls = ['http://www.elkayproperties.co.uk/results.asp']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):

		self._list_of_posts = "//img[@class='results1a_photo']/../@href"


		self._header_title_xpath = "//h1/a/text()"

		self._description_xpath = "//div[@id='detail-content']/p[2]/text()"

		self._location_xpath = "//h3[@class='details']/text()"

		self._object_type = "//span[text()='Property Type:']/following-sibling::text()[1]"

		self._bedrooms_xpath = "//span[text()='Bedrooms:']/following-sibling::text()[1]"

		self._bathrooms_xpath = "//span[text()='Bathrooms:']/following-sibling::text()[1]"

		self._prize_xpath = "//div[@id='detail-content']/h2/text()"

		self._pagination_xpath = "//a[@class='next']/@href"


	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

		next_page = response.xpath(self._pagination_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)


	def parse_info(self,response):

		item = DarkmatterItem()

		title = response.xpath(self._header_title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))


		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		object_type = response.xpath(self._object_type).extract()
		object_type = self.cleanText(self.parseText(self.listToStr(object_type)))

		Bedrooms = response.xpath(self._bedrooms_xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))

		Bathrooms = response.xpath(self._bathrooms_xpath).extract()
		Bathrooms = self.cleanText(self.parseText(self.listToStr(Bathrooms)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))
		prize = prize.replace("Must be seen","")
		prize = prize.strip()
		prize_type = prize.split(" ")[1]


		item['url'] 				= response.url
		item['title']				= title
		item['description'] 		= description
		item['location_address'] 	= location
		item['zipCode']				= ''
		item['Type']				= ''		 			
		item['ObjectType']			= object_type
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