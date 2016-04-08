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
			'http://feeds.feedburner.com/Kobcom-Home?format=xml',
			'http://krwg.org/feeds/term/9/rss.xml',
			'http://krqe.com/category/news/feed/',
			'http://www.koat.com/9154706?format=rss_2.0&view=feed',
			'http://www.770kkob.com/category/770-news/feed/',
			'http://www.cnjonline.com/news/feed/',
			'http://www.dchieftain.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://feeds.feedblitz.com/farmington/news&x=1',
			'http://lascrucesbulletin.com/site/feed/',
			'https://feeds.feedblitz.com/lascruces/news',
			# remove 'http://www.lamonitor.com/todaysnews/rss.xml',
			'http://www.themountainmail.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.riograndesun.com/?rss=news',
			'http://rdrnews.com/wordpress/blog/category/news/local-news/feed/',
			'http://feeds.feedblitz.com/ruidoso/news&x=1',
			'https://sangrechronicle.com/category/news/feed/',
			'http://www.qcsunonline.com/category/news/feed/',
			'http://www.scdailypress.com/site/feed/',
			'https://feeds.feedblitz.com/silvercity/news&x=1',
			'http://www.news-bulletin.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.cibolabeacon.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://feeds.feedblitz.com/alamogordo/news&x=1',
			'http://www.abqjournal.com/feed',
			'https://www.artesianews.com/category/artesia-news/local-news/feed',
			'http://feeds.feedblitz.com/carlsbad/news&x=1',
			
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
			location = "NM"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			