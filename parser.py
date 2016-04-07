#!/usr/bin/env python

import feedparser
import psycopg2

with psycopg2.connect("dbname ='feedparser' user ='admin' password= 'admin' host = 'localhost' ") as dbconnect:
	cur = dbconnect.cursor()

	url = (
			'http://www.ksfy.com/home/headlines/index.rss2',
			'http://www.kotatv.com/news/south-dakota-news/26933602?format=rss_2.0&view=feed',
			'http://www.kdlt.com/news/local-news/29767676?format=rss_2.0&view=feed',
			'http://www.keloland.com/feeds/NewsRssFeed',
			'http://www.newscenter1.tv/category/308614/local-news?clienttype=rss',
			'http://www.kbhbradio.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.drgnews.com/category/news/feed/',
			'http://www.gowatertown.net/category/local-news/feed/',
			'http://ksoo.com/category/news/feed/',
			'http://www.hubcityradio.com/feed/',
			'http://wnax.com/feed/',
			'http://www.aberdeennews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://rssfeeds.argusleader.com/siouxfalls/news&x=1',
			'http://www.bhpioneer.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/state_news,news/state_news/*&f=rss',
			'http://www.brookingsregister.com/News.xml',
			'http://www.capjournal.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.freemansd.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.plainsman.com/TopStories.xml',
			'http://www.mitchellrepublic.com/news/rss/',
			'http://www.plaintalk.net/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=local_news,local_news/*&f=rss',
			'http://rapidcityjournal.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.truedakotan.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.thepublicopinion.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.yankton.net/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=sports,sports/*&f=rss',
			
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
			location = "SD"

			try:
				print source
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
			except psycopg2.IntegrityError:
				dbconnect.rollback()