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
			'http://www.wcax.com/category/18197/localnews?clienttype=rss',
			'http://www.miltonindependent.com/category/news/feed/',
			'http://feeds.benningtonbanner.com/mngi/rss/CustomRssServlet/509/307700.xml',
			'http://rssfeeds.burlingtonfreepress.com/burlington/home&x=1',
			'http://feeds.reformer.com/mngi/rss/CustomRssServlet/510/205106.xml',
			'http://www.caledonianrecord.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.newportvermontdailyexpress.com/rss.xml',
			'http://www.wcax.com/category/18197/localnews?clienttype=rss',
			'https://bartonchronicle.com/feed/',
			'http://www.thenorthfieldnews.com/news.xml'
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
			location = "VT"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			