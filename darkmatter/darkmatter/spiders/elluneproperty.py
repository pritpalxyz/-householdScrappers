# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class EllunepropertySpider(scrapy.Spider):
	name = "elluneproperty"
	start_urls = ['http://elluneproperty.co.uk/properties-to-rent/']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._list_of_posts = "//div[@class='listing-unit-img-wrapper col-md-6']//img/../@href"

		self._title_xpath = "//div[@class='myPropertyHeader']/h1/text()"

		self._description_xpath = "//div[@id='myContent']/text()"

		self._location_xpath = "//h1[@class='entry-title entry-prop']/text()"

		self._prize_xpath = "//div[@id='myPrice']/text()"

		self._bathrooms_xpath = "//div[@id='myBathroomBg']//span[@class='myPropertyNumber']/text()"

		self._Bedrooms_xpath = "//div[@id='myBedroomBg']//span[@class='myPropertyNumber']/text()"

	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

	def parse_info(self,response):

		Typo = 'rent'

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize_tmp = prize
		prize = prize.split("(")[0].split(" ")[0]

		prize_type = prize_tmp.split("(")[0].split(" ")[2]

		Bathrooms = response.xpath(self._bathrooms_xpath).extract()
		Bathrooms = self.cleanText(self.parseText(self.listToStr(Bathrooms)))

		Bedrooms = response.xpath(self._Bedrooms_xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))



		item = DarkmatterItem()

		item['url']                 = response.url
		item['title']               = title
		item['description']         = description
		item['location_address']    = location
		item['zipCode']             = ''
		item['Type']                = Typo                       
		item['ObjectType']          = ''
		item['Price']               = prize
		item['PriceType']           = prize_type
		item['Rooms']               = ''
		item['Bathrooms']           = Bathrooms
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

