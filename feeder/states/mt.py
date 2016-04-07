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
			'http://www.kulr8.com/category/262588/local?clienttype=rss',
			'http://www.ktvq.com/category/288947/news?clienttype=rss',
			'http://www.kbzk.com/category/289025/news?clienttype=rss',
			'http://www.kxlf.com/category/288921/news?clienttype=rss',
			'http://www.nbcmontana.com/15193794?format=rss_2.0&view=feed',
			'http://www.abcfoxmontana.com/category/262488/rss-feeds?clienttype=rss',
			'http://www.krtv.com/category/288973/news?clienttype=rss',
			'http://www.kxlh.com/category/288908/news?clienttype=rss',
			'http://www.kpax.com/category/288999/news?clienttype=rss',
			'http://www.kfbb.com/category/262741/rss-feeds?clienttype=rss',
			'http://www.ktvh.com/category/news/feed/',
			'http://newstalk955.com/category/local-news-2/feed/',
			'http://newstalkkgvo.com/feed/',
			'http://klyq.com/category/local-news/feed/',
			'http://kmmsam.com/feed/',
			'http://www.belgrade-news.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://billingsgazette.com/search/?f=rss&t=article&c=news/local*&l=25&s=start_time&sd=desc',
			'http://www.bozemandailychronicle.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.glasgowcourier.com/rss',
			'http://www.havredailynews.com/rss',
			'http://missoulian.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.montanakaimin.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://mtstandard.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://themountaineer.villagesoup.com/rss/story/news',
			'http://www.westyellowstonenews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.thewesternnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=members,members/*&f=rss',
			'http://helenair.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.yellowstonecountynews.com/category/local-2/feed/',
			'http://missoulanews.bigskypress.com/missoula/Rss.xml?section=1131537'
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
					imageUrl = ''

			source = d.feed.title
			location = "MT"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			