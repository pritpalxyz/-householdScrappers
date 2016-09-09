# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class SalikandcoSpider(scrapy.Spider):
	name = "salikandco"
	start_urls = ['http://www.salikandco.com/search.aspx?ListingType=5&areainformation=&areainformationname=Location&radius=0&igid=&imgid=&egid=&emgid=&category=1&defaultlistingtype=5&markettype=0&cur=GBP']

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()
		for i in range(1,10):
			makeurl  = """http://www.salikandco.com/search.aspx?ListingType=6&areainformation=&areainformationname=Location&radius=0&igid=&imgid=&egid=&emgid=&category=1&defaultlistingtype=5&markettype=0&cur=GBP#&&OrderByColumnIndex=0&Page=%s&OrderByDirection=0&ItemsPerPage=10&Currency=GBP"""%(i)
			self.start_urls.append(makeurl)

	def declare_xpath(self):
		self._list_of_posts = "//h2/a/@href"

		self._title_xpath = "//h1[@id='ctl00_cntrlCenterRegion_cntrlProperties_item_0_ctl00_lblFormattedAddress']/text()"

		self._description_one_xpath = "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_item_0_ctl00_lblBriefDescription']//text()"
		self._description_two_xpath = "//div[@id='ctl00_cntrlCenterRegion_cntrlProperties_item_0_ctl00_cntrlFullDescription']//text()"

		self._prize_xpath = "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_item_0_ctl00_lblFormattedPrice']/text()"

		self._Bedrooms_xpath = "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_item_0_ctl00_lblBedrooms']/text()"

	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

	def parse_info(self,response):

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description_one = response.xpath(self._description_one_xpath).extract()
		description_one = self.cleanText(self.parseText(self.listToStr(description_one)))

		description_two = response.xpath(self._description_two_xpath).extract()
		description_two = self.cleanText(self.parseText(self.listToStr(description_two)))

		description = "%s %s"%(description_one,description_two)

		location = title

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize_type = prize.split(" ")[-1]

		prize = prize.split(" ")[2]

		Bedrooms = response.xpath(self._Bedrooms_xpath).extract()
		Bedrooms = self.cleanText(self.parseText(self.listToStr(Bedrooms)))

		uurl = str(response.url)
		Typo = uurl.split("/")[5].replace("-"," ")

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
		item['Bathrooms']           = ''
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

