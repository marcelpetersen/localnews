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
			'http://www.wlox.com/Global/category.asp?C=2868&nav=DYFw&clienttype=rss',
			'http://www.mpbonline.org/blogs/news/rss/',
			'http://feeds.feedburner.com/WDAMNews?format=xml',
			'http://whlt.com/category/news/feed/',
			'http://www.msnewsnow.com/Global/category.asp?C=7857&clienttype=rss',
			'http://wjtv.com/category/news/feed/',
			'http://www.wapt.com/9157890?format=rss_2.0&view=feed',
			'http://www.wtok.com/home/headlines/index.rss2',
			'http://feeds.feedburner.com/wgbctv?format=xml',
			'http://www.wcbi.com/category/local-news/feed/',
			'http://www.wmxi.com/category/state-news/feed',
			'http://www.dailyleader.com/category/news/feed/',
			'http://rssfeeds.clarionledger.com/jacksonms/news&x=1',
			'http://www.pressregister.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://dailycorinthian.com/rss/home/Daily+Corinthian+Stories?instance=Daily+Corinthian+Stories&content_type=article&tags=rss&offset=0&limit=200&source=site&page_name=home',
			'http://www.dailytimesleader.com/rss.xml',
			'http://www.ddtonline.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.gwcommonwealth.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news&f=rss',
			'http://rssfeeds.hattiesburgamerican.com/hattiesburgamerican/news&x=1',
			'http://leader-call.com/local-news/feed/',
			'http://www.meridianstar.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.natchezdemocrat.com/category/news/feed/',
			'http://djournal.com/news/feed/',
			'http://www.picayuneitem.com/category/news/feed/',
			'http://starkvilledailynews.com/rss.xml',
			'http://www.reflector-online.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://thedmonline.com/feed/'
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
			location = "MS"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			