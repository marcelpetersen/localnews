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
			'http://rssfeeds.12news.com/kpnx/local&x=1',
			'http://www.cbs5az.com/category/216452/kpho-newstream?clienttype=rss',
			'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=RSS_FEED&siteId=200017',
			'http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?obfType=RSS_FEED&siteId=10008&categoryId=10001',
			'http://www.telemundoarizona.com/noticias/local/?rss=y&embedThumb=y&summary=y',
			'http://www.tucsonnewsnow.com/Global/category.asp?C=5168&clienttype=rss',
			'http://aztecpressonline.com/category/news/feed/',
			'http://www.wildcat.arizona.edu/section/news.xml',
			'http://azbusinessdaily.com/stories.rss',
			'http://azdailysun.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://tucson.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://rssfeeds.azcentral.com/phoenix/local&x=1',
			'http://www.trivalleycentral.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=casa_grande_dispatch/area_news,casa_grande_dispatch/area_news/*&f=rss',
			'http://dcourier.com/rss/headlines/',
			'http://www.insidetucsonbusiness.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://kdminer.com/1_rss.xml',
			'http://www.mohavedailynews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.yumasun.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.westvalleyview.com/taxonomy/term/2/feed',
			'http://www.nogalesinternational.com/search/?f=rss&t',
			'http://www.tucsonweekly.com/tucson/Rss.xml?section=1063709',
			'http://feeds.feedburner.com/SedonaRedRockNews?format=xml',
			'http://www.silverbelt.com/News.xml',
			'http://www.phoenixnewtimes.com/news.rss',
			'http://www.tucsonlocalmedia.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.ahwatukee.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://azcapitoltimes.com/feed/',
			'http://cvrnews.com/1_rss.xml',
			'http://www.eastvalleytribune.com/search/?q=&t=article,link&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.grandcanyonnews.com/1_rss.xml',
			'http://www.lakepowellchronicle.com/TopStories.xml',
			'http://navajotimes.com/feed/',
			'http://nhonews.com/1_rss.xml',
			


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
			location = "AZ"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()
