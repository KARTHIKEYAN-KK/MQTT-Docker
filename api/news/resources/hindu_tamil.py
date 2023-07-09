from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import json, request

import feedparser
import requests
from bs4 import BeautifulSoup
import re

rss_url="http://feeds.feedburner.com/Hindu_Tamil_tamilnadu"

blp = Blueprint("Tamil Hindu News API", __name__, description="Latest News of Tamil Nadu")


def extract_text_from_html(html_content):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', html_content)
    clean_text = clean_text.replace('\n\n', ' ')
    return clean_text.strip()

def extract_image_url(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tag = soup.find('img')
    if img_tag:
        img_url = img_tag['src']
        return img_url
    return None

@blp.route("/tamil/news/tamil_nadu")
class TamilNaduNews(MethodView):
    def get(self):
        feed = feedparser.parse(rss_url)
        items = feed.entries

        rss_data = []
        for item in items:
            content = item.content[0].value
            image_url = extract_image_url(content)
            clean_content = extract_text_from_html(content)

            rss_item = {
                'title': item.title,
                'link': item.link,
                'description': item.description,
                'published_date': item.published,
                'modified_date': item.updated,
                'author': item.author,
                'content': clean_content,
                'image_url': image_url
            }
            rss_data.append(rss_item)

        return rss_data