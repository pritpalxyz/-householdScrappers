# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class RavenhomesSpider(scrapy.Spider):
	name = "ravenhomes"
	start_urls = ['http://www.raven-homes.com/properties.aspx?Mode=0&PriceMax=0&Bedrooms=0&Areas=',
		'http://www.raven-homes.com/properties.aspx?Mode=1&PriceMax=0&Bedrooms=0&Areas=']


	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):

		self._list_of_posts = "//img[@class='propertyflash']/../@href"


		self._title_xpath = "//div[@style='float:left;']/h1/span/text()"

		self._description_xpath = "//div[@class='descriptionRight']//text()"

		self._location_xpath = "//abbr[@class='geo']/text()"

		self._prize_xpath = "//div[@style='float:right; height:40px;']/h1/span/text()"


	def parse(self, response):
		url = str(response.url)
		Typo = ""
		conte = int(url.split("?")[1].split("&")[0].split("=")[1])
		if conte == 1:
			Typo = "Rent"
		else:
			Typo = "Sale"
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			req =  scrapy.Request(full_url, callback=self.parse_info)
			req.meta['typo'] = Typo
			yield req

	def parse_info(self,response):
		typo = response.meta['typo']

		item = DarkmatterItem()

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		Type = typo

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))


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
		item['Bathrooms']			= ''
		item['Bedrooms']			= ''
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






