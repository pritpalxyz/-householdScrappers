# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class SavoypropertySpider(scrapy.Spider):
	name = "savoyproperty"
	start_urls = [
			'http://www.savoyproperty.co.uk/property-status/for-rent/',
			'http://www.savoyproperty.co.uk/property-status/for-sale/'
			]

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()


	def declare_xpath(self):

		self._list_of_posts = "//a[@class='more-details']/@href"

		self._description_xpath = "//div[@class='content clearfix']//text()"

		self._location_xpath = "//div[@id='property-featured-image']/img/@alt"

		self._Typo_xpath = "//span[@class='status-label']/text()"

		self._prize_xpath = "//h5[@class='price']/span[2]/text()"

		self._pagination_xpath = "//div[@class='pagination']/a[@class='real-btn current']/following-sibling::a/@href"

	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			req =   scrapy.Request(full_url, callback=self.parse_info)
			yield req
			
		next_page = response.xpath(self._pagination_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)


	def parse_info(self,response):


		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		title = location

		Typo = response.xpath(self._Typo_xpath).extract()
		Typo = self.cleanText(self.parseText(self.listToStr(Typo)))


		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize = prize.split(" ")[0]

		item = DarkmatterItem()

		item['url']                 = response.url
		item['title']               = title
		item['description']         = description
		item['location_address']    = location
		item['zipCode']             = ''
		item['Type']                = Typo                       
		item['ObjectType']          = ''
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

