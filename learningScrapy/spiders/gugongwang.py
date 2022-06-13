import scrapy


class GugongwangSpider(scrapy.Spider):
    name = 'gugongwang'
    allowed_domains = ['gugong.net']
    start_urls = ['http://gugong.net/']

    def parse(self, response):
        for href in response.css('div.t_2 h3 > a'):
            yield response.follow(href, callback=self.level_a_parse)

    def level_a_parse(self, response):
        for href in response.css('div.t_4 h3 > a'):
            yield response.follow(href, callback=self.level_b_parse)

    def level_b_parse(self, response):
        for href in response.css('ul.list2 li > h3 >a'):
            yield response.follow(href, callback=self.content_parse)

        next_page = response.css('ul.pagelist li:nth-last-child(2)>a::attr(href)').get()
        if next_page is not None:
            for href in response.css('ul.list2 li > h3 >a'):
                yield response.follow(href, callback=self.content_parse)

    def content_parse(self, response):
        content_text = response.css('div.g_con div.con p::text').extract()
        yield {
            'content': content_text
        }
