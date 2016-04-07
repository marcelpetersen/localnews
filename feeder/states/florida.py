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
		'http://cbs12.com/news/local.rss',
		'http://weartv.com/news/local.rss',
		'http://mygtn.tv/news/local.rss',
		'http://www.winknews.com/feed/',
		'http://news.wgcu.org/feeds/term/114/rss.xml',
		'http://www.wuft.org/feed/',
		'http://www.news4jax.com/feeds/rssFeed/feedServlet?obfType=GMG_RSS_DETAIL&siteId=800004&categoryId=80041&nbRows=20&FeedFetchDays=10&includeFeeds=True',
		'http://rssfeeds.firstcoastnews.com/firstcoastnews-local&x=1',
		'http://miami.cbslocal.com/feed/',
		'http://www.nbcmiami.com/news/local/?rss=y&embedThumb=y&summary=y',
		'http://www.wsvn.com/?clienttype=rss',
		'http://www.local10.com/feeds/rssFeed/feedServlet?obfType=GMG_RSS_APP&siteId=800006&categoryId=80041&nbRows=10',
		'http://wlrn.org/feeds/term/61/rss.xml',
		'http://feedsyn.univision.com/univision23',
		'http://sflcw.com/feed/',
		'http://www.telemundo51.com/noticias/local/?rss=y&embedThumb=y&summary=y',
		'http://www.wesh.com/11789118?format=rss_2.0&view=feed',
		'http://www.clickorlando.com/feeds/rssFeed/feedServlet?obfType=GMG_RSS_DETAIL&siteId=800005&categoryId=80041&nbRows=20&FeedFetchDays=10&includeFeeds=True',
		'http://www.wesh.com/11789118?format=rss_2.0&view=feed',
		'http://www.wucftv.org/rss/',
		'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=RSS_FEED&siteId=200014',
		'http://www.wjhg.com/home/headlines/index.rss2',
		'http://news.wfsu.org/rss.xml',
		'http://ww2.wkrg.com/category/249151/news?clienttype=rss',
		'http://www.fox10tv.com/category/78813/news?clienttype=rss',
		'http://www.wctv.tv/home/headlines/index.rss',
		'http://wfla.com/feed/',
		'http://rssfeeds.wtsp.com/wtsp/localnews&x=1',
		'http://wusfnews.wusf.usf.edu/rss.xml',
		'http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?siteId=10010&obfType=RSS_FEED&categoryId=20000',
		'http://wfla.com/feed/',
		'http://www.mysuncoast.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
		'http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?obfType=RSS_FEED&siteId=10016&categoryId=20000',
		'http://www.wpbf.com/8789800?format=rss_2.0&view=feed',
		'http://www.wflx.com/Global/category.asp?C=104655&&clienttype=rss',
		'http://www.cwtv.com/feed/episodes/xml',
		'http://www.wengradio.com/category/news/feed/',
		'http://www.850wftl.com/feed/',
		'http://www.newsdaytonabeach.com/feed/',
		'http://www.wokv.com/feeds/categories/news/',
		'http://unfspinnaker.com/feed/',
		'http://www.usforacle.com/rss.php',
		'http://www.themiamihurricane.com/section/news/feed/',
		'http://www.dailycommercial.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
		'http://www.news-journalonline.com/rss/articles/101023/10',
		'http://www.sun-sentinel.com/news/rss2.0.xml',
		'http://feeds.jacksonville.com/JacksonvillecomNews?format=xml',
		'http://rssfeeds.floridatoday.com/brevard/news&x=1',
		'http://www.gainesville.com/rss/articles/NEWS/1002/30',
		'http://hernandotoday.com/news/feed/',
		'http://www.lakecityreporter.com/rss.xml',
		'http://courrierdefloride.com/feed/',
		'http://www.theledger.com/rss/articles/NEWS/1338/30',
		'http://www.miamiherald.com/news/?widgetName=rssfeed&widgetContentId=712015&getXmlFeed=true',
		'http://www.naplesnews.com/news/local/index.rss',
		'http://www.browardpalmbeach.com/news.rss'
		'http://www.miaminewtimes.com/news.rss',
		'http://www.newsherald.com/news?template=rss&mime=xml',
		'http://rssfeeds.news-press.com/ftmyers/news&x=1',
		'http://www.nwfdailynews.com/news?template=rss&mime=xml',
		'http://feeds.feedburner.com/orlandosentinel/news',
		'http://www.orlandoweekly.com/orlando/Rss.xml?section=2240408',
		'http://www.aroundosceola.com/feed/',
		'http://www.palmbeachdailynews.com/feeds/categories/news/',
		'http://www.palmbeachpost.com/feeds/categories/news/',
		'http://rssfeeds.pnj.com/pensacola/news&x=1',
		'http://www.tcpalm.com/news/index.rss',
		'http://staugustine.com/taxonomy/term/133/0/feed',
		'http://www.heraldtribune.com/rss/articles/article/2055/10',
		'http://www.ocala.com/rss/articles/NEWS/1356/30',
		# 'http://rssfeeds.tallahassee.com/tallahassee/news',
		'http://www.tampabay.com/feeds/rss.page?collatedTag=breaking-news&section=staffArticle&feedType=rss',
		'http://www.jacksoncountytimes.net/local-news.feed'		

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
			location = "FL"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			