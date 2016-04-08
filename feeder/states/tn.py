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
			'http://www.wrcbtv.com/Global/category.asp?C=123971&clienttype=rss',
			'http://newschannel9.com/news/local.rss',
			'http://www.wdef.com/category/local-news/feed/',
			'http://foxchattanooga.com/news/local.rss',
			'http://www.wbbjtv.com/feed/',
			'http://wate.com/category/news/local-news/feed/',
			'http://rssfeeds.wbir.com/wbir/local_news',
			';http://wreg.com/category/news/feed/',
			'http://www.wmcactionnews5.com/category/4728/news?clienttype=rss',
			'http://wkrn.com/category/news/local/feed/',
			'http://www.wsmv.com/category/208528/news?clienttype=rss',
			'http://fox17.com/news/local.rss',
			'http://wjhl.com/category/news/local-news/feed/',
			'http://www.wcyb.com/14591266?format=rss_2.0&view=feed',
			'http://www.chattanoogan.com/Breaking-News/feed.rss',
			'http://www.newstalk987.com/category/local-news/feed/',
			'http://nashvillepublicradio.org/rss.xml',
			'http://mix104.info/feed/',
			'http://www.dailypostathenian.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://rssfeeds.theleafchronicle.com/clarksville/news&x=1',
			'http://columbiadailyherald.com/news/local-news/feed',
			'http://www.greenevillesun.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://rssfeeds.jacksonsun.com/jacksontn/news&x=1',
			'http://www.timesnews.net/rss/local',
			# 'http://www.knoxvilledailysun.com/feed.xml',
			'http://www.knoxnews.com/feeds/rss/news/local',
			'http://www.thedailytimes.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.commercialappeal.com/topstories/index.rss',
			'http://www.t-g.com/feed/rss/news/week.rss',
			'http://rssfeeds.dnj.com/murfreesboro/news&x=1',
			'http://www.citizentribune.com/feed/',
			'http://rssfeeds.tennessean.com/nashville/home&x=1',
			'http://www.oakridger.com/news?template=rss&mime=xml',
			'http://www.parispi.net/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://timesgazette.com/feed',
			'http://www.tullahomanews.com/feed/',
			'http://www.stategazette.com/feed/rss/all/week.rss',
			'http://feeds.feedburner.com/memphisdailynews/bbde?format=xml',
			'http://www.memphisflyer.com/memphis/Rss.xml?section=1104305',
			'http://tsdmemphis.com/rss/headlines/',
			'http://www.advocateanddemocrat.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.nashvillecitypaper.com/top-stories/feed',
			'http://www.nashvillescene.com/nashville/Rss.xml?section=1178033',
			'http://www.southernstandard.com/syndication/feeds/rss/60/',
			
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
			location = "TN"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			