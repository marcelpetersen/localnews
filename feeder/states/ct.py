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
			'http://wtnh.com/category/news/feed/',
			'http://www.wfsb.com/category/210857/app-news?clienttype=rss',
			'http://www.nbcconnecticut.com/news/local/?rss=y&embedThumb=y&summary=y',
			'http://wtnh.com/category/news/feed/',
			'http://fox61.com/category/news/feed/',
			'http://www.wxlm.fm/feed/',
			'http://wshu.org/feeds/term/21/rss.xml',
			'http://connecticut.cbslocal.com/category/local-news/feed/',
			'http://www.stamfordadvocate.com/RSS/feed/Breaking-news-from-stamfordadvocate-com-251.php',
			'http://www.centralctcommunications.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=bristolpress/news*&f=rss',
			'http://www.norwichbulletin.com/news/state-news?template=rss&mime=xml',
			'http://ctmirror.org/feed/',
			'http://www.ctpost.com/rss/collectionRss/RSS-News-59480.php',
			'http://www.greenwichtime.com/RSS/feed/Breaking-news-from-greenwichtime-com-252.php',
			'http://feeds.feedburner.com/courant-breaking-news',
			'http://www.centralctcommunications.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=newbritainherald*&f=rss',
			'http://www.thehour.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.journalinquirer.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=page_one*,page_one*/*&f=rss',
			'http://www.middletownpress.com/section?template=RSS&profile=4002068&mime=xml',
			'http://www.middletownpress.com/section?template=RSS&profile=4002069&mime=xml',
			'http://www.nhregister.com/section?template=RSS&profile=4000932&mime=xml',
			'http://www.nhregister.com/section?template=RSS&profile=4001333&mime=xml',
			'http://www.nhregister.com/section?template=RSS&profile=4001332&mime=xml',
			'http://www.nhregister.com/section?template=RSS&profile=4002036&mime=xml',
			'http://www.nhregister.com/section?template=RSS&profile=4001238&mime=xml',
			'http://www.nhregister.com/section?template=RSS&profile=4001239&mime=xml',
			'http://www.newstimes.com/RSS/feed/Breaking-news-from-newstimes-com-249.php',
			'http://www.registercitizen.com/section?template=RSS&profile=4002074&mime=xml',
			'http://www.registercitizen.com/section?template=RSS&profile=4002076&mime=xml',
			'http://www.registercitizen.com/section?template=RSS&profile=4002078&mime=xml',
			'http://www.rep-am.com/rss/rss.php?rss=news',
			'http://minutemannewscenter.com/?rss=fairfield/news',
			'http://minutemannewscenter.com/?rss=westport/news',
			'http://www.courant.com/breaking-news/rss2.0.xml',
			'http://www.theridgefieldpress.com/category/news/feed/',
			'http://dailycampus.com/stories/?format=rss',
			'http://www.collegian.psu.edu/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://fairfieldmirror.com/category/news/feed/',
			'http://yaledailynews.com/feed/'

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
			location = "CT"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			