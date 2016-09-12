# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class SandfordsSpider(scrapy.Spider):
	name = "sandfords"
	start_urls = ['http://www.sandfords.com/']

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

		for pageno in range(1,25):
			makeurl = """http://www.sandfords.com/property-lettings/properties-to-rent-in-london/page-%s"""%(pageno)
			self.start_urls.append(makeurl)
			makeurl = """http://www.sandfords.com/property-sales/properties-for-sale-in-london/page-%s"""%(pageno)
			self.start_urls.append(makeurl)


	def declare_xpath(self):
		self._list_of_xpath = "//div[@class='row']//h2/a/@href"

		self._title_xpath = "//div[@class='specification']//h1/text()"

		self._description_xpath = "//div[@id='description']//div[@class='column-text']/p/text()"

		self._prize = "//div[@class='price-box']//strong/span[@class='price-qualifier']/text()"

		self._prize_type = "//div[@class='price-box']//strong/span[@class='price-text']/text()"

		self._Typo = "//div[@class='price-box']/span/text()"

		self._Bedrooms_xpath = "//li/span[@class='ico bedrooms']/../text()"

		self._Bathrooms_xpath = "//li/span[@class='ico bathrooms']/../text()"


	def parse(self, response):
		for href in response.xpath(self._list_of_xpath):
			full_url = response.urljoin(href.extract())
			req =   scrapy.Request(full_url, callback=self.parse_info)
			yield req

	def parse_info(self,response):


		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = title

		prize = response.xpath(self._prize).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize_type = response.xpath(self._prize_type).extract()
		prize_type = self.cleanText(self.parseText(self.listToStr(prize_type)))

		Typo = response.xpath(self._Typo).extract()
		Typo = self.cleanText(self.parseText(self.listToStr(Typo)))

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

