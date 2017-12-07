import scrapy
import re
import json

from tedtranscripts.items import TedTranscript

class TedSpider(scrapy.Spider):
    name = 'TedSpider'
    seed_url = 'https://www.ted.com/talks?sort=newest&page=1'
    lang_pttrn = re.compile('.*language=([a-z]{2})(&.*)?$')
    id_pttrn = re.compile('.*ted\.com/talks/([^/]*).*')

    def __init__(self, lang=None, talks=None, *args, **kwargs):
        super(TedSpider, self).__init__(*args, **kwargs)
        if not lang:
            raise Exception("Language should be specified. For example:\n -a lang=kn\n -a lang=en")
        self.lang = lang
        self.talks = None
        if talks:
            self.talks = set()
            with open(talks) as f:
                new_lang = 'language=%s' % lang
                for line in f:
                    url = json.loads(line)['url']
                    new_url = re.sub(r'language=[a-z]{2}', new_lang, url)
                    self.talks.add(new_url)
            self.logger.info("Found %d talks from the specified file %s", len(self.talks), talks)

    def start_requests(self):
        if self.talks is not None:
            self.logger.info("Focused crawl based on previous crawl output")
            for talk_url in self.talks:
                yield scrapy.Request(talk_url, callback=self.parse_talk_transcript)
        else:
            self.logger.info("Crawling all talks of language %s ", self.lang)
            browse_url = TedSpider.seed_url + "&language=%s" % self.lang
            yield scrapy.Request(browse_url, callback=self.parse_talks)

    def parse_talks(self, response):
        self.logger.info('Parse: %s', response.url)

        # go to the actual talk page
        urls = response.xpath('//a[@data-ga-context="talks"]/@href').extract()
        for url in urls:
            if '?' in url:
                url = url.replace("?", "//transcript?")
            else:
                print("SKIPPED:", url)
                continue
            yield response.follow(url, callback=self.parse_talk_transcript)

        # go to the next page
        next_urls = response.xpath('//a[@rel="next"]/@href')
        if next_urls:
            yield response.follow(next_urls[0], callback=self.parse)

    def parse_lang(self, url):
        match = TedSpider.lang_pttrn.match(url)
        return match.groups()[0] if match else None

    def parse_id(self, url):
        match = TedSpider.id_pttrn.match(url)
        return match.groups()[0] if match else None

    def parse_talk_transcript(self, response):
        url = response.url
        self.logger.info("Parse Talk Transcript:: %s", url)
        fragments = response.xpath('''//span[contains(@class, 'talk-transcript__fragment') and @data-time]''')

        item = TedTranscript()
        item['url'] = url
        item['id'] = self.parse_id(url)
        item['lang'] = self.parse_lang(url)
        item['data'] = {}
        for fragment in fragments:
            marker = int(fragment.xpath('./@data-time').extract()[0].strip())
            text = fragment.xpath('./text()').extract()[0].strip()
            item['data'][marker] = text

        return item
