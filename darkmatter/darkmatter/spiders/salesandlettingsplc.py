# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class SalesandlettingsplcSpider(scrapy.Spider):
	name = "salesandlettingsplc"
	start_urls = ['http://www.salesandlettingsplc.co.uk']

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()
		types = [5,6]
		for i in types:
			for page in range(1,25):
				makeurl = """http://www.salesandlettingsplc.co.uk/search.aspx?ListingType=%s&areainformation=&areainformationname=All+Locations&igid=&imgid=9&egid=&emgid=&category=1&defaultlistingtype=5&markettype=0&cur=GBP#&&OrderByColumnIndex=0&Page=%s&OrderByDirection=0&ItemsPerPage=10&Currency=GBP"""%(i,page)
				self.start_urls.append(makeurl)

	def declare_xpath(self):

		self._list_of_posts = "//div[@class='ListResultContainer']/h3//a/@href"

		self._title_xpath = "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_item_0_ctl00_lblFormattedAddress']/text()"


		self._description_xpath = "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_item_0_ctl00_lblBriefDescription']/text()"

		self._prize_xpath = "//span[@id='ctl00_cntrlCenterRegion_cntrlProperties_item_0_ctl00_lblFormattedPrice']/text()"


	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

	def parse_info(self,response):


		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = title


		urlll = str(response.url)
		Typo = urlll.split("/")[5].replace('-',' ')


		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize_type = prize.split(" ")[-1]

		prize = prize.split(" ")[0]


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

