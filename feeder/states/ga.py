
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

	url = ('http://www.walb.com/global/Category.asp?C=1687&clienttype=rss',
			'http://www.walb.com/global/Category.asp?C=1689&clienttype=rss',
			'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=VERVE_RSS_FEED&siteId=200003&categoryId=100000',
			'http://rssfeeds.11alive.com/wxia-local',
			'http://www.cbs46.com/category/162901/ap-news-center?clienttype=rss',
			'http://wjbf.com/category/news/feed/',
			'http://feeds.feedburner.com/news12topstories',
			'http://wrbl.com/category/news/local-news/feed/',
			'http://www.wtvm.com/category/216452/kpho-newstream?clienttype=rss',
			'http://www.wxtx.com/category/216452/kpho-newstream?clienttype=rss',
			'http://wgxa.tv/news/local.rss',
			'http://www.41nbc.com/category/local-news/feed/',
			'http://wsav.com/category/news/georgia-news/feed/',
			'http://www.wtoc.com/category/203681/news-local?clienttype=rss',
			'http://www.wctv.tv/home/headlines/index.rss',
			'http://valdostatoday.com/category/news-2/local/feed/',
			'http://wgac.com/feed/',
			'http://www.newsradio1067.com/category/local-news/feed/',
			'http://www.wsbradio.com/feeds/categories/news/',
			'http://atlanta.cbslocal.com/category/news/feed/',
			'http://crossroadsnews.com/rss/headlines/general-news/',
			'http://fanninsentinel.com/?feed=rss2',
			'http://www.earlycountynews.com/news.xml',
			'http://lagrangenews.com/feed',
			'http://www.ledger-enquirer.com/news/local/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
			'http://www.covnews.com/syndication/feeds/rss/1/',
			'http://www.theclaytontribune.com/rss.xml',
			'http://onlineathens.com/taxonomy/term/4691/2/feed',
			'http://atlantadailyworld.com/category/adw-news/feed/',
			'http://www.ajc.com/list/rss/news/breaking-news-center/aFSL/',
			'http://feeds.feedburner.com/augusta/latestnews?format=xml',
			'http://www.theblacksheartimes.com/search/?f=rss&t=article&c=news',
			'http://www.thebrunswicknews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local_news*&f=rss',
			'http://www.covnews.com/syndication/feeds/rss/1/',
			'http://www.northwestgeorgianews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=rome,rome/*&f=rss',
			'http://savannahnow.com/taxonomy/term/2099/0/feed',
			'http://www.statesboroherald.com/syndication/feeds/rss/1/',
			'http://nique.net/category/news/feed/',
			'http://www.macon.com/news/local/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
			'http://www.timesenterprise.com/search/?f=rss&',
			'http://www.tiftongazette.com/search/?f=rss&',
			'http://wjhnews.com/feed/',
			'http://www.morgancountycitizen.com/category/news/feed/',
			'http://www.moultrieobserver.com/search/?f=rss&t',
			'https://feeds.feedblitz.com/porthuron/news',
			
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
			location = "GA"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			