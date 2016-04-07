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
			'http://counton2.com/category/news/feed/',
			'http://www.live5news.com/Global/category.asp?C=159804&clienttype=rss',
			'http://foxcharleston.com/feed/',
			'http://www.wistv.com/Global/category.asp?C=70687&clienttype=rss',
			'http://abcnews4.com/news/local.rss',
			'http://rssfeeds.wltx.com/wltx-local&x=1',
			'http://www.abccolumbia.com/feed/',
			'http://wach.com/news/local.rss',
			'http://www.wyff4.com/9325148?format=rss_2.0&view=feed',
			'http://wspa.com/category/news/local-news-greenville-spartanburg-anderson-gaffney/feed/',
			'http://www.foxcarolina.com/category/218663/local-rss-feed?clienttype=rss',
			'http://wbtw.com/category/news/feed/',
			'http://wpde.com/news/local.rss',
			'http://www.wfxb.com/feed/',
			'http://www.wmbfnews.com/Global/category.asp?C=109081&clienttype=rss',
			'http://www.wrhi.com/category/news/local-news/feed',
			'http://www.berkeleyobserver.com/feed/',
			'http://www.southstrandnews.com/rss/all-news',
			'http://www.scnow.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.myrtlebeachonline.com/news/local/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
			'http://www.edgefieldadvertiser.com/feed/',
			'http://www.scnow.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.aikenstandard.com/apps/pbcs.dll/section?category=feed&template=rss&mime=xml&profile=1007',
			'http://rssfeeds.greenvilleonline.com/greenville/news&x=1',
			'http://www.heraldonline.com/news/local/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
			'http://www.goupstate.com/rss/articles/NEWS/1083/30',
			'http://www.independentmail.com/feeds/rss/news',
			'http://www.postandcourier.com/apps/pbcs.dll/section?Category=PC1602&template=rss&mime=XML',
			'http://www.thestate.com/news/local/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
			'http://uniondailytimes.com/feed',
			'http://thetandd.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc'	
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
			location = "SC"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			