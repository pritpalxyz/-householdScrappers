# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class SamuelkingSpider(scrapy.Spider):
	name = "samuelking"

	start_urls = ['http://www.samuelking.co.uk/buy.php','http://www.samuelking.co.uk/property-to-rent.php']

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._list_of_posts = "//div[@class='propertyDivMore']/a/@href"

		self._title_xpath = "//div[@class='introText']/text()"

		self._description_xpath = "//div[@class='div4Right propertyDetailsDiv']/div/text()"

		self._prize_xpath = "//input[@name='LoanAmount']/@value"

	def parse(self, response):

		uurl = str(response.url)
		Typo = uurl.split("/")[-1].split(".")[0].replace("-"," ").replace("property to","").strip()

		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			req =   scrapy.Request(full_url, callback=self.parse_info)
			req.meta['Typo'] = Typo
			yield req

	def parse_info(self,response):

		Typo = response.meta['Typo']

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._title_xpath).extract()
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

