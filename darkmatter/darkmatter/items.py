# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DarkmatterItem(scrapy.Item):
	url					= scrapy.Field()
	title				= scrapy.Field()
	description			= scrapy.Field()
	location_address	= scrapy.Field()
	zipCode				= scrapy.Field()
	Type				= scrapy.Field()#Sale or Rental ​ MANDATORY 
	ObjectType		= scrapy.Field() #Apartment or a House ​ MANDATORY 
	Price		= scrapy.Field()#numerical value + currency sign ​ MANDATORY (get the field even if it doesnt name the price, but is ‘Call for price’ or 
	PriceType			= scrapy.Field()# Sale, Weekly/Monthly/Yearly rental ​ MANDATORY 
	Rooms			= scrapy.Field() #number of rooms 
	Bathrooms		= scrapy.Field()#­ number of bathrooms 
	Bedrooms			= scrapy.Field()#number of bedrooms 
	Square			= scrapy.Field()#squar	
