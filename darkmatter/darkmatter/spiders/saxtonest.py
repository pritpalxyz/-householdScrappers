# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem



class SaxtonestSpider(scrapy.Spider):
	name = "saxtonest"
	start_urls = ['http://www.saxtonest.co.uk/property.php?ptype=for-sale',
			'http://www.saxtonest.co.uk/property.php?ptype=to-let']


	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):

		self._list_of_posts = "//img[@src='/images/more.gif']/../@href"

		self._title_xpath = "//div[@class='property_details property_search']//div[@class='address']/text()"

		self._description_xpath = "//div[@class='fullDesc']//text()"

		self._prize_xpath = "//span[@class='price']/text()"

		self._typo_xpath = "//span[@class='tenure']/text()"

		self._object_type = "//div[@class='desc']//span[@class='bedroom'][1]/text()"


	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			req =   scrapy.Request(full_url, callback=self.parse_info)
			yield req


	def parse_info(self,response):

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = title

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))


		Typo = response.xpath(self._typo_xpath).extract()
		Typo = self.cleanText(self.parseText(self.listToStr(Typo)))

		ObjectType = response.xpath(self._object_type).extract()
		ObjectType = self.cleanText(self.parseText(self.listToStr(ObjectType)))

		item = DarkmatterItem()

		item['url']                 = response.url
		item['title']               = title
		item['description']         = description
		item['location_address']    = location
		item['zipCode']             = ''
		item['Type']                = Typo                     
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


