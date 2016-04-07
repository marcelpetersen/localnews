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
			'http://www.4029tv.com/8898458?format=rss_2.0&view=asFeed',
			'http://5newsonline.com/category/news/feed/',
			'http://www.kait8.com/global/Category.asp?c=4391&clienttype=rss',
			'http://katv.com/news/local.rss',
			'http://rssfeeds.thv11.com/kthv/local',
			'http://www.newsradio1029.com/feed/',
			'http://www.arkansasonline.com/rss/headlines/latest/',
			'http://guardonline.com/category/local-news/feed/',
			'http://rssfeeds.baxterbulletin.com/baxter/home',
			'http://www.nwaonline.com/rss/headlines/arkansas/northwest/',
			'http://couriernews.com/rss/rss/News?instance=News&content_type=article&tags=news_local+news_obituaries+news_politics_government+news_education+news_crime+news_community+news_faith+news_state+news_nation+news_world+news_business&tag_inclusion=or&offset=0&limit=25&page_name=rss',
			'http://www.thedailycitizen.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.siftingsherald.com/news?template=rss&mime=xml',
			'http://www.helena-arkansas.com/news?template=rss&mime=xml',
			'http://harrisondaily.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news&f=rss',
			'http://www.hopestar.com/news?template=rss&mime=xml',
			'http://pulaskinews.net/taxonomy/term/11/feed',
			'http://pulaskinews.net/taxonomy/term/16/feed',
			'http://pulaskinews.net/taxonomy/term/1015/feed',
			'http://pulaskinews.net/taxonomy/term/1091/feed',
			'http://thecabin.net/taxonomy/term/162/0/feed',
			'http://www.malvern-online.com/rss.xml',
			'http://www.nwaonline.com/rss/headlines/arkansas/northwest/',
			'http://www.paragoulddailypress.com/',
			'http://pbcommercial.com/news/local/feed',
			'http://www.bentoncourier.com/rss.xml',
			'http://swtimes.com/news/feed',
			'http://thnews.com/category/news/feed/',
			'http://www.arkansasbusiness.com/rss/daily-report',
			'http://www.arktimes.com/arkansas/Rss.xml?section=861840',
			'http://www.nwaonline.com/rss/headlines/arkansas/northwest/',
			'http://www.uatrav.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local_news,news/local_news/*&f=rss',
			'http://ucaecho.net/feed/'			
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
			location = "AR"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			