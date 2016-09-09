# -*- coding: utf-8 -*-
import scrapy




from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem


class AbbypropertiesSpider(scrapy.Spider):
	name = "abbyproperties"
	allowed_domains = ["abbyproperties.com"]
	start_urls = ['http://www.abbyproperties.com']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declate_xpath()
		locID = [5,6]
		for i in locID:
			myurl = """http://www.abbyproperties.com/search.aspx?ListingType=%s&areainformation=&areainformationname=Location&radius=0&statusids=1,2,3,6,7,8,16&igid=&imgid=&egid=&emgid=&category=1&defaultlistingtype=5&markettype=0&cur=GBP"""%(i)
			self.start_urls.append(myurl)

	def declate_xpath(self):
		self._list_xpath = "//img[@class='smallImage mainimage-scroller-item']/../@href"

		self._title_xpath = "//h1/text()"
		self._description_xpath = "//div[@class='PropertyDetails']//div[@class='property-fulldetails-section'][1]/span/text()"

		self._prize_xpath = "//div[@class='galleryInner']//h2/span/text()"

	def parse(self, response):
		for href in response.xpath(self._list_xpath):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

	def parse_info(self,response):
		item = DarkmatterItem()

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		url = str(response.url)

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize_type = ''.join([i for i in prize if not i.isdigit()])
		prize_type = prize_type.split(" ")[1]

		Type = str(url.split("/")[5])
		Type = Type.replace("for-","")

		country = str(url.split('/')[6])

		state = str(url.split('/')[7])
		state = state.replace("-"," ")

		location = "%s %s"%(state,country)

		

		ObjectType = str(url.split("/")[4])

		# Some of Items not Availabe on site so i am leaving it blank



		item['url'] 				= response.url
		item['title']				= title
		item['description'] 		= description
		item['location_address'] 	= location
		item['zipCode']				= ''
		item['Type']				= Type			 			
		item['ObjectType']			= ObjectType
		item['Price'] 				= prize
		item['PriceType'] 			= prize_type
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










