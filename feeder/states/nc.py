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
			'http://wlos.com/news/local.rss',
			'http://www.wbtv.com/Global/category.asp?C=128868&clienttype=rss',
			'http://www.whky.com/archive?format=feed',
			'http://www.wccbcharlotte.com/feed/',
			'http://rssfeeds.wcnc.com/wcnc/local&x=1',
			'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=RSS_FEED&siteId=200005&categoryid=100003',
			'http://rssfeeds.wfmynews2.com/wfmynews2-local&x=1',
			'http://myfox8.com/category/news/feed/',
			'http://www.wxii12.com/9678710?format=rss_2.0&view=asFeed',
			'http://www.witn.com/news/headlines/index.rss2',
			'http://www.wcti12.com/14413318?format=rss_2.0&view=feed',
			'http://wnct.com/category/news/local-news/feed/',
			'http://www.wcti12.com/14413318?format=rss_2.0&view=feed',
			'http://www.wral.com/news/rss/142/',
			'http://abc11.com/feed/',
			'http://wncn.com/category/news-raleigh-durham-fayetteville-north-carolina/wncn-local-news/feed/',
			'http://www.wwaytv3.com/news/feed/',
			'http://www.foxwilmington.com/category/79461/local-news?clienttype=rss',
			'http://www.wect.com/category/216452/kpho-newstream?clienttype=rss',
			'http://www.wsicweb.com/category/wsicnews/feed/',
			'http://www.wfnc640am.com/news/feed/',
			'http://wfae.org/feeds/term/32/rss.xml',
			'http://www.dailytarheel.com/section/pageOne.xml',
			'http://courier-tribune.com/news/local/feed',
			'http://www.cherokeescout.com/rss.xml',
			'http://www.newsobserver.com/news/?widgetName=rssfeed&widgetContentId=8173866&getXmlFeed=true',
			'http://www.myandrewsjournal.com/rss.xml',
			'http://rssfeeds.citizen-times.com/asheville/local',
			'http://www.charlotteobserver.com/news/local/?widgetName=rssfeed&widgetContentId=8167599&getXmlFeed=true',
			'http://www.gastongazette.com/news?template=rss&mime=xml',
			'http://pilotmountainnews.com/feed',
			'http://jeffersonpost.com/category/news/feed',
			'http://www.kinston.com/news?template=rss&mime=xml',
			'http://www.lincolntimesnews.com/category/local-news/feed/',
			'http://maconcountytimes.com/feed',
			'http://mtairynews.com/category/news/feed',
			'http://mountainx.com/news/feed/',
			'http://www.newsoforange.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.hickoryrecord.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.hcpress.com/news/feed/',
			'http://www.jdnews.com/news?template=rss&mime=xml',
			'http://www.dispatch.com/content/syndication/news_local-state.xml',
			'http://www.gastongazette.com/news?template=rss&mime=xml',
			'http://www.greensboro.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local,news/crime,news/goverment,news/schools,news/rockingham_county,news/local,news/crime,news/goverment,news/schools,news/rockingham_county/*&f=rss',
			'http://www.salisburypost.com/category/news/local/feed/',
			'http://www.shelbystar.com/news?template=rss&mime=xml',
			'http://www.starnewsonline.com/rss/articles/NEWS/1004/30',
			'http://www.newbernsj.com/news?template=rss&mime=xml',
			'http://www.blueridgenow.com/rss/articles/NEWS/1042/50?encoding=utf-8&mime=xml/&fulltext=1',
			'http://www.thetimesnews.com/news?template=rss&mime=xml',
			'http://elkintribune.com/feed',
			'http://www.wataugademocrat.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.journalpatriot.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.wilsontimes.com/RSS/LocalNews/',
			'http://yadkinripple.com/feed',
			'http://www.journalnow.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',

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
					imageUrl = ''

			source = d.feed.title
			location = "NC"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			