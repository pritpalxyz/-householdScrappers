# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class ChoicestatesSpider(scrapy.Spider):
	name = "choicestates"
	allowed_domains = ["1stchoiceestates.com"]
	start_urls = ['http://www.1stchoiceestates.com']

	def __init__(self,location="london",*args, **kwargs):
		super(ChoicestatesSpider, self).__init__(*args, **kwargs)
		self.declare_xpath()
		self._location=location
		self._makeurl = """http://www.1stchoiceestates.com/?s=&sale-type=all&location=%s&type=&beds=&baths=&min=&max=&orderby=date&order=DESC&nr=10
		"""%(self._location)
		print self._makeurl
		self.start_urls.append(self._makeurl)

	def declare_xpath(self):
		self._list_all_posts_xpath = "//img[@class='attachment-dcr-half wp-post-image']/../@href"

		self._title_xpath = "//h1/text()"
		self._description_xpath = "//div[@class='description']/p/text()"
		self._location_state_xpath = "//div[@class='details-location']/a[last()]/text()"
		self._location_country_xpath = "//div[@class='details-location']/a[last()-1]/text()"
		self._prize_xpath = "//a[@class='btn btn-big btn-price']/text()"
		self._prize_type_xpath = "//a[@class='btn btn-big btn-price']/span/text()"

		self._bedrooms_xpath = "//span[@class='details-beds']/text()"
		self._bathrooms_xpath = "//span[@class='details-baths']/text()"

	def parse(self, response):
		for href in response.xpath(self._list_all_posts_xpath).extract():
			yield scrapy.Request(href,callback=self.parse_info)			

	def parse_info(self,response):
		item = DarkmatterItem()

		title = response.xpath(self._title_xpath).extract()

		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location_state = response.xpath(self._location_state_xpath).extract()
		location_state = self.cleanText(self.parseText(self.listToStr(location_state)))

		location_country = response.xpath(self._location_country_xpath).extract()
		location_country = self.cleanText(self.parseText(self.listToStr(location_country)))

		print "*"*100
		print location_state,location_country
		print "*"*100

		location = "%s %s"%(location_state,location_country)

		url = str(response.url)

		Type = url.split("/")[3]

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize_type = response.xpath(self._prize_type_xpath).extract()
		prize_type = self.cleanText(self.parseText(self.listToStr(prize_type)))

		bedrooms = response.xpath(self._bedrooms_xpath).extract()
		bedrooms = self.cleanText(self.parseText(self.listToStr(bedrooms)))

		bathrooms = response.xpath(self._bathrooms_xpath).extract()
		bathrooms = self.cleanText(self.parseText(self.listToStr(bathrooms)))


		item['url'] 				= response.url
		item['title']				= title
		item['description'] 		= description
		item['location_address'] 	= location
		item['zipCode']			= ''
		item['Type']				= Type			 			
		item['ObjectType']			= ''
		item['Price'] 				= prize
		item['PriceType'] 			= prize_type
		item['Rooms']	 			= ''
		item['Bathrooms']			= bathrooms
		item['Bedrooms']			= bedrooms
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






