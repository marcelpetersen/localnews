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
				'http://www.kwch.com/rss/21055626?format=rss_2.0&view=feed',
				'http://ksn.com/category/news/local/feed/',
				'http://www.kake.com/home/headlines/index.rss2',
				'http://feeds.feedburner.com/KOAMnews?format=xml',
				'http://feeds.feedburner.com/KOAMnews?format=xml',
				'http://www.wibw.com/home/localnews/headlines/index.rss',
				'http://ksnt.com/category/news/local-news/feed/',
				'http://www.knssradio.com/pages/rss/fg-11877.rss',
				'http://www.ksal.com/feed/',
				'http://www.wibwnewsnow.com/news/feed/',
				'http://www.jcpost.com/feed/',
				'http://1350kman.com/category/local-news/feed/',
				'http://centralkansasradio.com/feed/',
				'http://www.arkcity.net/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
				'http://www.atchisonglobenow.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
				'http://www.butlercountytimesgazette.com/news?template=rss&mime=xml',
				'http://www.chanute.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
				'http://www.ccenterdispatch.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
				'http://www.dodgeglobe.com/news?template=rss&mime=xml',
				'http://www.butlercountytimesgazette.com/news?template=rss&mime=xml',
				'http://www.emporiagazette.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
				'http://www.gbtribune.com/syndication/feeds/rss/69/',
				'http://www.hdnews.net/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
				'http://www.hutchnews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
				'http://www2.ljworld.com/rss/headlines/lawrence/',
				'http://www.leavenworthtimes.com/news?template=rss&mime=xml',
				'http://www.mcphersonsentinel.com/news?template=rss&mime=xml',
				'http://www.morningsun.net/news?template=rss&mime=xml',
				'http://www.thekansan.com/news?template=rss&mime=xml',
				'http://www.ottawaherald.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
				'http://www.salina.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
				'http://www.sentineltimes.com/category/local-news/feed/',
				'http://cjonline.com/rssfeed/16',
				'http://www.wellingtondailynews.com/news?template=rss&mime=xml',
				'http://www.winfieldcourier.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
				'http://www.kstatecollegian.com/category/news/feed/',
				'http://www.kansan.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
				

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
			location = "KS"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			