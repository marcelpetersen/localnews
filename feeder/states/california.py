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

	url = ('http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?obfType=RSS_FEED&siteId=100001&categoryId=20000',
			'http://www.krcrtv.com/14774432?format=rss_2.0&view=feed',
			'http://www.actionnewsnow.com/feeds/rssfeed.cfm?category=1088&cat_name=News%20-%20Local',
			'http://noticias.entravision.com/el-centro/feed/',
			'http://yourtvfamily.com/feed/',
			'http://feedsyn.univision.com/univision34',
			'http://www2.yourcentralvalley.com/rss/2692.rss',
			'http://abc30.com/feed/',
			'http://www.nbclosangeles.com/news/local/?rss=y&embedThumb=y&summary=y',
			'http://ktla.com/category/news/local-news/feed/',
			'http://ktla.com/category/sports/feed/',
			'http://abc7.com/feed/',
			'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=VERVE_RSS_FEED&siteId=200010&categoryId=100001',
			'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=VERVE_RSS_FEED&siteId=200010&categoryId=100006',
			'http://www.telemundo52.com/noticias/local/?rss=y&embedThumb=y&summary=y',
			'http://www.kesq.com/7625978?format=rss_2.0&view=feed',
			'http://www.kcra.com/11798330?format=rss_2.0&view=feed',
			'http://www.kcra.com/11798354?format=rss_2.0&view=feed',
			'http://feeds.feedblitz.com/news10-news',
			'http://sacramento.cbslocal.com/category/news/local/feed/',
			'http://fox40.com/category/news/local-news/feed/',
			'http://www.ksbw.com/8282574?format=rss_2.0&view=feed',
			'http://www.kionrightnow.com/rss/23048552?format=rss_2.0&view=feed',
			'http://www.cbs8.com/Global/category.asp?clienttype=rss_img&C=154671',
			'http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?siteId=100002&obfType=RSS_FEED&categoryId=20000',
			'http://www.kpbs.org/news/2016/mar/24/dead-gray-whale-washes-ashore-at-torrey-pines/',
			'http://www.nbcsandiego.com/news/local/?rss=y&embedThumb=y&summary=y',
			'http://fox5sandiego.com/category/news/feed/',
			'http://www.nbcbayarea.com/news/local/?rss=y&embedThumb=y&summary=y',
			'http://kron4.com/feed/',
			'http://abc7news.com/feed/',
			'http://www.telemundoareadelabahia.com/noticias/local/?rss=y&embedThumb=y&summary=y',
			'http://ww2.kqed.org/news/feed',
			'http://www.keyt.com/18249944?format=rss_2.0&view=feed',
			'http://feeds.feedburner.com/KRCBNorthBayReport?format=xml',
			'http://www.kgoradio.com/feed/',
			'http://www.newspress.com/Top/rss/rss.jsp?s=LOCAL',
			'http://www.mymotherlode.com/category/news/local/feed',
			'http://920kvec.com/feed/',
			'http://www.latimes.com/local/rss2.0.xml',
			'http://feeds.mercurynews.com/mngi/rss/CustomRssServlet/568/200748.xml',
			'http://www.ocregister.com/common/rss/rss.php?catID=18800',
			'http://www.sandiegouniontribune.com/rss/headlines/most-recent/',
			'http://www.sfgate.com/rss/feed/Top-Sports-Stories-RSS-Feed-487.php',
			'http://www.sfgate.com/bayarea/feed/Bay-Area-News-429.php',
			'http://feeds.contracostatimes.com/mngi/rss/CustomRssServlet/571/200207.xml',
			'http://www.pe.com/common/rss/rss.php?catID=24090',
			'http://www.sgvtribune.com/section?template=RSS&profile=4000415&mime=xml',
			'http://www.dailybreeze.com/section?template=RSS&profile=4000336&mime=xml',
			'http://www.modbee.com/news/local/?widgetName=rssfeed&widgetContentId=712766&getXmlFeed=true',
			'http://www.pressdemocrat.com/rss-news',
			'http://www.presstelegram.com/section?template=RSS&profile=4000254&mime=xml',
			'http://www.dailybulletin.com/section?template=RSS&profile=4000603&mime=xml',
			'http://www.chicoer.com/section?template=RSS&profile=4004437&mime=xml',
			'http://www.newspress.com/Top/rss/rss.jsp?s=LOCAL',
			'http://www.montereyherald.com/section?template=RSS&profile=4004745&mime=xml',
			'http://www.vvdailypress.com/news?template=rss&mime=xml',
			'http://www.mercedsunstar.com/news/local/?widgetName=rssfeed&widgetContentId=711265&getXmlFeed=true',
			'http://www.lodinews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://napavalleyregister.com/search/?f=rss&c=news&l=25&s=start_time&sd=desc',
			'http://www.stanforddaily.com/feed/',
			'http://rssfeeds.thecalifornian.com/salinas/news',
			'http://www.redbluffdailynews.com/section?template=RSS&profile=4004603&mime=xml',
			'http://www.redlandsdailyfacts.com/section?template=RSS&profile=4000770&mime=xml',
			'http://www.mantecabulletin.com/syndication/feeds/rss/',
			'http://www.bakersfield.com/rss',
			'http://asbarez.com/feed/',
			'http://feeds.insidebayarea.com/mngi/rss/CustomRssServlet/181/201307.xml',
			'http://www.pasadenastarnews.com/section?template=RSS&profile=4000511&mime=xml',
			'http://www.recorderonline.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local_news*&f=rss',
			'http://www.redding.com/feeds/rss/news/local',
			'http://www.signalscv.com/syndication/feeds/rss/',
			'http://www.santacruzsentinel.com/section?template=RSS&profile=4004654&mime=xml',
			'http://www.dailydemocrat.com/section?template=RSS&profile=4004985&mime=xml',
			'http://www.vcstar.com/feeds/rss/news/local/ventura',
			'http://feeds.feedburner.com/Sacobserver?format=xml',
			'http://www.eastbayexpress.com/oakland/Rss.xml?section=1063824',
			'http://www.goldenstatenewspapers.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=tracy_press/our_town,tracy_press/our_town/*&f=rss',
			'http://berkeleydailyplanet.com/feeds/full.rss',
			'http://www.palipost.com/feed/',
			'http://www.sanbenitocountytoday.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss'
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
			location = "CA"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			