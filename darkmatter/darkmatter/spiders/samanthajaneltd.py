# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class SamanthajaneltdSpider(scrapy.Spider):
	name = "samanthajaneltd"
	start_urls = ['https://www.onthemarket.com/agents/branch/samanthajane-ltd-charlton/properties/?search-type=to-rent&let-agreed=true',
	'https://www.onthemarket.com/agents/branch/samanthajane-ltd-charlton/properties/?search-type=for-sale&under-offer=true']


	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()


	def declare_xpath(self):
		self._list_of_posts = "//div[@class='main-image property-image']/a/@href"

		self._title_xpath = "//div[@class='panel-content']//h1/text()"

		self._description_xpath = "//div[@class='description']//text()"

		self._location_xpath = "//div[@class='panel-content']//div[@class='details-heading']/p/text()"

		self._prize_xpath = "//div[@class='panel-content']//span[@class='price-data']/text()"

		self._next_page_pagination = "//a[@title='Next page']/@href"

	def parse(self, response):

		uurl = str(response.url)
		Typo = uurl.split("=")[1].split("&")[0].replace("-"," ")


		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			req = scrapy.Request(full_url, callback=self.parse_info)
			req.meta['Typo'] = Typo
			yield req

		next_page = response.xpath(self._next_page_pagination)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse_info)

	def parse_info(self,response):

		Typo = response.meta['Typo']

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))



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

