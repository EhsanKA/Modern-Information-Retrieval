import scrapy
from scrapy.exceptions import CloseSpider


class QuotesSpider(scrapy.Spider):
    name = "scholar"
    limit = 2000
    counter =0
    urls= []
    start_urls = [
            'https://www.semanticscholar.org/paper/Coordinated-actor-model-of-self-adaptive-traffic-Bagheri-Sirjani/45ee43eb193409c96107c5aa76e8668a62312ee8',
            'https://www.semanticscholar.org/paper/Automatic-Access-Control-Based-on-Face-and-Hand-in-Jahromi-Bonderup/2199cb39adbf22b2161cd4f65662e4a152885bae',
            'https://www.semanticscholar.org/paper/Fair-Allocation-of-Indivisible-Goods%3A-Improvement-Ghodsi-Hajiaghayi/03d557598397d14727803987982c749fbfe1704b',
            'https://www.semanticscholar.org/paper/Restoring-highly-corrupted-images-by-impulse-noise-Taherkhani-Jamzad/637cf5540c0fb1492d94292bf965b2c404e42fb4',
            'https://www.semanticscholar.org/paper/Domino-Temporal-Data-Prefetcher-Bakhshalipour-Lotfi-Kamran/665c0dde22c2f8598869d690d59c9b6d84b07c01',
            'https://www.semanticscholar.org/paper/Deep-Private-Feature-Extraction-Ossia-Taheri/3355aff37b5e4ba40fc689119fb48d403be288be',
        ]

    def parse(self, response):
        self.counter += 1
        if self.counter > self.limit:
            raise CloseSpider()

        self.log("Crawling Counter = " + str(self.counter))
        self.log("Crawling Limit = " + str(self.limit))

        res = response.xpath('//div[@id="references"]/div[@class="card-content"]/div/article/div/div[@class="result-meta"]/a/@href').extract()
        ids = [ (item.split("/")[-2]+item.split("/")[-1]) for item in res]
        refs = []
        for url in res:
            refs.append(response.urljoin(url))

        url_parts = response.url.split('/')

        yield {
        	# "type": "paper",
        	"id": url_parts[-2]+ url_parts[-1],
        	"title": response.xpath('//div[@id="paper-header"]/h1/text()').extract_first(),
        	"authors": response.xpath('/html/body/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div/ul/li[1]/span/span/a/span/span/text()').extract(),
        	"date": response.xpath('//span[@data-selenium-selector="paper-year"]/span/span/text()').extract_first(),
        	"abstract": response.xpath('//div[@class="fresh-paper-detail-page__abstract"]/div/text()').extract_first(),
        	"references": ids[:10]
        }
        for url in refs[:5]:
            if url in self.urls:
                continue
            else:
                self.urls.append(url)
                yield scrapy.Request(url=url, callback=self.parse)
