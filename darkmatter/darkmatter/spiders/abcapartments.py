# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from darkmatter.items import DarkmatterItem


class AbcapartmentsSpider(scrapy.Spider):
	name = "abcapartments"
	start_urls = [
				 'http://www.abc-apartments.com/v2/index.php/properties-to-let',
				 'http://www.abc-apartments.com/v2/index.php/short-let',
				 'http://www.abc-apartments.com/v2/index.php/properties-for-sale'
				 ]

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):

		self._list_posts_xpath = "//div[@class='property_thumb_holder']/a/@href"
		self._title_xpath = "//div[@class='ip_mainheader']/h2/text()"
		self._description_xpath = "//td[@class='summary_left']/p/text()"
		self._location_xpath = "//dd[@class='tabs'][1]//div[@class='ip_sidecol_mainaddress']/text()"
		self._object_type_xpath = "//dd[1]//div[@class='ip_sidecol_categories']/a/text()"
		self._prize_xpath = "//span[@class='pe_price']/text()"

		self._bedrooms_xpath = "//div[@class='ip_beds']/text()"
		self._bathrooms_xpath = "//div[@class='ip_baths']/text()"


	def parse(self, response):
		propType = self.guessType(str(response.url))
		for href in response.xpath(self._list_posts_xpath):
			full_url = response.urljoin(href.extract())
			req =  scrapy.Request(full_url, callback=self.parse_info)
			req.meta['Type'] = propType
			yield req

	def guessType(self,url):
		url = str(url)
		finalkey = ""
		keyword = url.split('/')[5]
		if keyword == "properties-for-sale":
			finalkey = "sale"
		elif keyword == "short-let":
			finalkey = "short let"
		elif keyword == "properties-to-let":
			finalkey = "to let"
		else:
			finalkey = ""
		return finalkey

	def parse_info(self,response):
		Type = response.meta['Type']
		item = DarkmatterItem()

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		ObjectType = response.xpath(self._object_type_xpath).extract()
		ObjectType = self.cleanText(self.parseText(self.listToStr(ObjectType)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		Bedrooms = response.xpath(self._bedrooms_xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))

		Bathrooms = response.xpath(self._bathrooms_xpath).extract()
		Bathrooms = self.cleanText(self.parseText(self.listToStr(Bathrooms)))


		# Some of Items not Availabe on site so i am leaving it blank

		item['url'] 				= response.url
		item['title']				= title
		item['description'] 		= description
		item['location_address'] 	= location
		item['zipCode']				= ''
		item['Type']				= Type	
		item['ObjectType']			= ObjectType
		item['Price'] 				= prize
		item['PriceType'] 			= Type
		item['Rooms']	 			= ''
		item['Bathrooms']			= Bathrooms
		item['Bedrooms']			= Bedrooms
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


