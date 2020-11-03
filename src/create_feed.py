import feedgenerator
import markdown
import os
from datetime import datetime, timezone, timedelta


OUTPUT_PATH = 'output/'
ARTICLE_PATH = 'articles/'


class Feed:
    def __init__(self, url, sitename):
        self.name = 'feed'
        self.url = url
        self.sitename = sitename

    def createFeed(self):
        feed = feedgenerator.Atom1Feed(title=self.sitename, link=self.url, description='')
        articles = [i.replace(ARTICLE_PATH, '').replace('.md', '') for i in os.listdir(ARTICLE_PATH)]
        articles = sorted(articles, reverse=True)
        for i in articles:
            with open(ARTICLE_PATH + i + '.md', mode='r', encoding='utf_8') as f:
                text = f.read()
            md = markdown.Markdown(extensions=['meta'])
            md.convert(text)
            title = str(md.Meta['title'][0]).replace('"', '')
            link = self.url + '/' + ARTICLE_PATH + i
            year, month, day = map(int, str(md.Meta['date'][0]).split('-'))
            jst = timezone(timedelta(hours=+9), 'JST')
            date = datetime(year, month, day, tzinfo=jst)
            feed.add_item(title=title, link=link, description='', pubdate=date)
        with open(OUTPUT_PATH + self.name + '.xml', mode='w', encoding='utf_8') as f:
            f.write(feed.writeString('utf_8'))
