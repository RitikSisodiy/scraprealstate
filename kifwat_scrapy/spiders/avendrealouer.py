import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AvendrealouerSpider(CrawlSpider):
    name = 'avendrealouer'
    start_urls = [
        'https://www.avendrealouer.fr/recherche.html?pageIndex=1&sortPropertyName=ReleaseDate&sortDirection=Descending&searchTypeID=1&typeGroupCategoryID=1&localityIds=2-11&typeGroupIds=1,2,10,11,12#o=Home'
    ]
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'FEEDS': {
            'netvendeur.csv': {
                'format': 'csv',
                'fields': []
            }
        },
        'DUPEFILTER_CLASS': 'kifwat_scrapy.middlewares.CustomFilter',
        'USER_AGENT': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }

    rules = (
        Rule(LinkExtractor(restrict_css='#result-list a.linkToFd'), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='.pagination .pageNumber'), callback='_parse'),
    )

    def parse_item(self, response):
        return {
            'title': response.css('[class*=dHead] h1::text').extract_first(),
            'price': ''.join(re.findall('\d', response.css('[class*=dValue]::text').extract_first())),
            **{p.css('::text').extract_first().lower(): p.css('span::text').extract_first() for p in response.css('[class*=dInformations] p')},
            'ville': response.css('[class*=dCity]::text').extract_first(),
            'agency name': response.css('[class*=dName]::text').extract_first(),
            'description': response.css('[class*="Professional__PStyled"]::text').extract_first(),
            'url': response.css('[class*="dImg"] img::attr(src)').extract_first()
        }
