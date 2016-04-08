#!/usr/bin/env python
import os
import feedparser
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
with psycopg2.connect(database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port) as dbconnect:
	cur = dbconnect.cursor()

	url = (
			'http://www.nbcwashington.com/news/local/?rss=y&embedThumb=y&summary=y',
			'http://wjla.com/news/local.rss',
			'http://rssfeeds.wusa9.com/wusa-news&x=1',
			'http://dcw50.com/category/news/feed/',
			'http://feeds.feedburner.com/WAMU885LocalNews',
			'http://woldcnews.newsone.com/category/dcnews/feed/',
			'http://thehill.com/rss/syndicator/19109',
			'http://feeds.washingtonpost.com/rss/rss_express',
			# 'http://www.politico.com/rss/politicopicks.xml',
			'http://feeds.washingtonpost.com/rss/local',
			'http://www.washingtontimes.com/rss/headlines/news/local/',
			'http://www.thehoya.com/category/news/feed/',
			'http://www.gwhatchet.com/news/feed/',
			'http://georgetownvoice.com/section/news/feed/',
			'http://www.washingtonexaminer.com/rss/politics',
			'http://www.washdiplomat.com/index.php?format=feed&type=rss',
			'http://www.washingtonblade.com/category/news/local-news/feed/',
			'http://eltiempolatino.com/rss/headlines/',
			'http://www.cathstan.org/RSS/2',
			'http://www.elpreg.org/RSS/4'

			)

	for link in url:
		d = feedparser.parse(link)

		for data in d.entries:


			title = data.title
			link = data.link
			try:
				time = data.published
			except AttributeError:
				try:
					time = d.feed.published
				except AttributeError:
					time = data.updated

			try: 
				imageUrl = data.links[1].href
			except (IndexError, AttributeError): 
				try:
					imageUrl = data.media_content[0]['url']
				except (AttributeError, KeyError):
					imageUrl = 'http://polar-spire-13485.herokuapp.com/static/img/logo3.png'

			source = d.feed.title
			location = "DC"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			