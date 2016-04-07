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

	url = ('http://news10.com/category/news/local/feed/',
		'http://boston.cbslocal.com/category/news/local/feed/',
		'http://www.wcvb.com/9849828?format=rss_2.0&view=feed',
		'http://www.whdh.com/?clienttype=rss',
		'http://wwlp.com/category/news/local/feed/',
		'http://www.westernmassnews.com/category/13530/national-news?clienttype=rss',
		'http://ww.abc6.com/Global/category.asp?C=178000&clienttype=rss',
		'http://www.wbur.org/content/news/boston/feed',
		'http://whmp.com/feed/',
		'http://wpkz.net/category/new-england/feed/',
		'http://dailycollegian.com/category/collegian-news/local/feed/',
		'http://www.thecrimson.com/feeds/section/news/',
		'http://tech.mit.edu/rss/news.xml',
		'http://tuftsdaily.com/category/news/feed/',
		'http://williamsrecord.com/feed/',
		'http://www.bentleyvanguard.com/category/news/feed/',
		'http://www.umassmedia.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
		'http://dailyfreepress.com/category/news/feed/',
		'http://www.boston.com/tag/local-news/feed',
		'http://www.telegram.com/news?template=rss&mime=xml',
		'http://feeds.lowellsun.com/mngi/rss/CustomRssServlet/105/204916.xml',
		'http://www.patriotledger.com/news?template=rss&mime=xml',
		'http://delivery.digitalfirstmedia.com/ConvergencePublisher/?format=genericxml2rumble&uri=http://feeds.berkshireeagle.com/mngi/rss/CustomRssServlet/101/259206.xml',
		'http://www.southcoasttoday.com/news?template=rss&mime=xml',
		'http://www.enterprisenews.com/news?template=rss&mime=xml',
		'http://www.bostonherald.com/feed',
		'http://www.metrowestdailynews.com/news?template=rss&mime=xml',
		'http://feeds.sentinelandenterprise.com/mngi/rss/CustomRssServlet/106/230112.xml',
		'http://www.heraldnews.com/news?template=rss&mime=xml',
		'http://www.thesunchronicle.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local_news*&f=rss',
		'http://homenewshere.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
		'http://www.newburyportnews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
		'http://www.gloucestertimes.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
		'http://www.tauntongazette.com/news?template=rss&mime=xml',
		'http://www.milforddailynews.com/news?template=rss&mime=xml',
		'http://atholdailynews.com/rss.xml',
		'http://www.metro.us/rss.xml?c=1414044023-0',
		
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
			location = "MA"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()
