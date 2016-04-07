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
			'http://www.wbrc.com/Global/category.asp?C=151716&clienttype=rss',
			'http://www.wvtm13.com/29096546?format=rss_2.0&view=feed',
			'http://wvua23.com/feed/',
			'http://wiat.com/category/news/feed/',
			'http://www.wtvy.com/home/headlines/index.rss',
			'http://whnt.com/category/news/feed/',
			'http://www.waaytv.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local,news/local/*&f=rss',
			'http://www.waff.com/category/216452/kpho-newstream?clienttype=rss',
			'http://www.alabamanews.net/feed/',
			'http://www.wsfa.com/Global/category.asp?C=1188&clienttype=rss',
			'http://www.annistonstar.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://lagniappemobile.com/category/news/latest/feed/',
			'http://www.southeastsun.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.annistonstar.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.enewscourier.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://blog.al.com/news_birmingham_impact/atom.xml',
			'http://blog.al.com/news_huntsville_impact/atom.xml',
			'http://blog.al.com/news_mobile_impact/atom.xml',
			'http://blog.al.com/news_montgomery_impact/atom.xml',
			'http://blog.al.com/news_tuscaloosa_impact/atom.xml',
			'http://impact.al.com/news_anniston-gadsden_impact/atom.xml',
			'http://www.sandmountainreporter.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.birminghamtimes.com/category/local/feed/',
			'http://www.cullmantimes.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.decaturdaily.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local,news/local/*&f=rss',
			'http://www.dothaneagle.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.dothaneagle.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://times-journal.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.timesdaily.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.gadsdentimes.com/rss/articles/NEWS/1017/30',
			'http://rssfeeds.montgomeryadvertiser.com/montgomery/news&x=1',
			'http://www.oanow.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.annistonstar.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=the_daily_home/dh_news,the_daily_home/dh_news/*&f=rss',
			'http://www.tuscaloosanews.com/rss/articles/NEWS/1007/30'
		
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
			location = "AL"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			