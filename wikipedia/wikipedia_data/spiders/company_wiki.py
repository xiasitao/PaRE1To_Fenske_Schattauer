import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from ..items import PageData
 
import datetime
from time import sleep


class CompanyWikiSpider(scrapy.Spider):
    name = 'company_wiki'
    allowed_domains = ['www.wikipedia.org']

    def start_requests(self):
        start_url = 'https://en.wikipedia.org/w/index.php?title=List_of_S%26P_500_companies&offset=&limit=2500&action=history'
        yield scrapy.Request(url=start_url, callback=self.parse_version_history)

    def parse_version_history(self, response):
        list_items = response.xpath('//ul[@id="pagehistory"]//li')
        for item in list_items:
            time = item.xpath('normalize-space(.//a[@class="mw-changeslist-date"]//text())').get()
            next_page = item.xpath('normalize-space(.//a[@class="mw-changeslist-date"]//@href)').get()
            
            time = datetime.datetime.strptime(time, '%H:%M, %d %B %Y')

            if next_page is not None:
                next_page = response.urljoin(next_page)
                print(next_page, '   ', time)
                content = get_html(next_page)
                yield scrapy.Request(next_page, callback=self.parse_wikipage, meta={'time': time, 'content': content},dont_filter=True)

    def parse_wikipage(self, response):
        time = response.meta['time']
        response = Selector(text=response.meta['content'])

        table = response.xpath('//table[contains(@class,"wikitable")][1]//tbody//tr')
        info_one = response.xpath('normalize-space(//table[contains(@class,"wikitable")][1]//thead//tr//th[1]/a/text())').get()
        #info_two = response.xpath('normalize-space(//table[contains(@class,"wikitable")][1]//thead//tr//th[2]/text())').get()

        if ('symbol' or 'ticker') in info_one.lower():
            ticker = 1
            security = 2
        else:
            ticker = 2
            security = 1
        
        loader = ItemLoader(item=PageData(), selector=table, response=response)
        data = []
        for i in range(1, len(table)):
            dd = {}
            row = table[i]
            dd['ticker'] = row.xpath(f'normalize-space(.//td[{ticker}]//text())').get()
            dd['security'] = row.xpath(f'normalize-space(.//td[{security}]//text())').get()
            data.append(dd)
        loader.add_value('pagedata', data)
        loader.add_value('date', time)
        yield loader.load_item()

###helper functions
def start_chrome():
    from shutil import which
    from selenium import webdriver
    from fake_useragent import UserAgent
    ua = UserAgent()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    
    chrome_options.add_argument(f'user-agent={ua.random}')#need to restart this every few requests
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    prefs = {"plugins.plugins_disabled" : ["Chrome PDF Viewer"], 'intl.accept_languages': 'de_DE,de'}
    chrome_options.add_experimental_option("prefs",prefs)
    
    chrome_path = which('chromedriver')
    driver = webdriver.Chrome(chrome_path, options=chrome_options)
    #comment this out on PI
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })"""})
    driver.delete_all_cookies()
    return driver

def get_html(href: str) -> str:
    
    driver = start_chrome()
    driver.get(href)
    sleep(3)
    pagehtml = driver.page_source
    sleep(2)
    driver.quit()
    return pagehtml
    #except Exception:
    #    return None