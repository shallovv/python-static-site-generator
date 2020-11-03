import markdown
import string
import os
from datetime import datetime, timezone, timedelta


OUTPUT_PATH = 'output/'
ARTICLE_PATH = 'articles/'
HTML = '''\
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <link href="/css/main.css" rel="stylesheet" type="text/css">
    <link href="$url" rel="canonical">
    <title>記事一覧</title>
</head>
<body>
    <header>
        <a href="/">$sitename</a>
        <a href="/articles">記事一覧</a>
        <a href="https://www.google.com/search?q=site:$url">検索</a>
    </header>
    <main>
        <header>
            <h1>記事一覧</h1>
        </header>
        <section>
            <ul>
$article_list
            </ul>
        </section>
    </main>
</body>
</html>
'''


ARTICLES = '''\
<li>
    <time datetime="$date">$dateja</time>
    <a href="$path">$title</a>
</li>
'''


class ArticleList:
    def __init__(self, url, sitename):
        self.name = 'articles'
        self.url = url
        self.sitename = sitename

    def convertHTML(self):
        articles = [i.replace(ARTICLE_PATH, '').replace('.md', '') for i in os.listdir(ARTICLE_PATH)][::-1]
        articles = sorted(articles, reverse=True)
        article_list = ''
        for i in articles:
            with open(ARTICLE_PATH + i + '.md', mode='r', encoding='utf_8') as f:
                text = f.read()
            md = markdown.Markdown(extensions=['meta'])
            md.convert(text)
            title = str(md.Meta['title'][0]).replace('"', '')
            year, month, day = map(int, str(md.Meta['date'][0]).split('-'))
            jst = timezone(timedelta(hours=+9), 'JST')
            date = datetime(year, month, day, tzinfo=jst).isoformat()
            dateja = str(year) + '年' + str(month) + '月' + str(day) + '日'
            context = {
                'date': date,
                'dateja': dateja,
                'path': ARTICLE_PATH + i,
                'title': title
            }
            template = string.Template(ARTICLES)
            article_list += template.substitute(context)
        url = self.url + '/' + self.name
        sitename = self.sitename
        context = {
            'url': url,
            'sitename': sitename,
            'article_list': article_list
        }
        template = string.Template(HTML)
        html = template.substitute(context)
        with open(OUTPUT_PATH + self.name + '.html', mode='w', encoding='utf_8') as f:
            f.write(html)
