import markdown
import string
from datetime import datetime, timezone, timedelta


OUTPUT_PATH = 'output/'
ARTICLE_PATH = 'articles/'
HTML = '''\
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width">
    <link href="/css/main.css" rel="stylesheet">
    <link href="$url" rel="canonical">
    <title>$title</title>
</head>
<body>
    <header>
        <a href="/">$sitename</a>
        <a href="/articles">記事一覧</a>
        <a href="https://www.google.com/search?q=site:$url">検索</a>
    </header>
    <main>
        <header>
            <h1>$title</h1>
            <time datetime="$date">$dateja</time>
        </header>
        <section>
$contents
        </section>
    </main>
</body>
</html>
'''


class Article:
    def __init__(self, name, url, sitename):
        self.name = name
        self.url = url
        self.sitename = sitename

    def convertHTML(self):
        with open(ARTICLE_PATH + self.name + '.md', mode='r', encoding='utf_8') as f:
            text = f.read()
        md = markdown.Markdown(extensions=['meta', 'fenced_code'])
        contents = md.convert(text)
        url = self.url + '/' + ARTICLE_PATH + self.name
        sitename = self.sitename
        title = str(md.Meta['title'][0]).replace('"', '')
        year, month, day = map(int, str(md.Meta['date'][0]).split('-'))
        jst = timezone(timedelta(hours=+9), 'JST')
        date = datetime(year, month, day, tzinfo=jst).isoformat()
        dateja = str(year) + '年' + str(month) + '月' + str(day) + '日'
        context = {
            'url': url,
            'sitename': sitename,
            'title': title,
            'date': date,
            'dateja': dateja,
            'contents': contents
        }
        template = string.Template(HTML)
        html = template.substitute(context)
        with open(OUTPUT_PATH + ARTICLE_PATH + self.name + '.html', mode='w', encoding='utf_8') as f:
            f.write(html)
