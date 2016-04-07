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
			'http://www.njtvonline.org/news/feed/',
			'http://www.telemundo47.com/noticias/local/?rss=y&embedThumb=y&summary=y',
			'http://wobmam.com/category/news/feed/',
			'http://nj1015.com/feed/',
			'http://www.wnyc.org/feeds/sections/njpr/',
			'http://rssfeeds.app.com/asburypark/home',
			'http://www.burlingtoncountytimes.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://rssfeeds.mycentraljersey.com/bridgewater/home&x=1',
			'http://rssfeeds.courierpostonline.com/cherryhill/localnews',
			'http://rssfeeds.thedailyjournal.com/vineland/news&x=1',
			'http://rssfeeds.dailyrecord.com/morristown/home&x=1',
			'http://blog.nj.com/ledgerupdates_impact/rss.xml',
			'http://www.northjersey.com/cmlink/local-news-rss.rss',
			'http://www.pressofatlanticcity.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/press*&f=rss',
			'http://www.trentonian.com/section?template=RSS&profile=4002301&mime=xml',
			'http://blog.nj.com/atlantic_impact/rss.xml',
			'http://blog.nj.com/bergen_impact/rss.xml',
			'http://blog.nj.com/burlington_impact/rss.xml',
			'http://blog.nj.com/camden_impact/rss.xml',
			'http://blog.nj.com/capemay_impact/rss.xml',
			'http://blog.nj.com/cumberland_impact/rss.xml',
			'http://blog.nj.com/essex_impact/rss.xml',
			'http://blog.nj.com/gloucestercounty_impact/rss.xml',
			'http://blog.nj.com/hunterdon_impact/rss.xml',
			'http://blog.nj.com/centraljersey_impact/rss.xml',
			'http://blog.nj.com/middlesex_impact/rss.xml',
			'http://blog.nj.com/monmouth_impact/rss.xml',
			'http://blog.nj.com/morris_impact/rss.xml',
			'http://blog.nj.com/ocean_impact/rss.xml',
			'http://blog.nj.com/passaic_impact/rss.xml',
			'http://blog.nj.com/salem_impact/rss.xml',
			'http://blog.nj.com/somerset_impact/rss.xml',
			'http://blog.nj.com/sussex_impact/rss.xml',
			'http://blog.nj.com/union_impact/rss.xml',
			'http://blog.nj.com/warren_impact/rss.xml'
			'http://www.capemaycountyherald.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/government,news/government/*&f=rss',
			'http://www.voorheessun.com/feed/',
			'http://www.tabernaclesun.com/feed/'
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
			location = "NJ"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			