# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class ScarlettpropertyservicesSpider(scrapy.Spider):

	name = "scarlettpropertyservices"
	start_urls = [
			'http://www.scarlettpropertyservices.com/listings/flats-apartments',
			'http://www.scarlettpropertyservices.com/listings/bungalows',
			'http://www.scarlettpropertyservices.com/listings/commercial-property',
			'http://www.scarlettpropertyservices.com/listings/houses']

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()


	def declare_xpath(self):

		self._list_of_posts = "//a[@class='ip-property-header-accent']/@href"

		self._title_xpath = "//h1/text()"

		self._prize_xpath = "//h1/small[@class='ip-detail-price']/text()"

		self._description_xpath = "//div[@id='propdescription']//text()"

		self._typo_xpath = "//b[text()='Property Type:']/following-sibling::a/text()"

		self._location_xpath = "//div[@id='propdetails']//div[@class='ip-sidecol ip-mainaddress']/address//text()"


	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)


	def parse_info(self,response):


		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))


		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		typo = response.xpath(self._typo_xpath).extract()
		try:
			typo = typo[0]
		except:
			pass
		typo = self.cleanText(self.parseText(self.listToStr(typo)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))


		item = DarkmatterItem()

		item['url']                 = response.url
		item['title']               = title
		item['description']         = description
		item['location_address']    = location
		item['zipCode']             = ''
		item['Type']                = typo                       
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



