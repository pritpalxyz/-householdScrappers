# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class SamuelestatesSpider(scrapy.Spider):
	name = "samuelestates"
	start_urls = [
			'http://www.samuelestates.com/property-search/?propertySearch=sales&location=&price_min=&price_max=&beds_min=&radius=0',
			'http://www.samuelestates.com/property-search/?propertySearch=lettings&location=&price_min=&price_max=&beds_min=&radius=0']

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._list_of_posts = "//div[@class='property-details']/div[@class='float-right']/a/@href"

		self._title_xpath = "//h1[@itemprop='name']/text()"

		self._description_xpath = "//span[@itemprop='description']/p/text()"

		self._prize_xpath = "//div[@class='property-price']/text()"

		self._next_page_xpath = "//a[@class='nextpostslink']/@href"


	def parse(self, response):
		uurl = str(response.url)
		Typo = uurl.split("=")[1].split("&")[0]

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
		location = title

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

