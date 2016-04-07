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
			'http://www.1011now.com/home/headlines/index.rss2',
			'http://www.nebraska.tv/category/102576/news?clienttype=rss',
			'http://feeds.feedburner.com/NetNewsStories',
			'http://www.klkntv.com/Global/category.asp?C=148537&clienttype=rss',
			'http://www.knopnews2.com/home/headlines/index.rss2',
			'http://www.ketv.com/9675452?format=rss_2.0&view=feed',
			'http://www.wowt.com/home/headlines/index.rss',
			'http://www.ketv.com/9675452?format=rss_2.0&view=feed',
			'http://fox42kptm.com/news/local.rss',
			'http://www.kotatv.com/news/nebraska-news/27244128?format=rss_2.0&view=feed',
			'http://www.kgwn.tv/home/headlines/index.rss2',
			'http://www.nbcneb.com/home/headlines/index.rss2',
			'http://ksn.com/category/news/local/feed/',
			'http://newschannelnebraska.com/feed/',
			'http://kios.org/rss.xml',
			'http://www.mycentralnebraska.com/category/news/feed/',
			'http://rapidcityjournal.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://columbustelegram.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.dailynebraskan.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://fremonttribune.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.theindependent.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local,news/local/*&f=rss',
			'http://www.hastingstribune.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local,news/local/*&f=rss',
			'http://www.kearneyhub.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local,news/local/*&f=rss',
			'http://journalstar.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.ncnewspress.com/news?template=rss&mime=xml',
			'http://norfolkdailynews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.nptelegraph.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.omaha.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.starherald.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local_news*&f=rss',
			'http://www.journaldemocrat.com/news?template=rss&mime=xml'


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
			location = "NE"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			