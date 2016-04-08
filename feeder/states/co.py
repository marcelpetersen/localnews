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
			'http://www.kktv.com/home/headlines/index.rss2',
			'http://www.krdo.com/14776464?format=rss_2.0&view=feed',
			'http://fox21news.com/category/news/local/feed/',
			'http://kwgn.com/category/news/feed/',
			'http://denver.cbslocal.com/category/news/feed/',
			'http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?obfType=RSS_FEED&siteId=100003&categoryId=10001',
			'http://rssfeeds.9news.com/kusa-local&x=1',
			'http://www.telemundodenver.com/noticias/local/?rss=y&embedThumb=y&summary=y',
			'http://kdvr.com/category/news/feed/',
			'http://krqe.com/category/news/feed/',
			'http://www.nbc11news.com/home/headlines/index.rss2',
			'http://inewsnetwork.org/feed/',
			'http://feeds.denverpost.com/dp-news-breaking-local',
			'http://feeds.feedburner.com/GazetteOnlineLocalNews?format=xml',
			'http://feeds.dailycamera.com/mngi/rss/CustomRssServlet/21/218121.xml',
			'http://www.chieftain.com/XMLServer/?pub=PuebloChieftain&section=/News/',
			'http://www.pueblowestview.com/XMLServer/?pub=PuebloWestView&section=/News/',
			'http://www.gjsentinel.com/feeds/rss2',
			'feed://feeds.timescall.com/mngi/rss/CustomRssServlet/46/243101.xml',
			'http://rssfeeds.coloradoan.com/fortcollins/news&x=1',
			'http://www.durangoherald.com/section/news01?template=RSS&mime=xml',
			'http://feeds.canoncitydailyrecord.com/mngi/rss/CustomRssServlet/49/244843.xml',
			'http://feeds.feedburner.com/AspenDailyNews?format=xml',
			#remove 'http://www.aspentimes.com/csp/mediapool/sites/SwiftShared/assets/csp/rssCategoryFeed.csp?pub=AspenTimes&sectionId=745&sectionLabel=News',
			'http://www.aurorasentinel.com/feed/',
			'http://www.boulderweekly.com/news/feed/',
			#remove # 'http://feeds.broomfieldenterprise.com/mngi/rss/CustomRssServlet/24/218410.xml',
			'http://feeds.lamarledger.com/mngi/rss/CustomRssServlet/27/217303.xml',
			# remove'http://www.canyoncourier.com/todaysnews/rss.xml',
			'http://feeds.coloradodaily.com/mngi/rss/CustomRssServlet/25/219104.xml',
			'http://www.csindy.com/coloradosprings/Rss.xml?section=1064314',
			'http://feeds.eptrail.com/mngi/rss/CustomRssServlet/28/218052.xml',
			'http://feeds.lamarledger.com/mngi/rss/CustomRssServlet/27/217303.xml',
			'http://feeds.lamarledger.com/mngi/rss/CustomRssServlet/27/217303.xml',
			'http://feeds.julesburgadvocate.com/mngi/rss/CustomRssServlet/23/218046.xml',
			'http://www.lajuntatribunedemocrat.com/news?template=rss&mime=xml',
			'http://www.steamboattoday.com/rss/headlines/',
			'http://www.telluridenews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.vaildaily.com/csp/mediapool/sites/SwiftShared/assets/csp/rssCategoryFeed.csp?pub=VailDaily&sectionId=876&sectionLabel=News',
			'http://www.westword.com/news.rss'
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
			location = "CO"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			