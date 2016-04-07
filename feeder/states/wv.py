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
			'http://www.wvva.com/Global/category.asp?C=141371&clienttype=rss',
			'http://www.wearewvproud.com/?clienttype=rss',
			'http://www.wsaz.com/news/index.rss2',
			'http://wchstv.com/news/local.rss',
			'http://wvah.com/news/local.rss',
			'http://www.tristateupdate.com/?clienttype=RSS',
			'http://wvpublic.org/feeds/term/23/rss.xml',
			'http://www.wdtv.com/rss.cfm?type=5News',
			'http://www.wvalways.com/?clienttype=rss',
			'http://www.yourohiovalley.com/?clienttype=rss',
			'http://wtov9.com/news/local.rss',
			'http://wajr.com/category/local-news/feed/',
			'http://wepm.com/feed/',
			'http://www.register-herald.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.timeswv.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.herald-dispatch.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://thedpost.com/Dev/RSS-Test?rss=Local-Stories',
			'http://www.newsandsentinel.com/page/syndrss.front/headline.xml',
			'http://theintelligencer.net/page/syndRSS.front/headline.xml?ID=526&subCatID=515',
			'http://www.bdtonline.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.theet.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.newstribune.info/news?template=rss&mime=xml',
			'http://loganbanner.com/category/news/feed',
			'http://www.journal-news.net/page/syndrss.front/headline.xml',
			'http://mydailyregister.com/category/news/feed',
			'http://www.weirtondailytimes.com/page/syndrss.front/headline.xml',
			'http://williamsondailynews.com/category/news/feed',
			'http://www.thedaonline.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://marshallparthenon.com/category/news/feed/'
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
			location = "WV"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			