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
			'http://www.komu.com/feeds/rssfeed.cfm?category=5&cat_name=News',
			'http://krcgtv.com/news/local.rss',
			'http://www.abc17news.com/18420526?format=rss_2.0&view=feed',
			'http://khqa.com/news/local.rss',
			'http://fox4kc.com/category/news/feed/',
			'http://www.kctv5.com/category/210833/app-news?clienttype=rss',
			'http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?obfType=RSS_FEED&siteId=10014&categoryId=20000',
			'http://www.kctv5.com/category/210833/app-news?clienttype=rss',
			'http://ktvo.com/news/local.rss',
			'http://fox2now.com/category/news/feed/',
			'http://www.kmov.com/category/216452/kpho-newstream?clienttype=rss',
			'http://rssfeeds.kgw.com/kgw/local&x=1',
			'http://kplr11.com/category/news/feed/',
			'http://abcstlouis.com/news/local.rss',
			'http://www.ky3.com/news/local/21048998_21049004?format=rss_2.0&view=feed',
			'http://www.kspr.com/news/local/21051620_21051626?format=rss_2.0&view=feed',
			'http://www.fox5krbk.com/category/news/local-news/feed/',
			'http://www.kttn.com/category/news/feed/',
			'http://www.ozarkareanetwork.com/feed/',
			'http://www.centralmoinfo.com/category/big-k-news/feed/',
			'http://kwos.com/feed/',
			'http://www.myozarksonline.com/category/state-and-local-news/feed/',
			'http://www.newstalkkzrg.com/category/state-and-local-news/feed/',
			'http://www.kzimksim.com/category/news/local-news/feed/',
			'http://www.krmsradio.com/category/local/feed/',
			'http://stlouis.cbslocal.com/category/news/feed/',
			'http://khmoradio.com/feed/',
			'http://www.myozarksonline.com/category/state-and-local-news/feed/',
			'http://ksisradio.com/category/news/feed/',
			'http://www.680kfeq.com/category/news/feed/',
			'http://www.boonvilledailynews.com/news?template=rss&mime=xml',
			'http://www.bowlinggreentimes.com/feed/',
			'http://www.californiademocrat.com/rss/headlines/local/',
			'http://www.lakenewsonline.com/news?template=rss&mime=xml',
			'http://www.semissourian.com/feed/rss/all/today.rss',
			'http://www.carthagepress.com/news?template=rss&mime=xml',
			'http://www.chillicothenews.com/news?template=rss&mime=xml',
			'http://www.columbiamissourian.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/local,news/local/*&f=rss',
			'http://dailyjournalonline.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.hannibal.net/news?template=rss&mime=xml',
			'http://www.examiner.net/news?template=rss&mime=xml',
			'http://www.newstribune.com/rss/headlines/local/',
			'http://www.joplinglobe.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.kirksvilledailyexpress.com/news?template=rss&mime=xml',
			'http://www.lebanondailyrecord.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.marshallnews.com/feed/rss/news/week.rss',
			'http://www.maryvilledailyforum.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.mexicoledger.com/news?template=rss&mime=xml',
			'http://www.moberlymonitor.com/news?template=rss&mime=xml',
			'http://www.neoshodailynews.com/news?template=rss&mime=xml',
			'http://www.therolladailynews.com/news?template=rss&mime=xml',
			'http://sedaliademocrat.com/category/news/feed',
			'http://www.stltoday.com/search/?c=news%2Flocal,news%2flocal%2f*&d1=&d2=&s=start_time&sd=desc&l=50&f=rss&t=article,html,collection,link',
			'http://rssfeeds.news-leader.com/springfield/home',
			'http://www.republictimes.net/category/breaking-news/feed/',
			'http://www.dailystarjournal.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.waynesvilledailyguide.com/news?template=rss&mime=xml'
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
					imageUrl = ''

			source = d.feed.title
			location = "MO"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			