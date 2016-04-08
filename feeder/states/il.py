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
		'http://www.wsiltv.com/category/301474/news?clienttype=rss',
		'http://www.wpsdlocal6.com/category/280445/local-news?clienttype=rss',
		'http://www.kfvs12.com/category/2804/home?clienttype=RSS',
		'http://foxillinois.com/news/local.rss',
		'http://www.nbcchicago.com/news/local/?rss=y&embedThumb=y&summary=y',
		'http://abc7chicago.com/feed/',
		'http://wgntv.com/category/news/feed/',
		'http://feedsyn.univision.com/univisionchicago',
		'http://feeds.feedburner.com/chicagotonight?format=xml',
		'http://www.telemundochicago.com/noticias/local/?rss=y&embedThumb=y&summary=y',
		'http://www.wandtv.com/Global/category.asp?C=99886&clienttype=rss',
		'http://www.cinewsnow.com/news/local/index.rss2',
		'http://khqa.com/news/local.rss',
		'http://www.wgem.com/category/134874/mobile-news?&clienttype=rss',
		'http://kwqc.com/feed/',
		'http://wqad.com/category/news/feed/',
		'http://www.wrex.com/Global/category.asp?C=195914&clienttype=rss',
		'http://www.wifr.com/news/headlines/index.rss',
		'http://newschannel20.com/news/local.rss',
		'http://chicago.cbslocal.com/category/news/feed/',
		'http://1440wrok.com/feed/',
		'http://www.am1250wspl.com/category/localheadlines/feed/',
		'http://wtax.com/feed/',
		'http://news.983talk.com/feed/',
		'http://wzoe.com/feed/',
		'http://wglt.org/feeds/news/rss.xml',
		'http://www.wfiwradio.com/feed/',
		'http://www.wgil.com/category/news/local-news/feed/',
		'http://www.wgfaradio.com/newsite/index.php?option=com_content&view=category&layout=blog&id=53&Itemid=106&format=feed&type=rss',
		'http://www.wjol.com/feed/',
		'http://www.wjbc.com/category/local-news/feed/',
		'http://wgnradio.com/category/news/feed/',
		'http://www.news-gazette.com/news/local/feed.xml',
		'http://www.wmix94.com/feed/',
		'http://www.effinghamradio.com/local-news/feed/',
		'http://northernpublicradio.org/feeds/term/9/rss.xml',
		'http://northernstar.info/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=city*,city*/*&f=rss',
		'http://www.loyolaphoenix.com/category/news/feed/',
		'http://depauliaonline.com/topics/news/feed/',
		'http://dailynorthwestern.com/feed/',
		'http://www.dailyillini.com/servlet/feed/daily-illini-main-feed',
		'http://www.dailyegyptian.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
		'http://www.columbiachronicle.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news_wire*&f=rss',
		'http://chicagomaroon.com/category/news/feed/',
		'http://www.reviewatlas.com/news?template=rss&mime=xml',
		'http://www.duquoin.com/news?template=rss&mime=xml',
		'http://www.theintelligencer.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=local_news,local_news/*&f=rss',
		'http://www.daily-journal.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local,news/local/*&f=rss',
		'http://www.pontiacdailyleader.com/section/feed',
		'http://www.cantondailyledger.com/news?template=rss&mime=xml',
		'http://www.dailyregister.com/news?template=rss&mime=xml',
		'http://www.dailyrepublicannews.com/news?template=rss&mime=xml',
		'http://www.news-gazette.com/news/local/feed.xml',
		'http://www.dailyherald.com/rss/feed/?feed=news_local',
		'http://www.daily-chronicle.com/?rss=news/local',
		'http://www.advocatepress.com/news?template=rss&mime=xml',
		'http://chicagodefender.com/category/news/city/feed/',
		'http://www.chicagoreader.com/chicago/Rss.xml?section=846996',
		'http://www.carmitimes.com/news?template=rss&mime=xml',
		'http://rvpnews.com/?feed=rss2',
		'http://www.bentoneveningnews.com/news?template=rss&mime=xml',
		'http://feeds.feedburner.com/chicagotribune/news',
		'http://newstrib.com/28_rss.xml',
		'http://www.nwherald.com/?rss=news/local',
		'http://www.olneydailymail.com/news?template=rss&mime=xml',
		'http://www.pantagraph.com/search/?f=rss&t=article&c=news/local*&l=25&s=start_time&sd=desc',
		'http://www.parisbeacon.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
		'http://www.pekintimes.com/news?template=rss&mime=xml',
		'http://www.galesburg.com/news?template=rss&mime=xml',
		'http://www.robdailynews.com/2_rss.xml',
		'http://www.morrisherald-news.com/?rss=news',
		'http://jg-tc.com/search/?f=rss&c[]=news/local&sd=desc&s=start_time',
		'http://www.journalstandard.com/news?template=rss&mime=xml',
		'http://www.pjstar.com/news?template=rss&mime=xml',
		'http://www.kcchronicle.com/?rss=news/local',
		'http://www.lincolncourier.com/news?template=rss&mime=xml',
		'http://www.mcdonoughvoice.com/news?template=rss&mime=xml',
		'http://www.windycitymediagroup.com/feedmaker.php',
		'https://thetelegraph.com/feed',
		'http://thesouthern.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
		'http://www.starcourier.com/news?template=rss&mime=xml',
		'http://www.sj-r.com/section/feed',
		'http://www.rrstar.com/news?template=rss&mime=xml',
		'http://myjournalcourier.com/feed',
		'http://www.oakpark.com/RSS/',
		'http://www.mysuburbanlife.com/?rss=news/local',
		'http://hpherald.com/feed/',
		'http://illinoistimes.com/rss-30-1-news.xml',
		'http://rockrivertimes.com/category/news/local-news/feed/',
		'http://www.marengo-uniontimes.com/news?format=feed&type=rss',
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
			location = "IL"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			