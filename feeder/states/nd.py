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
			'http://www.wday.com/latest/rss/',
			'http://www.wdaz.com/latest/rss/',
			'http://www.kxnet.com/category/221344/news?clienttype=rss',
			'http://www.kfyrtv.com/home/headlines/index.rss2',
			'http://www.valleynewslive.com/news/local/headlines/index.rss2',
			'http://www.kvrr.com/news/local-news/29762018?format=rss_2.0&view=feed',
			'http://www.devilslakejournal.com/news?template=rss&mime=xml',
			'http://bismarcktribune.com/search/?f=rss&c=lifestyles/outdoors&l=25&s=start_time&sd=desc',
			'http://www.thedickinsonpress.com/latest/rss/',
			'http://www.grandforksherald.com/latest/rss/',
			'http://www.jamestownsun.com/latest/rss/',
			'http://www.minotdailynews.com/page/syndrss.front/headline.xml',
			'http://www.times-online.com/rss.xml',
			'http://www.wahpetondailynews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.willistonherald.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.wcrecord.com/news/2016-03-30/News/feed',
			'http://dakotastudent.com/category/news/feed/',
			'http://ndsuspectrum.com/category/news/local/feed/',
			'http://www.inforum.com/latest/rss/',
			'http://www.heraldpressnd.com/components/rssfeed.php?ncid=6',
			'http://www.hillsborobanner.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss'
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
			location = "ND"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			