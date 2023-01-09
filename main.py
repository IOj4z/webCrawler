from lib2to3.pgen2.grammar import line
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import requests
import random


class Content:
    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):
        print('New article found for topic:{}'.format(self.topic))
        print('URL: {}'.format(self.url))
        print('TITLE: {}'.format(self.title))
        print('BODY:\n{}'.format(self.body))


class Website:
    def __init__(self, name, url, searchUrl, resultListing, resultUrl, absoluteUrl, titleTag, bodyTag):
        self.name = name
        self.url = url
        self.searchUrl = searchUrl
        self.resultListing = resultListing
        self.resultUrl = resultUrl
        self.absoluteUrl = absoluteUrl
        self.titleTag = titleTag
        self.bodyTag = bodyTag


class Crawler:
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None

        return BeautifulSoup(req.text, 'html.parser')

    def safeGet(self, pageObj, selector):
        childObj = pageObj.select(selector)
        if childObj is not None and len(childObj) > 0:
            return childObj[0].get_text()
        selectedElems = pageObj.select(selector)
        if selectedElems is not None and len(selectedElems) > 0:
            return '\n'.join([elem.get_text() for elem in selectedElems])
        return ''

    def search(self, topic, site):
        bs = self.getPage(site.searchUrl + topic)
        searchResults = bs.select(site.resultListing)

        for result in searchResults:
            url = ''
            if site.absoluteUrl:
                url = result.select(site.resultUrl)
                # print(url)
                bs = self.getPage(url[0].attrs['href'])
            else:
                bs = self.getPage(site.url + url)
            #
            if bs is None:
                print('Something was wrong with that page or URL.Skipping!')
                return
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(topic, title, body, url)
                content.print()

    def parse(self, site, url):
        bs = self.getPage(url)
        if bs is not None:
            title = self.safeGet(bs, site.titleTag)
            body = self.safeGet(bs, site.bodyTag)
            if title != '' and body != '':
                content = Content(url, title, body)
                content.print()


crawler = Crawler()
siteData = [
    ['O\'Reilly Media', 'http://oreilly.com',
     'https://ssearch.oreilly.com/?q=',
     'article.product-result', 'p.title a',
     True, 'h1',
     'section#product-description'],

    ['Reuters', 'http://reuters.com',
     'http://www.reuters.com/search/news?blob=',
     'div.search-result-content', 'h3.searchresult-title a', False, 'h1',
     'div.StandardArticleBody_body_1gnLA'],

    ['Brookings', 'http://www.brookings.edu',
     'https://www.brookings.edu/search/?s=',
     'div.list-content article',
     'h4.title a', True, 'h1', 'div.post-body']
]
sites = []
for row in siteData:
    sites.append(Website(row[0], row[1], row[2], row[3], row[4],
                         row[5], row[6], row[7]))
topics = ['python', 'data science']
for topic in topics:
    print('GETTING INFO ABOUT: ' + topic)
    for targetSite in sites:
        crawler.search(topic, targetSite)

# crawler.parse(websites[0],
#               'http://shop.oreilly.com/product/0636920028154.do')
# crawler.parse(websites[1],
#               'http://www.reuters.com/article/us-usa-epa-pruitt-idUSKBN19W2D0')
# crawler.parse(websites[2],
#               'https://www.brookings.edu/blog/techtank/2016/03/01/idea-to-retire-oldmethods-of-policy-education/')
# crawler.parse(websites[3],
#               'https://www.nytimes.com/2018/01/28/business/energy-environment/oilboom.html')

#
#
# def scrapeNYTimes(url):
#     bs = getPage(url)
#     title = bs.find('h1')
#     lines = bs.select('div.StoryBodyCompanionColumn div p')
#     body = '\n'.join([line.text for line in lines])
#
#     return Content(url, title, body)
#
#
# def scrapeBrookings(url):
#     bs = getPage(url)
#     title = bs.find('h1').text
#     body = bs.find('div', {'class', 'post-body'}).text
#     return Content(url, title, body)
#
#
# url = 'https://www.brookings.edu/blog/futuredevelopment/2018/01/26/delivering-inclusive-urban-access-3-uncomfortable' \
#       '-truths/ '
# content = scrapeBrookings(url)
# print('Title: {}'.format(content.title))
# print('URL: {}\n'.format(content.url))
# print(content.body)
#
# url = 'https://www.nytimes.com/2018/01/25/opinion/sunday/silicon-valley-immortality.html'
# content = scrapeNYTimes(url)
# print('Title: {}'.format(content.title))
# print('URL: {}\n'.format(content.url))
# print(content.body)
