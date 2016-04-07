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
			'http://kutv.com/news/local.rss',
			'http://www.ksl.com/xml/148.rss',
			'http://fox13now.com/category/news/feed/',
			'http://kpcw.org/feeds/term/22/rss.xml',
			'http://www.sltrib.com/rss/feed/?sec=/News/&level=0',
			'http://www.deseretnews.com/utah/index.rss',
			'http://www.standard.net/rss/local',
			'http://www.heraldextra.com/search/?f=rss&t=article&c=news/local*&l=25&s=start_time&sd=desc',
			'http://news.hjnews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.richfieldreaper.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://gaysaltlake.com/feed/',
			'http://www.cityweekly.net/utah/Rss.xml?category=2124970',
			'http://www.suunews.com/rss/headlines/',
			'http://tooeleonline.com/feed/',
			'http://www.stgeorgeutah.com/news/archive/category/news/local/feed',
			'http://rssfeeds.thespectrum.com/stgeorge/news&x=1',
			'http://servedaily.com/feed/',
			# 'http://www.morgancountynews.net/todaysnews/rss.xml'
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
			location = "UT"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			