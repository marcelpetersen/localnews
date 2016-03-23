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

	url = ('http://www.news9.com/category/211667/news9com-news-rss?clienttype=rss',
			'http://www.koco.com/9844956?format=rss_2.0&view=feed',
			'http://www.kswo.com/category/216452/kpho-newstream?clienttype=rss'
			'http://ktul.membercenter.worldnow.com/global/category.asp?C=189710&clienttype=rss',
			'http://www.newson6.com/category/208401/newson6com-news-rss?clienttype=rss',
			'http://www.fox23.com/feeds/rssFeed?obfType=RSS_DETAIL&siteId=600013&categoryId=500001',
			'http://www.krmg.com/list/rss/news/local/top-local-stories/aPM/',
			'http://publicradiotulsa.org/feeds/term/49/rss.xml',   
			'http://www.choctawnation.com/rss',
			'http://www.tulsaworld.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss', 
			'http://www.baptistmessenger.com/feed/',
			'http://okmulgeenews.net/local-news?format=feed',
			'http://swoknews.com/rss.xml',
			'http://www.woodwardnews.net/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local_news,news/local_news/*&f=rss',
			'http://www.miamiok.com/news?template=rss&mime=xml',
			'http://www.ardmoreite.com/news?template=rss&mime=xml',
			'http://examiner-enterprise.com/news/local-news/feed',
			'http://www.ocolly.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.oudaily.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/state*&f=rss',
			'http://www.news-star.com/news?template=rss&mime=xml'

			)

	for link in url:
		d = feedparser.parse(link)

		for data in d.entries:


			title = data.title
			link = data.link
			time = data.published
			try: 
				imageUrl = data.links[1].href
			except IndexError: 
				try:
					imageUrl = data.media_content[0]['url']
				except AttributeError:
					imageUrl = ''

			source = d.feed.title
			location = "OK"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
			except psycopg2.IntegrityError:
				dbconnect.rollback()
				print "Already Stored"
				

				

			