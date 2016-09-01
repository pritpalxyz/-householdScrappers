# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class MadisonbrookSpider(scrapy.Spider):
	name = "madisonbrook"
	start_urls = ['http://madisonbrook.com/Properties.html?Location=&CategoryID=1&MinBeds=0&Type=&MinPrice=100000&MaxPrice=10000000&Page=1&PageSize=16&Order=1&International=no',
		'http://madisonbrook.com/Properties.html?Location=&CategoryID=2&MinBeds=0&Type=&MinPrice=100000&MaxPrice=10000000&Page=1&PageSize=16&Order=1&International=no']

	def __init__(self,*args, **kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()

	def declare_xpath(self):

		self._list_of_posts = "//div[@class='borderi']/a[1]/@href"

		self._title_xpath = "//div[@id='ctl00_ContentPlaceHolder1_pnlPropertyDetails']/div[1]/div[2]/h2/text()"

		self._description_xpath = "//span[@class='price-box']/../p/text()"

		self._location_xpath = "//div[@id='ctl00_ContentPlaceHolder1_pnlPropertyDetails']/div[1]/div[2]/h3/text()"

		self._prize_xpath = "//span[@class='price-box']/text()"

		self._bedrooms_xpath = "//span[@class='sofa']/text()"

		self._bathrooms_xpath = "//span[@class='shower']/text()"

		self._last_page_count_xpath = "//div[@class='subnav']/ul/li[last()]/a/text()"

	def parse(self, response):
		for href in response.xpath(self._list_of_posts):
			full_url = response.urljoin(href.extract())
			yield scrapy.Request(full_url, callback=self.parse_info)

		try:
			page_count = response.xpath(self._last_page_count_xpath).extract()[0]
			page_count = self.cleanText(self.parseText(self.listToStr(page_count)))
			print page_count
			print "*"*100
			page_count = int(page_count)
	 
			url = str(response.url)
			catagory=url.split("&")[1]
			for uu in range(2,page_count+1):
				makeurl = """http://madisonbrook.com/Properties.html?Location=&%s&MinBeds=0&Type=&MinPrice=100000&MaxPrice=10000000&Page=%s&PageSize=16&Order=1&International=no"""%(catagory,uu)
				self.start_urls.append(makeurl)
		except:
			pass

	def parse_info(self,response):

		item = DarkmatterItem()

		title = response.xpath(self._title_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))

		location = response.xpath(self._location_xpath).extract()
		location = self.cleanText(self.parseText(self.listToStr(location)))

		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))


		bedrooms = response.xpath(self._bedrooms_xpath).extract()
		bedrooms = self.cleanText(self.parseText(self.listToStr(bedrooms)))

		bathrooms = response.xpath(self._bathrooms_xpath).extract()
		bathrooms = self.cleanText(self.parseText(self.listToStr(bathrooms)))

		Type = self.getType(str(response.url))


		item['url'] 				= response.url
		item['title']				= title
		item['description'] 		= description
		item['location_address'] 	= location
		item['zipCode']				= ''
		item['Type']				= Type			 			
		item['ObjectType']			= ''
		item['Price'] 				= prize
		item['PriceType'] 			= ''
		item['Rooms']	 			= ''
		item['Bathrooms']			= bathrooms
		item['Bedrooms']			= bedrooms
		item['Square'] 				= ''
		yield item


	def getType(self,urll):
		url =str(urll)
		conte = int(url.split("&")[1].split("=")[1])
		MyType = ""
		if conte == 1:
			MyType = "Buy"
		else:
			MyType = "Rent"
		return MyType



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




