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

	url = ('http://www.waow.com/Global/category.asp?C=123744&clienttype=rss',
			'http://www.weau.com/home/headlines/index.rss',
			'http://www.wqow.com/Global/category.asp?C=123744&clienttype=rss',
			'http://wbay.com/category/news/local/feed/',
			'http://fox11online.com/news/local.rss',
			'http://www.news8000.com/news?format=rss_2.0&view=feed',
			'http://www.wxow.com/Global/category.asp?C=123769&clienttype=rss',
			'http://www.channel3000.com/?format=rss_2.0&view=feed',
			'http://www.nbc15.com/home/headlines/index.rss',
			'http://fox6now.com/category/news/feed/',
			'http://www.wisn.com/9374280?format=rss_2.0&view=feed',
			'http://www.northlandsnewscenter.com/news/local/index.rss2',
			'http://www.wdio.com/rssfeeds/rss10335.xml',
			'http://www.fox21online.com/news/local-news/29764842?format=rss_2.0&view=feed',
			'http://www.wsaw.com/home/headlines/index.rss2',
			'http://www.1410wizm.com/index.php?format=feed',
			'http://www.whby.com/index.php/rss/feeds/whby_news/25',
			'http://www.1490wosh.com/category/local-news/feed/',
			'http://wtaq.com/news/feed/local/rss/',
			'http://rssfeeds.postcrescent.com/appleton/news&x=1',
			'http://www.apg-wi.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.beloitdailynews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/national,news/national/*&f=rss',
			'http://www.hngnews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=sun_prairie_star*&f=rss',
			'http://www.chetekalert.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news&f=rss',
			'http://www.chiltontimesjournal.com/category/news/feed/',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=monona_cottage_grove,monona_cottage_grove/*&f=rss',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=cambridge_deerfield,cambridge_deerfield/*&f=rss',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=deforest_times/news/school,deforest_times/news/school/*&f=rss',
			'http://www.leadertelegram.com/rss',
			'http://rssfeeds.fdlreporter.com/fonddulac/news&x=1',
			'http://www.dailyunion.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://rssfeeds.greenbaypressgazette.com/greenbay/news&x=1',
			'http://lacrossetribune.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=lodi_enterprise/news/local,lodi_enterprise/news/local/*&f=rss',
			'https://badgerherald.com/news/feed/',
			'http://host.madison.com/search/?f=rss&t=article&c=&l=25&s=start_time&sd=desc',
			'https://themadisonmisnomer.com/category/news/feed/',
			'http://host.madison.com/search/?f=rss&t=article&c=&q=%23wsj&l=25&s=start_time&sd=desc',
			'http://rssfeeds.htrnews.com/manitowoc/news&x=1',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=mcfarland_thistle/news/school,mcfarland_thistle/news/school/*&f=rss',
			'http://middletontimes.com/rss.xml',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=milton_courier/sports/local/softball,milton_courier/sports/local/softball/*&f=rss',
			'http://hosted2.ap.org/atom/OHCJL/f88abdb59d484e25a06de66b0c595a58',
			'http://rssfeeds.thenorthwestern.com/oshkosh/news&x=1',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=lodi_enterprise/news/local,lodi_enterprise/news/local/*&f=rss',
			'http://rssfeeds.sheboyganpress.com/sheboygan/news&x=1',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=sun_prairie_star/news,sun_prairie_star/news/*&f=rss',
			'http://mykenoshacounty.com/?feed=rss2',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=waterloo_marshall/news/local,waterloo_marshall/news/local/*&f=rss',
			'http://www.watertowndailytimes.com/section/rss_wdtnews?mime=application%2Frss%2Bxml',
			'http://www.hngnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=waunakee_tribune/news/government,waunakee_tribune/news/government/*&f=rss',
			'http://rssfeeds.wausaudailyherald.com/wausau/news&x=1',
			'http://www.wausharaargus.com/rss.xml',
			'http://rssfeeds.wisconsinrapidstribune.com/wisconsinrapids/news'

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
			location = "WI"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			