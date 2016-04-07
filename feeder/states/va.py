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

	url = ('http://www.newsplex.com/home/headlines/index.rss',
			'http://www.nbc29.com/category/85534/local-news?clienttype=rss',
			'http://www.whsv.com/news/headlines/index.rss',
			'http://wtkr.com/category/news/feed/',
			'http://wavy.com/category/news/local-news/feed/',
			'http://rssfeeds.13newsnow.com/wvec/local&x=1',
			'http://fox43tv.com/category/news/virginia/feed/',
			'http://wtvr.com/category/news/feed/',
			'http://www.nbc12.com/Global/category.asp?C=134132&nav=0RZF&clienttype=rss',
			'http://www.wdbj7.com/news/local/more-news/20465844?format=rss_2.0&view=feed',
			'http://wsls.com/feed/',
			'http://wset.com/news/local.rss',
			'http://www.wcyb.com/14591266?format=rss_2.0&view=feed',
			'http://wfirnews.com/feed',
			'http://wsvaonline.com/feed/',
			'http://wina.com/news/sections/local/feed',
			'http://wlni.com/feed',
			'http://www.heraldcourier.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local,news/local/*&f=rss',
			'http://www.dailyprogress.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://dailypress.feedsportal.com/c/34257/f/656251/index.rss',
			'http://www.godanriver.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.fredericksburg.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/blogs/weather,news/blogs/weather/*&f=rss',
			'http://www.newsadvance.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c=news/local*&f=rss',
			'http://rssfeeds.newsleader.com/staunton-news&x=1',
			'http://www.nvdaily.com/news/feed',
			'http://www.progress-index.com/news?template=rss&mime=xml',
			'http://www.richmond.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.roanoke.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local/roanoke,news/local/roanoke/*&f=rss',
			'http://www.southwesttimes.com/category/news/feed/',
			'http://rssfeeds.usatoday.com/usatoday-newstopstories&x=1',
			'http://feeds.feedburner.com/TheBlueGrayPress?format=xml',
			'http://www.cavalierdaily.com/section/news.xml',
			'http://www.collegiatetimes.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.commonwealthtimes.org/category/print-edition/news/feed/',
			'http://www.galaxgazette.com/todaysnews/rss.xml',
			'http://pilotonline.com/search/?q=&nsa=eedition&l=20&s=start_time&sd=desc&f=rss&c%5B%5D=news',
			'http://www.henricocitizen.com/site/rss',
			'http://www.blackenterprise.com/category/news/feed/',
			'http://feeds.feedburner.com/PurcellvilleGazette?format=xml',
			'http://southsidemessenger.net/feed/',
			'http://eltiempolatino.com/rss/headlines/',
						


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
			location = "VA"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			