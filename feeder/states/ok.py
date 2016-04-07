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

	url = ('http://www.news9.com/category/211667/news9com-news-rss?clienttype=rss',
			'http://www.koco.com/9844956?format=rss_2.0&view=feed',
			'http://www.kswo.com/category/216452/kpho-newstream?clienttype=rss'
			'http://ktul.membercenter.worldnow.com/global/category.asp?C=189710&clienttype=rss',
			'http://ktul.membercenter.worldnow.com/global/category.asp?C=189711&clienttype=rss,'
			'http://www.newson6.com/category/208401/newson6com-news-rss?clienttype=rss',
			'http://www.fox23.com/feeds/rssFeed?obfType=RSS_DETAIL&siteId=600013&categoryId=500001',
			'http://www.krmg.com/list/rss/news/local/top-local-stories/aPM/',
			'http://publicradiotulsa.org/feeds/term/49/rss.xml',   
			'http://www.choctawnation.com/rss',
			'http://www.tulsaworld.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss', 
			'http://www.baptistmessenger.com/feed/',
			'http://okmulgeenews.net/local-news?format=feed',
			'http://swoknews.com/rss.xml',
			'http://www.woodwardnews.net/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local_news,news/local_news/*&f=rss',
			'http://www.miamiok.com/news?template=rss&mime=xml',
			'http://www.ardmoreite.com/news?template=rss&mime=xml',
			'http://examiner-enterprise.com/news/local-news/feed',
			'http://www.ocolly.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.oudaily.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/state*&f=rss',
			'http://www.news-star.com/news?template=rss&mime=xml',
			'http://feeds.feedburner.com/ktenlocalnews?format=xml',
			'http://feeds.feedburner.com/Newsok/home',
			'http://www.kxii.com/news/headlines/index.rss',
			# 'http://www.newschannel6now.com/category/179961/news?clienttype=rss',
			'http://www.news-star.com/news?template=rss&mime=xml',
			'http://altustimes.com/category/news/feed',
			'http://durantdemocrat.com/feed',
			'http://www.yourokmulgee.com/taxonomy/term/6/feed',
			'http://www.yourokmulgee.com/taxonomy/term/2/feed',
			'http://www.henryettafree-lance.com/taxonomy/term/2/feed',
			'http://www.hugonews.com/feed/',
			'https://chickasaw.net/News/RSS/Press-Release-RSS-Feed.aspx',
			'http://journalrecord.com/feed/',
			'http://www.alvareviewcourier.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://city-sentinel.com/feed/',
			'http://www.sequoyahcountytimes.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.sequoyahcountytimes.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=sports,sports/*&f=rss',
			'http://www.grandlakenews.com/news?template=rss&mime=xml',
			'http://www.grandlakenews.com/sports?template=rss&mime=xml',
			'http://www.elrenotribune.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://mustangnews.net/feed/',
			'http://www.purcellregister.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://feeds.feedburner.com/Newsok/news/local',
			'http://www.cherokee.org/GenerateRSS.aspx',
			'http://okgazette.com/category/news/state/feed/',
			'http://www.stwnewspress.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.enidnews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.muskogeephoenix.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.mcalesternews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.normantranscript.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.duncanbanner.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.pryordailytimes.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.claremoreprogress.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.edmondsun.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://tucollegian.org/category/news/feed/',
						)

	for link in url:
		d = feedparser.parse(link)

		for data in d.entries:


			title = data.title
			link = data.link
			try:
				time = data.published
			except AttributeError:
				time = d.feed.published
			try: 
				imageUrl = data.links[1].href
			except IndexError: 
				try:
					imageUrl = data.media_content[0]['url']
				except AttributeError:
					imageUrl = 'http://polar-spire-13485.herokuapp.com/static/img/logo3.png'

			source = d.feed.title
			location = "OK"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			