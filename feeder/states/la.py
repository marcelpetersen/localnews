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
			'http://klax-tv.com/category/localheadlines/feed/',
			'http://www.wbrz.com/feeds/rssfeed.cfm?category=58&cat_name=News',
			'http://klfy.com/category/news/local/feed/',
			'http://www.kplctv.com/category/216452/kpho-newstream?clienttype=rss',
			'http://www.knoe.com/home/headlines/index.rss2',
			'http://www.kalb.com/home/headlines/index.rss2',
			'http://rssfeeds.wwltv.com/wwl/local&x=1',
			'http://www.wdsu.com/9854384?format=rss_2.0&view=feed',
			'http://www.fox8live.com/category/235041/local-news?clienttype=rss',
			'http://wgno.com/category/news/feed/',
			'http://rssfeeds.kgw.com/kgw/local',
			'http://www.ksla.com/global/Category.asp?c=50833&clienttype=rss',
			'http://kpel965.com/feed/',
			'http://710keel.com/feed/',
			'http://rssfeeds.thetowntalk.com/alexandria/news&x=1',
			'http://www.bastropenterprise.com/news?template=rss&mime=xml',
			'http://theadvocate.com/feed?feedName=News&feedURL=http://theadvocate.com/news/&publication=Advocate&sections=/news/&areas=Stories&counts=20&feedContentPage=/shared/templates/feeds/rss2.csp',
			'http://bossierpress.com/category/news/feed/',
			'http://www.weeklycitizen.com/news?template=rss&mime=xml',
			'http://www.hammondstar.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.houmatoday.com/rss/articles/ARTICLES/1211/30',
			'http://rssfeeds.theadvertiser.com/lafeyettela/news&x=1',
			'http://www.americanpress.com/news/local/rss/',
			'http://www.leesvilledailyleader.com/news?template=rss&mime=xml',
			'http://press-herald.com/category/news/feed/',
			'http://rssfeeds.thenewsstar.com/monroe/news&x=1',
			'http://blog.nola.com/nola_river_baton_rouge_news/atom.xml',
			'http://blog.nola.com/eastjefferson/atom.xml',
			'http://blog.nola.com/new_orleans/atom.xml',
			'http://blog.nola.com/plaquemines/atom.xml',
			'http://blog.nola.com/river/atom.xml',
			'http://blog.nola.com/stbernard/atom.xml',
			'http://blog.nola.com/st-tammany-community_impact/atom.xml',
			'http://blog.nola.com/westbank/atom.xml',
			'http://www.postsouth.com/news?template=rss&mime=xml',
			'http://rssfeeds.dailyworld.com/opelousas/news&x=1',
			'http://rssfeeds.shreveporttimes.com/shreveport/news&x=1',
			'http://www.sulphurdailynews.com/news?template=rss&mime=xml',
			'http://www.lsunow.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.thetechtalk.org.php5-24.dfw1-2.websitetestlink.com/feed/',
			'http://www.tulanehullabaloo.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://thevermilion.com/category/news/feed/',
			'http://www.dailycomet.com/rss/articles/ARTICLES/1212/30',
			'http://rustonleader.com/rss.xml'

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
			location = "LA"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			