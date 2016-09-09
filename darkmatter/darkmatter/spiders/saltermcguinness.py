# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from bs4 import BeautifulSoup
import re
from darkmatter.items import DarkmatterItem

class SaltermcguinnessSpider(scrapy.Spider):
	name = "saltermcguinness"
	start_urls = ['http://www.saltermcguinness.net/sm08/pages/search2.asp']

	def __init__(self,*args,**kwargs):
		super(self.__class__, self).__init__(*args, **kwargs)
		self.declare_xpath()
		self.ids = []


	def declare_xpath(self):
		self._list_of_posts_id = "//input[@id='idnumber']/@value"

		self._next_page_xpath = "//a[text()=' Next >']/@href"

		self._address_xpath = "html/body/table[4]/tbody/tr[1]/td/table/tbody/tr/td[2]/table[1]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[1]/table/tbody/tr/td[2]"

		self._prize_xpath = "//span[@class='big_sub8']/text()"

		self._prize_type = "//span[@class='big_sub8']/following-sibling::span/text()"

		self._description_xpath = "//td[@class='main3_title' and @height='142']/text()"

	def parse(self, response):
		for idd in response.xpath(self._list_of_posts_id).extract():
			self.ids.append(idd)

		frmdata = {
				"property": "Any",
				"minbed": "Any",
				"area": "Any",
				"minprice":"300",
				"maxprice":"3000",
				"Submit":"Search"
				}
		url = "http://www.saltermcguinness.net/sm08/pages/search.asp"
		yield FormRequest(url, callback=self.parse_info, formdata=frmdata)


	def parse_info(self,response):
		for idd in response.xpath(self._list_of_posts_id).extract():
			self.ids.append(idd)

		next_page = response.xpath(self._next_page_xpath)
		if next_page:
			url = response.urljoin(next_page[0].extract())
			yield scrapy.Request(url, self.parse_info)
		else:
			for i in self.ids:
				makeurl = """http://www.saltermcguinness.net/sm08/pages/display.asp?idnumber=%s&image2.x=13&image2.y=11"""%(i)
				yield scrapy.Request(makeurl,self.getMainInfo)

		

	def getMainInfo(self,response):
		print response.url

		title = response.xpath(self._address_xpath).extract()
		title = self.cleanText(self.parseText(self.listToStr(title)))

		Typo = 'Let'
		prize = response.xpath(self._prize_xpath).extract()
		prize = self.cleanText(self.parseText(self.listToStr(prize)))

		prize_type = response.xpath(self._prize_type).extract()
		prize_type = self.cleanText(self.parseText(self.listToStr(prize_type)))

		location = title

		description = response.xpath(self._description_xpath).extract()
		description = self.cleanText(self.parseText(self.listToStr(description)))
			
		item = DarkmatterItem()

		item['url']                 = response.url
		item['title']               = title
		item['description']         = description
		item['location_address']    = location
		item['zipCode']             = ''
		item['Type']                = Typo                       
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

			