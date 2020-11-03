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
    <link href="$root/css/main.css" rel="stylesheet" type="text/css">
    <link href="$url" rel="canonical">
    <title>$sitename</title>
</head>
<body>
    <header>
        <a href="$root/">$sitename</a>
        <a href="$root/articles">記事一覧</a>
        <a href="https://www.google.com/search?q=site:$url">検索</a>
    </header>
    <main>
        <section>
            <h2>最近の記事</h2>
            <ul>
$recent
            </ul>
        </section>
        <section>
            <h2>リンク</h2>
            <dl>
                <dt><a href="$root/feed.xml">Feed</a></dt>
                <dd>更新情報をRSSで配信しています</dd>
            </dl?
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


class TopArticle:
    def __init__(self, url, root, sitename):
        self.name = 'index'
        self.url = url
        self.root = root
        self.sitename = sitename

    def convertHTML(self):
        articles = [i.replace(ARTICLE_PATH, '').replace('.md', '') for i in os.listdir(ARTICLE_PATH)]
        recent_5_articles = sorted(articles, reverse=True)[:5]
        recent = ''
        for i in recent_5_articles:
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
            recent += template.substitute(context)
        url = self.url
        root = self.root
        sitename = self.sitename
        context = {
            'url': url,
            'root': root,
            'sitename': sitename,
            'recent': recent
        }
        template = string.Template(HTML)
        html = template.substitute(context)
        with open(OUTPUT_PATH + self.name + '.html', mode='w', encoding='utf_8') as f:
            f.write(html)
