import scrapy
from imdbTop250.items import Imdbtop250Item, CastItem

class imdbTop250Spider(scrapy.Spider) :
	name = "spider"
	allowed_domains = ["imdb.com"]
	start_urls = [
		"http://www.imdb.com/chart/top?tt1954470&ref_=tt_awd"
	]

	def parse(self, response) :
		for sel in response.xpath("/html/body/div[1]/div/div[@id='pagecontent']/div[3]/div/div[@id='main']/div/span/div/div/div[2]/table/tbody/tr") :
			item = Imdbtop250Item()
			item['Title'] = sel.xpath('td[2]/a/text()')
			item['Ranking'] = sel.xpath('td[2]/text()')
			item['ReleaseDate'] = sel.xpath('td[2]/span/text()')
			item['Rating'] = sel.xpath('td[3]/strong/text()')
			# print "PATH", sel.xpath("td[2]/a/@href").extract()
			item['MainPageURL'] = "http://imdb.com" + sel.xpath("td[2]/a/@href").extract()[0]

			request = scrapy.Request(item['MainPageURL'], callback = self.parseMovieDetails)
			request.meta['item'] = item
			yield request
			print "\n\n\n\n"

	def parseMovieDetails(self, response) :
		item = response.meta['item']
		item = self.getBasicFilmInfo(item, response)
		item = self.getCastMemberInfo(item, response)
		return item

	def getBasicFilmInfo(self, item, response) :
		item['Director'] = response.xpath("/html/body/div[1]/div/div[@id='pagecontent']/div[@id='content-2-wide']/div[@id='maindetails_center_top']/div[2]/div/table/tbody/tr[1]/td[2]/div[4]/a/span/text()").extract()
		item['Writers'] = response.xpath("/html/body/div[1]/div/div[@id='pagecontent']/div[@id='content-2-wide']/div[@id='maindetails_center_top']/div[2]/div/table/tbody/tr[1]/td[2]/div[5]/a/span/text()").extract()
		item["Sinopsis"] = response.xpath("/html/body/div[1]/div/div[@id='pagecontent']/div[@id='content-2-wide']/div[@id='maindetails_center_top']/div[2]/div/table/tbody/tr[1]/td[2]/p/text()").extract()
		item["Genres"] = response.xpath("/html/body/div[1]/div/div[@id='pagecontent']/div[@id='content-2-wide']/div[@id='maindetails_center_top']/div[2]/div/table/tbody/tr[1]/td[2]/div[2]/a/span/text()").extract()
		return item

	def getCastMemberInfo(self, item, response) :
		item["CastMembers"] = []
		for index, castMember in enumerate(response.xpath("/html/body/div[1]/div/div[@id='pagecontent']/div[@id='content-2-wide']/div[@id='maindetails_center_bottom']/div[@id='titleCast']/table/tbody/tr")) :
			if(index == 0) :
				continue
			cast = CastItem()
			cast['Ranking'] = index
			cast['ActorName'] = self.ifNotEmptyGetIndex(castMember.xpath("td[2]/a/span/text()"))
			cast['CharacterName'] = self.ifNotEmptyGetIndex(castMember.xpath("td[4]/div/a/text()"))
			item["CastMembers"].append(cast)
		return item

	def ifNotEmptyGetIndex(self, item, index = 0) :
		if item :
			return item[index]
		else :
			return item