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

	url = ('http://www.14news.com/category/216452/kpho-newstream?clienttype=rss',
			'http://wane.com/category/news/local/feed/'
			'http://44news.wevv.com/indiana/feed/',
			'http://www.21alive.com/news/local/index.rss2',
			'http://lakeshorepublicmedia.org/topic/local/feed/',
			'http://cbs4indy.com/category/news/feed/',
			'http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?siteId=100004&obfType=RSS_FEED&categoryId=20000',
			'http://wishtv.com/feed/',
			'http://www.wthr.com/category/23903/local-news?clienttype=rss',
			'http://feeds.feedburner.com/wfiunews?format=xml',
			'http://fox59.com/category/news/feed/',
			'http://wlfi.com/category/news/local/feed/',
			'http://www.wndu.com/news/headlines/index.rss',
			'http://www.wsbt.com/news/local/21046404?format=rss_2.0&view=feed',
			'http://www.fox28.com/category/123726/news?clienttype=rss',
			'http://wthitv.com/category/news/local/feed/',
			'http://www.waovam.com/feed/',
			'http://www.wbiw.com/local/index.xml',
			'http://newstalk1280.com/category/local-news/feed/',
			'http://www.wgclradio.com/feed/',
			'http://www.wowo.com/feed/',
			'http://www.newsnowwarsaw.com/category/local-news/feed/',
			'http://localnewsdigital.com/feed/',
			'http://www.wsbt.com/news/local/21046404?format=rss_2.0&view=feed',
			'http://www.depauw.edu/feeds/news/',
			'http://feeds.feedburner.com/bostonphoenix/',
			'http://www.ipfwcommunicator.org/category/news-politics/feed/',
			'http://andersonian.com/category/top-stories/feed/',
			'https://record.goshen.edu/category/news/feed',
			'http://www.valpotorch.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.isustudentmedia.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=indiana_statesman/news*&f=rss',
			'http://iusbpreface.net/feed/',
			'http://www.heraldbulletin.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://kpcnews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.batesvilleheraldtribune.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.tmnews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.heraldtimesonline.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local,news/local/*&f=rss',
			'https://news-banner.com/category/news/local-news/feed/',
			'http://www.thebraziltimes.com/feed/rss/all/week.rss',
			'http://www.thebanner.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.thepostandmail.com/rss.xml',
			'http://www.therepublic.com/feed/local',
			'http://www.journalreview.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.decaturdailydemocrat.com/rss.xml',
			'http://kpcnews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.elkharttruth.com/rss/news',
			'http://www.courierpress.com/news/local/index.rss',
			'http://www.journalgazette.net/news/local/rss/',
			'http://www.dailyjournal.net/feed/local',
			'http://www.chronicle-tribune.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.goshennews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.bannergraphic.com/feed/rss/news/week.rss',
			'http://www.greenfieldreporter.com/feed/local',
			'http://www.hartfordcitynewstimes.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local,news/local/*&f=rss',
			'http://www.ibj.com/rss/9',
			'http://www.indianapolisrecorder.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local,news/local/*&f=rss',
			'http://rssfeeds.indystar.com/indystar/allnews&x=1',
			'http://www.kokomotribune.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.heraldargus.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://rssfeeds.jconline.com/lafayettein/news&x=1',
			'http://www.reporter.net/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.gcdailyworld.com/feed/rss/all/week.rss',
			'http://www.pharostribune.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.reporter-times.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.thenewsdispatch.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local,news/local/*&f=rss',
			'http://rssfeeds.thestarpress.com/muncie/news&x=1',
			'http://www.nwitimes.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c%5B%5D=news/local&f=rss',
			'http://www.personcountylife.com/news.xml',
			'http://thetimes24-7.com/1_rss.xml',
			'http://www.journal-topics.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.flyergroup.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.shelbynews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.thepilotnews.com/rss.xml',
			'http://www.rochsent.com/31_rss.xml',
			'http://www.rushvillerepublican.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.tribtown.com/feed/local',
			'http://www.southbendtribune.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.spencereveningworld.com/news.xml',
			'http://www.tribstar.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.washtimesherald.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.timessentinel.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.frostillustrated.com/category/local-2/feed/',
			'http://www.newsbug.info/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://ss-times.com/feed/',
			'http://kokomoperspective.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss'


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
			location = "IN"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()
