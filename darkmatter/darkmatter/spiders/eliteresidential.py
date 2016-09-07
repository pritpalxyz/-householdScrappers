# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class EliteresidentialSpider(scrapy.Spider):
	name = "eliteresidential"
	start_urls = ['http://www.eliteresidential.co.uk/search.aspx?ListingType=5&category=1&igid=&imgid=9&egid=&emgid=&defaultlistingtype=6']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()
		for pageno in range(1,12):
			makeurl = """http://www.eliteresidential.co.uk/search.aspx?ListingType=6&category=1&igid=&imgid=9&egid=&emgid=&defaultlistingtype=6#&&Page=%s"""%(pageno)
			self.start_urls.append(makeurl)

	def declare_xpath(self):

		self._list_of_posts = "//div[@class='searchResultsContentContainer']//h2/a/@href"
		
		self.title_xpath = "//div[@class='fullDetailsPropertyInfo']//h1/span/text()"
		self.description_one_xpath = "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_lblBriefDescription']/text()"
		self.description_two_xpath = "//table[@id='ctl00_cntrlCenterRegion_cntrlProperties_ctl00_ctl00_cntrlBulletedList']//tr//text()"

		self.address_xpath = "//div[@class='fullDetailsPropertyInfo']//h1/span/text()"

		self.prize_xpath = "//span[@class='featuredPropertyPrice']/text()"




	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

	def parse_info(self,response):
		item = DarkmatterItem()

		title = response.xpath(self.title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		desc_one = response.xpath(self.description_one_xpath).extract()
		desc_one = self.cleanText(self.parseText(self.listToStr(desc_one)))

		desc_two = response.xpath(self.description_two_xpath).extract()
		desc_two = self.cleanText(self.parseText(self.listToStr(desc_two)))

		description = "%s %s"%(desc_one,desc_two)

		location = response.xpath(self.address_xpath).extract()

		prize = response.xpath(self.prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))



		item['url'] 				= response.url
		item['title']				= title
		item['description'] 		= description
		item['location_address'] 	= location
		item['zipCode']			= ''
		item['Type']				= ''			 			
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





