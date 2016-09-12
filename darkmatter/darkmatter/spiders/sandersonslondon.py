# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class SandersonslondonSpider(scrapy.Spider):
	name = "sandersonslondon"
	start_urls = ['http://www.sandersonslondon.co.uk/results.dtx?getdata=true&stype=sales&search=bystreet&_DSKeyIndex=&view=list',
				'http://www.sandersonslondon.co.uk/results.dtx?getdata=true&stype=rentals&search=bystreet&_DSKeyIndex=&view=list']

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._list_of_posts = "//img[@class='imagelist']/../@href"

		self._title_xpath = "//div[@id='details-titles']/h1/text()"

		self._description_xpath = "//div[@class='details-description']/text()"

		self._prize_xpath = "//div[@id='details-titles']/h2/text()"




	def parse(self, response):

		uurl = str(response.url)
		Typo = uurl.split("=")[2].split("&")[0]

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


		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))


		prize = prize.split("|")[0]

		location = title

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

