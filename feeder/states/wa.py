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
		'http://keprtv.com/news/local.rss',
		'http://www.nbcrightnow.com/global/category.asp?c=78263&clienttype=rss',
		'http://komonews.com/news/local.rss',
		'http://rssfeeds.king5.com/king5/local',
		'http://q13fox.com/feed/',
		'http://rssfeeds.krem.com/krem/local&x=1',
		'http://www.kxly.com/news/101270?format=rss_2.0&view=feed',
		'http://www.khq.com/category/73323/home?clienttype=rss',
		'http://kimatv.com/news/local.rss',
		'http://kbkw.com/feed/',
		'http://newstalk870.am/feed/',
		'http://kgmi.com/news/sections/local/feed',
		'http://mynorthwest.com/xml/11.xml',
		'http://newstalkkit.com/feed/',
		'http://kpq.com/feed/',
		'http://www.kxly.com/news/101270?format=rss_2.0&view=feed',
		'http://komonews.com/news/local.rss',
		'http://spokanepublicradio.org/feeds/term/36/rss.xml',
		'http://www.seattletimes.com/seattle-news/feed/',
		'http://www.bellinghamherald.com/news/local/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
		'http://www.theolympian.com/news/local/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
		'http://www.thenewstribune.com/news/local/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
		'http://www.tri-cityherald.com/news/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
		'http://tdn.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
		'http://www.thestranger.com/seattle/Rss.xml?section=226',
		'http://www.seattlepi.com/local/feed/seattlepi-com-Local-News-218.php',
		'http://www.kitsapsun.com/feeds/rss/news/local',
		'http://www.spokesman.com/feeds/stories/news/',
		'http://www.columbian.com/news/local/',
		'http://thedailyworld.com/news/local/feed',
		'http://www.heraldnet.com/section/RSS02&mime=xml'		


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
			location = "WA"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()
