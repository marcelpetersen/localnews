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
		'http://foxsanantonio.com/local.rss',
		'http://news4sanantonio.com/news/local.rss',
		'http://cbs4local.com/news/local.rss',
		'http://kfdm.com/news/local.rss',
		'http://keyetv.com/news/local.rss',
		'http://www.ktxs.com/14770050?format=rss_2.0&view=feed',
		'http://www.cbs19.tv/Global/category.asp?C=137100&clienttype=rss',
		'http://www.newschannel10.com/category/72489/news?clienttype=rss',
		'http://www.ksla.com/global/Category.asp?c=2801&clienttype=rss',
		'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=RSS_FEED&siteId=200004',
		'http://rssfeeds.kvue.com/kvue/local',
		'http://kxan.com/category/news/local/feed/',
		'http://thecwaustin.com/feed/',
		'http://feedsyn.univision.com/univisionaustin',
		'http://www.12newsnow.com/Global/category.asp?C=177955&clienttype=rss',
		# 'http://www.newswest9.com/Global/category.asp?C=83261&clienttype=rss',
		'http://www.telemundo40.com/noticias/local/?rss=y&embedThumb=y&summary=y',
		'http://www.kbtx.com/content/news/index.rss',
		'http://www.kiiitv.com/category/194865/news?clienttype=rss',
		'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=RSS_FEED&siteId=200007',
		'http://www.nbcdfw.com/news/local/?rss=y&embedThumb=y&summary=y',
		'http://rssfeeds.wfaa.com/wfaa/local',
		'http://dfw.cbslocal.com/category/news/feed/',
		'http://feedsyn.univision.com/univisiondallas',
		'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=RSS_FEED&siteId=200007',
		'http://www.telemundodallas.com/noticias/local/?rss=y&embedThumb=y&summary=y',
		'http://www.kvia.com/15161272?format=rss_2.0&view=feed',
		'http://www.click2houston.com/feeds/rssFeed/feedServlet?obfType=GMG_RSS_DETAIL&siteId=800003&categoryId=80045&nbRows=20&FeedFetchDays=10&includeFeeds=True',
		'http://rssfeeds.khou.com/khou/local',
		'http://abc13.com/feed/',
		'http://cw39.com/category/newsfix/feed/',
		'http://www.kgns.tv/home/headlines/index.rss2',
		'http://kttz.org/rss.xml',
		'http://www.kcbd.com/category/216452/kpho-newstream?clienttype=rss',
		'http://feeds.feedburner.com/ktre/aABF?format=xml',
		'http://www.ksat.com/feeds/rssFeed/feedServlet?obfType=GMG_RSS_DETAIL&siteId=800001&nbRows=20&FeedFetchDays=180&categoryId=80041',
		'http://feedsyn.univision.com/univision41',
		'http://www.telemundosanantonio.com/noticias/local/?rss=y&embedThumb=y&summary=y',
		'http://www.kltv.com/Global/category.asp?C=7845&clienttype=rss',
		'http://www.cbs19.tv/Global/category.asp?C=137100&clienttype=rss',
		'http://www.kcentv.com/Global/category.asp?C=170050&clienttype=rss',
		'http://www.kxxv.com/Global/category.asp?C=84199&clienttype=rss',
		'http://www.abc40.com/Global/category.asp?C=85376&clienttype=rss',
		'http://www.foxrio2.com/category/news/feed/',
		'http://ktemnews.com/category/news/local-news/feed/',
		'http://1470kyyw.com/category/local-news/feed/',
		'http://radioabilene.com/?feed=rss2',
		'http://newstalk1290.com/category/local-news/feed/',
		'http://wtaw.com/category/news/feed/',
		'http://kfyo.com/feed/',
		'http://voiceofamarillo.com/feed/',
		'http://ksfa860.com/feed/',
		'http://www.ktsa.com/feed/',
		'http://www.kurv.com/category/local/feed/',
		'http://www.thebatt.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
		'http://baylorlariat.com/category/news/feed/',
		'http://thedailycougar.com/news/feed/',
		'http://www.dailytexanonline.com/rss/articles/all',
		'http://houstonianonline.com/category/news/feed/',
		'http://ntdaily.com/feed/',
		'http://www.thepacer.net/category/news/campus-local/feed/',
		'http://paisano-online.com/news-cat/city/feed/',
		'http://www.asurampage.com/rss.php',
		'http://www.ricethresher.org/section/homepage.xml',
		'http://www.reporternews.com/feeds/rss/news',
		'http://www.alicetx.com/news?template=rss&mime=xml',
		'http://amarillo.com/taxonomy/term/174/2/feed',
		'http://baytownsun.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
		'http://www.beaumontenterprise.com/home/collectionRss/Home-Heds-News-7272.php',
		'http://bigspringherald.com/rss.xml',
		'http://www.borgernewsherald.com/rss.xml',
		'http://www.brenhambanner.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
		'http://www.brownsvilleherald.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
		'http://www.brownwoodtx.com/news?template=rss&mime=xml',
		'http://www.yourhoustonnews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=dayton*&f=rss',
		'http://www.caller.com/news/local/index.rss',
		'http://dailysentinel.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local&f=rss',
		'http://www.dallasnews.com/?rss',
		'http://delrionewsherald.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
		'http://www.dentonrc.com/local-news/?rss',
		'http://rssfeeds.elpasotimes.com/elpaso/news&x=1',
		'http://focusdailynews.com/clients/focusdailynews/headlines.rss',
		'http://www.fbherald.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news&f=rss',
		'http://www.star-telegram.com/news/local/?widgetName=rssfeed&widgetContentId=714290&getXmlFeed=true',
		'http://www.galvnews.com/search/?t=article&c[]=news/local*%2Cnews/edu*%2Cnews/pol*&f=rss',
		'http://www.hendersondailynews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
		'http://heralddemocrat.com/taxonomy/term/2/feed',
		'http://www.chron.com/rss/feed/News-270.php',
		'http://dailytimes.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news&f=rss',
		'http://www.kilgorenewsherald.com/news.xml',
		'http://kdhnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
		'http://www.lmtonline.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=front-news*&f=rss',
		'http://www.news-journalonline.com/rss/articles/101023/10',
		'http://lufkindailynews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local&f=rss',
		'http://www.marshallnewsmessenger.com/news/local/rss/',
		'http://www.mrt.com/rss/',
		'http://www.themonitor.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
		'http://www.dailytribune.net/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
		'http://herald-zeitung.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news&f=rss&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=community_alert,community_alert/*&f=rss',
		'http://www.oaoa.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
		'http://theparisnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
		'http://www.myplainview.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
		'http://www.gosanangelo.com/feeds/rss/news',
		'http://www.mysanantonio.com/default/feed/local-news-176.php',
		# 'http://www.sanmarcosrecord.com/rss.xml',
		'http://seguingazette.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
		'http://www.sweetwaterreporter.com/rss.xml',
		'http://taylorpress.net/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news&f=rss',
		'http://www.tdtnews.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
		'http://www.timesrecordnews.com/news/local/index.rss',
		'http://www.tylerpaper.com/',
		'http://www.valleymorningstar.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local_news,news/local_news/*&f=rss',
		'http://www.victoriaadvocate.com/news/local-news/rss/',
		'http://www.wacotrib.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss'
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
					d.feed.published
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
			location = "TX"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			