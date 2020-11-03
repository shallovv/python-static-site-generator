import os

OUTPUT_PATH = 'output/'
ARTICLE_PATH = 'articles/'


class Sitemap:
    def __init__(self, url):
        self.name = 'sitemap'
        self.url = url

    def createSitemap(self):
        articles = [i.replace('.md', '') for i in os.listdir(ARTICLE_PATH)]
        articles = sorted(articles, reverse=True)
        sitemap = ''
        for i in articles:
            url = self.url + '/' + i + '\n'
            sitemap += url
        with open(OUTPUT_PATH + self.name + '.txt', mode='w', encoding='utf_8') as f:
            f.write(sitemap)
