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

	url = ('http://cbs2iowa.com/news/local.rss',
			'http://www.kwwl.com/category/128862/news?clienttype=rss',
			'http://kwqc.com/category/news/local-news/feed/',
			'http://www.kcci.com/9358036?format=rss_2.0&view=feed',
			'http://whotv.com/category/news/feed/',
			'http://kimt.com/category/news/local-news/feed/',
			'http://www.kaaltv.com/rssFeeds/rss10151.xml',
			'http://www.kttc.com/Global/category.asp?C=123673&clienttype=rss',
			'http://siouxlandnews.com/news/local.rss',
			'http://www.ottumwaradio.com/category/local-news/feed/',
			'http://www.kbur.com/category/news/local-news/feed/',
			'http://kicdam.com/news/sections/local/feed',
			'http://www.kmaland.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://kscj.com/category/kscj-local-news/feed/',
			'http://www.kwbg.com/category/local-news/feed/',
			'http://amestrib.com/topnews/feed',
			'http://www.swiowanewssource.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://newsrepublican.com/taxonomy/term/1251/feed',
			'http://www.clintonherald.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.nonpareilonline.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.dailyiowegian.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://rssfeeds.desmoinesregister.com/desmoines/news&x=1',
			'http://www.esthervilledailynews.com/page/syndrss.front/headline.xml',
			'http://fairfield-ia.villagesoup.com/rss/story/news',
			'http://www.dailydem.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://feeds.feedburner.com/GazetteOnlineLocalNews?format=xml',
			'http://globegazette.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.thehawkeye.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://rssfeeds.press-citizen.com/iowacity/home&x=1',
			'http://www.dailygate.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.lemarssentinel.com/feed/rss/news/week.rss',
			'http://www.messengernews.net/page/syndRSS.front/headline.xml?ID=5020&subCatID=5010',
			'http://mt-pleasant-ia.villagesoup.com/rss/story/news',
			'http://muscatinejournal.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.newtondailynews.com/?rss=news',
			'http://www.ottumwacourier.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://qctimes.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://siouxcityjournal.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.spencerdailyreporter.com/feed/rss/all/week.rss',
			'http://www.thonline.com/search/?q=&t=article&l=500&d=today&d1=&d2=&s=&sd=desc&f=rss',
			'http://washington-ia.villagesoup.com/rss/story/news',
			'http://wcfcourier.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.freemanjournal.net/page/syndrss.front/headline.xml',
			'http://daily-iowan.com/feed/'
			

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
			location = "IA"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			