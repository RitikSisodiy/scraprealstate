import re

from scrapy import FormRequest
from scrapy.spiders import CrawlSpider
from w3lib.url import add_or_replace_parameter


def clean(str_or_lst):
    if isinstance(str_or_lst, list):
        data = [clean(x) for x in str_or_lst]
        return [x for x in data if x]
    return re.sub('\s+', ' ', str_or_lst).strip()


class SwissSpider(CrawlSpider):
    name = 'reg_entreprises'
    start_urls = [
        'https://www.registre-entreprises.tn/'
    ]
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'FEEDS': {
            'registre_entreprises.csv': {
                'format': 'csv',
                'fields': [
                    'unique identifier', 'Legal form', 'State of the register', 'Tax situation',
                    'Company name', 'Trade name', 'address',

                    'المعرف الوحيد', 'الوضع القانوني', 'حالة السجل التجاري', 'الوضعية الجبائية',
                    'الاسم الجماعي', 'الإسم التجاري للشركة', 'المقر الإجتماعي',
                ],
            },
        },
        'DUPEFILTER_CLASS': 'kifwat_scrapy.middlewares.CustomFilter',
        'USER_AGENT': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }

    priorities = {
        'set_year': 2,
        'year': 4,
        'backtolist': 6,
        'page': 6,
        'product': 8,
    }

    seen_pages = {}

    def start_requests(self):
        for req in super().start_requests():
            yield req.replace(meta={'dont_merge_cookies': True})

    def parse_start_url(self, response, **kwargs):
        yield response.follow(
            'https://www.registre-entreprises.tn/search/RCCSearch.do?action=getPage&rg_type=PM&search_mode=NORMAL',
            meta={'dont_merge_cookies': True},
            callback=self.parse_year
        )

    def parse_year(self, response):
        # This request is to the same page url but for a different session for every year
        for index, year in enumerate(
                response.css('[name="searchRegistrePmRcc.registrePm.demande.anneeInsertion"] option::text').extract()):
            yield response.request.replace(
                priority=self.priorities['set_year'],
                meta={
                    'year': year,
                    'dont_merge_cookies': True,
                    'cookiejar': index,
                },
                callback=self.parse_navigation
            )

    def parse_navigation(self, response):
        req = FormRequest.from_response(
            response,
            formname='rCCSearchForm',
            formdata={
                'searchRegistrePmRcc.registrePm.demande.anneeInsertion': response.meta['year']
            },
            priority=self.priorities['year'],
            meta={
                'cookiejar': response.meta['cookiejar'],
            },
            callback=self.parse_page
        )
        yield req.replace(url=req.url + '?action=search')

    def parse_page(self, response):
        self.seen_pages.setdefault(response.meta['cookiejar'], set('1'))
        req = FormRequest.from_response(response, formname='rCCSearchForm')

        jsession = re.findall(';jsessionid=([^?&]+)', response.url)
        if jsession:
            response.meta.update({'jsession': jsession[0]})

        for index in response.xpath('//tr[contains(@onclick, "choixDocuments")]').re('choixDocuments\((.*?)\)'):
            yield req.replace(
                url=req.url + f'?action=chooseDocuments&numRegistreIndex={index}',
                priority=self.priorities['product'],
                meta={
                    'cookiejar': response.meta['cookiejar']
                },
                callback=self.parse_company
            )

        yield req.replace(
            url=add_or_replace_parameter(req.url, 'action', 'backToList'),
            priority=self.priorities['backtolist'],
            dont_filter=True,
            meta={
                'cookiejar': response.meta['cookiejar'],
                'jsession': response.meta['jsession'],
            },
            callback=self.parse_pages
        )

    def parse_pages(self, response):
        cookiejar = response.meta['cookiejar']
        jsession = re.findall(
            ';jsessionid=([^?&]+)', response.request.url if 'jsession' in response.request.url else response.url)

        jsession = jsession[0] if jsession else response.meta['jsession']

        for page in clean(response.css('.PagNum ::text').extract()):
            if page not in self.seen_pages[cookiejar]:
                self.seen_pages[cookiejar].add(page)

                yield response.follow(
                    response.css(f'.PagNum a[href*="page={page}"]')[0],
                    cookies={
                        'JSESSIONID': jsession
                    },
                    priority=self.priorities['page'],
                    meta={
                        'cookiejar': cookiejar,
                        'jsession': jsession
                    },
                    callback=self.parse_page,
                )
                break

    def parse_company(self, response):
        return {
            'unique identifier': self.get_second_td(response, 'Identifiant unique'),
            'Legal form': self.get_second_td(response, 'Forme juridique'),
            'State of the register': self.get_second_td(response, 'Etat du registre'),
            'Tax situation': self.get_tax(response, 'Situation Fiscale'),
            'Company name': self.get_second_td(response, 'Dénomination sociale'),
            'Trade name': self.get_second_td(response, 'Nom Commercial'),
            'address': self.get_second_td(response, 'Adresse du Siège'),

            'المعرف الوحيد': self.get_last_td(response, 'المعرف الوحيد'),
            'الوضع القانوني': self.get_last_td(response, 'الوضع القانوني'),
            'حالة السجل التجاري': self.get_last_td(response, 'حالة السجل التجاري'),
            'الوضعية الجبائية': self.get_tax(response, 'الوضعية الجبائية', -1),
            'الاسم الجماعي': self.get_last_td(response, 'الاسم الجماعي'),
            'الإسم التجاري للشركة': self.get_last_td(response, 'الإسم التجاري للشركة'),
            'المقر الإجتماعي': self.get_last_td(response, 'المقر الإجتماعي'),
        }

    def get_second_td(self, response, column_name):
        return clean(response.xpath(
            f'//tr[td[contains(., "{column_name}")]]/td[@class="Inn-06-black"]//text()'
        ).extract_first() or '')

    def get_last_td(self, response, column_name):
        return clean(response.xpath(
            f'//tr[td[contains(., "{column_name}")]]/td[@class="Inn-06-black"]//text()'
        )[-1].extract())

    def get_tax(self, response, key, index=0):
        tax_situation = clean(response.xpath(
            f'//table[contains(@class, "search-result")]//td[contains(.,"{key}")]//text()'
        ).extract())[1:]

        tax_situation = " ".join(tax_situation)

        if index == -1:
            return f'{tax_situation} {self.get_last_td(response, key)}'

        return f'{tax_situation} {self.get_second_td(response, key)}'
