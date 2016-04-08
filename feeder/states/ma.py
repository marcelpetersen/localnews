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

		'http://minnesota.cbslocal.com/category/news/local/feed/',
			'http://kstp.com/rssFeeds/rss1.xml',
			'http://www.northlandsnewscenter.com/news/local/index.rss2',
			'http://www.keyc.com/Global/category.asp?C=201267&clienttype=rss',
			'http://rssfeeds.kare11.com/kare/local&x=1',
			'http://kimt.com/category/news/local-news/feed/',
			'http://www.kaaltv.com/rssFeeds/rss10151.xml',
			'http://www.mprnews.org/topic/all-news/rss',
			'http://www.kchkradio.net/feed/',
			'http://www.knuj.net/feed/',
			'http://krocam.com/feed/',
			'http://www.myalbertlea.com/category/news/local-news/feed/',
			'http://www.willmarradio.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.voiceofalexandria.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://kymnradio.net/news/feed/',
			'http://minnesota.cbslocal.com/category/news/feed/',
			'http://wjon.com/feed/',
			'http://www.mndaily.com/rss',
			'http://www.crookstontimes.com/news?template=rss&mime=xml',
			'http://www.duluthnewstribune.com/latest/rss/',
			'http://www.mankatofreepress.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://finance-commerce.com/category/news/feed/',
			'https://www.minnpost.com/department/30893/rss.xml',
			'http://www.twincities.com/section/news/feed/',
			'http://www.startribune.com/local/index.rss2',
			'http://www.nujournal.com/page/syndrss.front/headline.xml',
			'http://www.republican-eagle.com/latest/rss/',
			'http://www.postbulletin.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://rssfeeds.sctimes.com/stcloud/news&x=1',
			'http://www.virginiamn.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.winonadailynews.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.dglobe.com/latest/rss/'
				
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
			location = "MA"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()
