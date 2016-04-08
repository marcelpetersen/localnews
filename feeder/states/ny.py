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
			'http://news10.com/feed/',
			'http://wnyt.com/rssFeeds/rss10114.xml',
			'http://fox23news.com/',
			'http://www.wbng.com/news/local/index.rss2',
			'http://www.wicz.com/localnewsrss.asp',
			'http://rssfeeds.wgrz.com/wgrz/top-stories&x=1',
			'http://wivb.com/feed/',
			'http://newyork.cbslocal.com/category/news/feed/',
			'http://feedsyn.univision.com/univisionnuevayork',
			'http://www.nbcnewyork.com/news/local/?rss=y&embedThumb=y&summary=y',
			'http://abc7ny.com/feed/',
			'http://pix11.com/category/local-stories/feed/',
			'http://www.telemundo47.com/noticias/local/?rss=y&embedThumb=y&summary=y',
			'http://www.wcax.com/category/18197/localnews?clienttype=rss',
			'http://www.wptz.com/8870862?format=rss_2.0&view=asFeed',
			'http://www.whec.com/rssFeeds/rss565.xml',
			'http://13wham.com/news/local.rss',
			'http://foxrochester.com/news/local.rss',
			'http://cnycentral.com/news/local.rss',
			'http://www.wktv.com/news/local/index.rss2',
			'http://www.wwnytv.com/news/local/index.rss2',
			'http://cbs6albany.com/news/local.rss',
			'http://wxxinews.org/rss.xml',
			'http://wnbf.com/category/local-news/feed/',
			'http://www.amny.com/cmlink/1.2427115',
			'http://auburnpub.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.dailyfreeman.com/section?template=RSS&profile=4003275&mime=xml',
			'http://www.dailygazette.com/rss/headlines/local/',
			'http://www.mpnnow.com/news?template=rss&mime=xml',
			'http://rssfeeds.democratandchronicle.com/democratandchronicle/news&x=1',
			'http://www.theepochtimes.com//n3/c/nyc/ny-news/feed/',
			'http://www.timestelegram.com/news?template=rss&mime=xml',
			'http://rssfeeds.ithacajournal.com/ithaca/home',
			'http://rssfeeds.lohud.com/westchester/news&x=1',
			'http://www.the-leader.com/news?template=rss&mime=xml',
			'http://www.leaderherald.com/page/syndrss.front/headline.xml',
			'http://www.metro.us/rss.xml?c=1414044023-4',
			'http://feeds.nydailynews.com/NydnRss?format=xml',
			'http://feeds.feedblitz.com/nylj-news&x=1',
			'http://nypost.com/news/feed/',
			'http://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml',
			'http://www.newsday.com/cmlink/1.1284724',
			'http://www.observertoday.com/page/syndrss.front/headline.xml',
			'http://www.uticaod.com/news?template=rss&mime=xml',
			'http://www.oleantimesherald.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news&f=rss',
			'http://www.post-journal.com/page/syndrss.front/headline.xml',
			'http://blog.syracuse.com/news/atom.xml',
			'http://rssfeeds.poughkeepsiejournal.com/poughkeepsie/news&x=1',
			'http://rssfeeds.pressconnects.com/binghamton/home&x=1',
			'http://www.troyrecord.com/section?template=RSS&profile=4004092&mime=xml',
			'http://www.registerstar.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.salamancapress.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.saratogian.com/section?template=RSS&profile=4004091&mime=xml',
			'http://rssfeeds.stargazette.com/elmira/home',
			'http://blog.silive.com/latest_news/atom.xml',
			'http://www.recordonline.com/news?template=rss&mime=xml',
			'http://www.timesunion.com/default/feed/Breaking-News-240.php',
			'http://www.wsj.com/xml/rss/3_7085.xml',
			'http://www.nyunews.com/feed/',
			'http://www.wellsvilledaily.com/news?template=rss&mime=xml',
			'http://www.oneidadispatch.com/section?template=RSS&profile=4003837&mime=xml',
			'http://oswegocountytoday.com/feed/',
			'http://observer.com/feed/',
			'http://www.bxtimes.com/assets/feeds/rss.x'
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
			location = "NY"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			