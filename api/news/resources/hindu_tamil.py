import feedparser
import requests
from bs4 import BeautifulSoup
import re

rss_url="http://feeds.feedburner.com/Hindu_Tamil_tamilnadu"

blp = Blueprint("Tamil Hindu News API", __name__, description="Latest News of Tamil Nadu")

@blp.route("/tamil/news/tamil_nadu")
class TamilNaduNews(MethodView):
    def get(self):
        feed = feedparser.parse(rss_url)
        items = feed.entries

        rss_data = []
        for item in items:
            rss_item = RSSItem(
                title=item.title,
                link=item.link,
                description=item.description,
                published_date=item.published,
                modified_date=item.updated,
                author=item.author,
                content=item.content[0].value
            )
            rss_data.append(rss_item.serialize())

        return rss_data