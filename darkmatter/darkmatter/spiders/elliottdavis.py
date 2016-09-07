# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem



class ElliottdavisSpider(scrapy.Spider):
	name = "elliottdavis"
	start_urls = ['http://www.elliottdavis.co.uk/searchresults.aspx']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):
		self._list_of_posts = "//a[@class='homepage-listings-link']/@href"

		self._title_xpath = "//h4/span[@id='ctl00_ContentPlaceHolder1_Label1']/text()"

		self._description_xpath = "//p[@class='MsoNormal']/text()"

		self._location_xpath = "//span[@id='ctl00_ContentPlaceHolder1_lblLocation']/text()"

		self._postal_code = "//span[@id='ctl00_ContentPlaceHolder1_lblPostCode']/text()"

		self._Type_object_xpath = "//span[@id='ctl00_ContentPlaceHolder1_lblType']/text()"

		self._prize_xpath = "//span[@class='pPrice']/text()"

		self._Bedrooms_xpath = "//span[@id='ctl00_ContentPlaceHolder1_lblBedroom']/text()"

		self._bathrooms_xpath = "//span[@id='ctl00_ContentPlaceHolder1_lblKitchen']/text()"

	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

	def parse_info(self,response):

		item = DarkmatterItem()

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		zipCode = response.xpath(self._postal_code).extract()
		zipCode = self.cleanText(self.parseText(self.listToStr(zipCode)))

		TypeOBJ = response.xpath(self._Type_object_xpath).extract()
		TypeOBJ = self.cleanText(self.parseText(self.listToStr(TypeOBJ)))

		TypeOBJ = TypeOBJ.replace("for","")
		Type = TypeOBJ.split("  ")[1]

		ObjectType = TypeOBJ.split("  ")[0]

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		tmpp = prize.split(" ")[0]
		prize_type = prize.replace(tmpp,"")
		prize = tmpp


		Bedrooms = response.xpath(self._Bedrooms_xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))

		Bathrooms = response.xpath(self._bathrooms_xpath).extract()
		Bathrooms = self.cleanText(self.parseText(self.listToStr(Bathrooms)))
				
		item['url']                 = response.url
		item['title']               = title
		item['description']         = description
		item['location_address']    = location
		item['zipCode']             = zipCode
		item['Type']                = Type                       
		item['ObjectType']          = ObjectType
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