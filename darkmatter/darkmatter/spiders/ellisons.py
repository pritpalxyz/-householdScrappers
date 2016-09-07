# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class EllisonsSpider(scrapy.Spider):
	name = "ellisons"
	start_urls = [
				'http://www.ellisons.uk.com/buy/property-for-sale',
				'http://www.ellisons.uk.com/let/property-to-let'
				]

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._list_of_posts = "//div[@class='module-content']/a/@href"

		self._title_xpath = "//h1[@class='details_h1']/text()"
		self._description_xpath = "//div[@id='module-description']/div/text()"

		self._location_xpath = "//div[@id='module-contact']/div/text()"


		self._prize_xpath = "//span[@class='nativecurrencyvalue']/text()"

		self._Bedrooms_xpath = "//div[@class='details-stats']/span[1]/text()"

		self._Bathrooms_xpath = "//div[@class='details-stats']/span[2]/text()"

		self._next_page_xpath = "//ul[@class='pagination']//li[@class='navarrow'][1]/a/@href"

	def parse(self, response):
		uurl = str(response.url)
		Typo = uurl.split("/")[3]

		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			req =  scrapy.Request(full_url, callback=self.parse_info)
			req.meta['Typo'] = Typo
			yield req
		next_page = response.xpath(self._next_page_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse)


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

		Bedrooms = response.xpath(self._Bedrooms_xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))

		Bathrooms = response.xpath(self._Bathrooms_xpath).extract()
		Bathrooms = self.cleanText(self.parseText(self.listToStr(Bathrooms)))

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

