import os
import shutil
from dotenv import load_dotenv
from src import create_top_article
from src import create_article
from src import create_article_list
from src import create_feed
from src import create_sitemap


load_dotenv()


OUTPUT_PATH = 'output/'
ARTICLE_PATH = 'articles/'
STATIC_PATH = 'static/'
SITENAME = os.environ['SITENAME']
URL = os.environ['URL']


# remove output dir
if os.path.isdir(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)
    os.mkdir(OUTPUT_PATH)
else:
    os.mkdir(OUTPUT_PATH)


# create articles
os.mkdir(OUTPUT_PATH + ARTICLE_PATH)
articles = [i.replace(ARTICLE_PATH, '').replace('.md', '') for i in os.listdir(ARTICLE_PATH)]
for i in articles:
    article = create_article.Article(i, URL, SITENAME)
    article.convertHTML()


# create top page
top_article = create_top_article.TopArticle(URL, SITENAME)
top_article.convertHTML()


# create article list
article_list = create_article_list.ArticleList(URL, SITENAME)
article_list.convertHTML()


# copy static file
shutil.copytree(STATIC_PATH + 'css/', OUTPUT_PATH + 'css/')


# crate feed
feed = create_feed.Feed(URL, SITENAME)
feed.createFeed()

# create sitemap
sitemap = create_sitemap.Sitemap(URL)
sitemap.createSitemap()
