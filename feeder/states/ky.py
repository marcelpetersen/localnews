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
			'http://www.wbko.com/feeds/iphone?placement=/news/headlines',
			'http://www.wtvq.com/category/local-news/feed/',
			'http://www.wave3.com/category/1178/home?clienttype=rss',
			'http://rssfeeds.whas11.com/whas/local',
			'http://www.wlky.com/9366964?format=rss_2.0&view=asFeed',
			'http://www.wdrb.com/Global/category.asp?C=123963&nav=menu1404_2&clienttype=rss',
			'http://www.wekyam.com/category/news/feed/',
			'http://wfpl.org/feed/',
			'http://womiowensboro.com/feed/',
			# 'http://www.kystandard.com/todaysnews/rss.xml',
			'http://www.kentucky.com/latest-news/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
			'http://www.leoweekly.com/category/news/feed/',
			'http://www.messenger-inquirer.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://newsdemocratleader.com/feed',
			# 'http://www.thenewsenterprise.com/todaysnews/rss.xml',
			# 'http://www.oldhamera.com/todaysnews/rss.xml',
			'http://www.bgdailynews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			# 'http://www.pioneernews.net/todaysnews/rss.xml',
			'http://www.richmondregister.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.sentinel-echo.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.rutlandherald.com/apps/pbcs.dll/section?category=RSS04&mime=xml',
			'http://www.thetimestribune.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.tricitynews.com/cmlink/tcn-news-rss-valid-1.1999006',
			# 'http://www.mytrimblenews.com/todaysnews/rss.xml',
			'http://www.voice-tribune.com/feed/',
			'http://www.kykernel.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://wkuherald.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.easternprogress.com/category/news/feed/',
			'http://www.centralkynews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=amnews/news,amnews/news/*&f=rss',
			# 'http://www.theandersonnews.com/todaysnews/rss.xml',
			'http://bizlex.com/category/latest-news-2/feed/',
			'http://www.somerset-kentucky.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://rssfeeds.courier-journal.com/courierjournal/news&x=1',
			'http://floydcountytimes.com/feed',
			'http://www.news-graphic.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://harlandaily.com/feed',
			'http://www.thegleaner.com/news/index.rss2',
			'http://www.dailyindependent.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss'

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
			location = "KY"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			