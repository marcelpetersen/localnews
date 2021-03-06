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
			'http://www.wmur.com/9858808?format=rss_2.0&view=feed',
			'http://wkbkradio.com/feed/',
			'https://wntk.wordpress.com/feed/',
			'http://espnkeene.com/news/sections/local/feed',
			'http://www.citizen.com/current/Local/feed',
			'http://thedartmouth.com/category/news/feed/',
			'http://www.derrynews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.fosters.com/news?template=rss&mime=xml',
			'http://www.sentinelsource.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.unionleader.com/section/news/?template=RSS?nocache=1?omniture=0',
			'http://www.seacoastonline.com/news?template=rss&mime=xml',
			'http://feeds.nashuatelegraph.com/news/full?format=xml',
			'http://www.carriagetownenews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://londonderrytimes.net/feed/',
			'http://tnhdigital.com/category/news/breaking-news/feed/',
			'http://www.fosters.com/news?template=rss&mime=xml'

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
			location = "NH"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			