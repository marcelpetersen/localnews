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
			'http://kenvtv.com/news/local.rss',
			'http://news3lv.com/news/local.rss',
			'http://www.fox5vegas.com/category/210851/app-news?clienttype=rss',
			'http://www.telemundolasvegas.com/noticias/local/?rss=y&embedThumb=y&summary=y',
			'http://mynews4.com/news/local.rss',
			'http://www.kolotv.com/feeds/rss',
			'http://foxreno.com/news/local.rss',
			'http://www.ktvn.com/Global/category.asp?C=90455&clienttype=rss',
			'http://kdwn.com/tag/local/feed/',
			'http://lasvegas.cbslocal.com/category/news/feed/',
			'http://www.reviewjournal.com/news/las-vegas/feed',
			'http://elkodaily.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://lasvegassun.com/feeds/headlines/all/',
			'http://www.nevadaappeal.com/csp/mediapool/sites/SwiftShared/assets/csp/rssCategoryFeed.csp?pub=NevadaAppeal&sectionId=656&sectionLabel=Local',
			'http://rssfeeds.rgj.com/reno/news&x=1',
			'http://www.gvnews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://pvtimes.com/taxonomy/term/1/feed',
			'http://www.recordcourier.com/csp/mediapool/sites/SwiftShared/assets/csp/rssCategoryFeed.csp?pub=RecordCourier&sectionId=694&sectionLabel=Local',
			'http://www.southvalleyjournal.com/categories/news.rss',
			'http://sparkstrib.com/category/news/feed/'
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
			location = "NV"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			