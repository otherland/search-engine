import datetime
import pickle
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_absolute(url):
    return bool(urlparse(url).netloc)

class Crawler:
    def __init__(self, seed_url):
        self.to_crawl = set([seed_url])
        self.crawled = set()
        self.store = dict()
        self.max_links = 20

    def can_crawl(self):
        return self.to_crawl and len(self.crawled) <= self.max_links

    def get_html(self, url):
        try:
            response = requests.head(url)
            response.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
            print(err)
            # Write code to store error with url

        if not "text/html" in response.headers["content-type"]:
            return False

        try:
            response = requests.get(url)
            response.raise_for_status()
            html = response.text
            return html
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
            print(err)
            return False


    def get_links(self, seed_url, soup):
        links = soup.find_all('a')
        urls = list()

        for link in links:
            url = link.get('href', False)
            if url == False:
                continue
            if not is_absolute(url):
                url = urljoin(seed_url, url)
            # Default scheme
            url = urlparse(url, scheme='http').geturl()
            # Remove params
            url = urljoin(url, urlparse(url).path)
            if url not in self.crawled:
                urls.append(url)

        if urls:
            print("Found {} urls.".format(len(urls)))
        return urls

    def queue_links(self, links):
        links = list(reversed(links))
        self.to_crawl = self.to_crawl.union(links)

    def serialize_html(self, url, html):
        data = dict()
        soup = BeautifulSoup(html, 'html.parser')
        links = self.get_links(url, soup)
        self.queue_links(links)

        data['url'] = url
        # data['html'] = html
        data['text'] = soup.text
        data['links'] = links
        data['title'] = getattr(soup.title, "text", "").strip()
        data['date_time'] = datetime.datetime.now()
        return data

    def store_data(self, url, data):
        self.store.update({
            url: data
        })

    def crawl(self):
        print("Starting crawl...")

        while self.can_crawl():
            url = self.to_crawl.pop()
            print("Crawling: {}".format(url))
            html = self.get_html(url)
            if html == False:
                continue
            data = self.serialize_html(url, html)
            self.crawled = self.crawled.union([url])
            self.store_data(url, data)
            from IPython import embed; embed();

        with open('crawler.pickle', 'wb') as file:
            pickle.dump(self.store, file)

        print("Finished crawling.")

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
    CR = Crawler(seed_url=url)
    CR.crawl()


















