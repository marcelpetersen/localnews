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
			'http://wabi.tv/category/news/local-news/feed/',
			'http://rssfeeds.wcsh6.com/wcsh/local&x=1',
			'http://wgme.com/news/local.rss',
			'http://www.wmtw.com/8792934?format=rss_2.0&view=asFeed',
			'http://fox23maine.com/news/local.rss',
			'http://wgan.com/news/sections/local/feed',
			'http://www.journaltribune.com/current/Front_Page/feed',
			'http://www.pressherald.com/news/feed/',
			'http://www.centralmaine.com/news/feed/',
			'http://www.timesrecord.com/news.xml',
			'http://bangordailynews.com/feed/',
			'http://feeds.feedburner.com/TheBatesStudent',
			'http://bowdoinorient.com/rss/section/1',
			'http://www.magic-city-news.com/rss.xml',
			'http://www.theforecaster.net/category/news/feed/',
			'http://sjvalley-times.com/category/news/feed/',
			'http://www.seacoastonline.com/news?template=rss&mime=xml'

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
			location = "ME"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			