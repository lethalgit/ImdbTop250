# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class Imdbtop250Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	Title = Field()
	Rating = Field()
	Ranking = Field()
	ReleaseDate = Field()
	MainPageURL = Field()

	Director = Field()
	Writers = Field()
	Sinopsis = Field()
	Genres = Field()
	
	CastMembers = Field()

class CastItem(scrapy.Item) :
	ActorName = Field()
	CharacterName = Field()
	Ranking = Field()
