import scrapy

from scrapy.loader import ItemLoader
from ..items import KombankItem
from itemloaders.processors import TakeFirst


class KombankSpider(scrapy.Spider):
	name = 'kombank'
	start_urls = ['https://www.kombank.me/me/vesti']

	def parse(self, response):
		post_links = response.xpath('//div[@class="card-body"]/ul/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col-md-8 vest"]//text()[normalize-space() and not(ancestor::div[@class="datum"] | ancestor::h1 | ancestor::div[@class="arhiva"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="col-md-8 vest"]/div[@class="datum"]/text()').get()

		item = ItemLoader(item=KombankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
