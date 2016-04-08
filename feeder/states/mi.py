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
			'https://wcmu.org/news/?feed=rss2&cat=11',
			'http://fox-obfeeds.endplay.com/feeds/rssFeed?obfType=RSS_FEED&siteId=200002',
			'http://www.clickondetroit.com/feeds/rssFeed/feedServlet?obfType=GMG_RSS_DETAIL&siteId=800002&categoryId=80041&nbRows=10',
			'http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?obfType=RSS_FEED&siteId=10017&categoryId=10001',
			'http://detroit.cbslocal.com/category/news/feed/',
			'http://www.wnem.com/category/210875/app-news?clienttype=rss',
			'http://www.abc12.com/news/localnews/headlines/index.rss2',
			'http://nbc25news.com/news/local.rss',
			'http://wsmh.com/news/local.rss',
			'http://wwmt.com/news/local.rss',
			'http://woodtv.com/category/news/feed/',
			'http://rssfeeds.wzzm13.com/wzzm13-local&x=1',
			'http://fox17online.com/category/news/feed/',
			'http://wlns.com/category/news/feed/',
			'http://www.wilx.com/news/headlines/index.rss2',
			'http://uppermichiganssource.com/news/local.rss',
			'http://feeds.feedburner.com/upabc10?format=xml',
			'http://upnorthlive.com/news/local.rss',
			'http://www.9and10news.com/category/221201/latest-news?clienttype=rss',
			'http://michiganradio.org/rss.xml',
			'http://www.953mnc.com/rss',
			'http://www.wsjm.com/category/local-stories/feed/',
			'http://www.fmtalk1005.com/news/feed/',
			'http://www.wsgw.com/category/local-news/feed/',
			'http://www.wphm.net/category/local-news/feed/',
			'http://wkmi.com/feed/',
			'http://wfnt.com/feed/',
			'http://wbckfm.com/feed/',
			'http://www.sanilacbroadcasting.com/category/local-news/feed/',
			'http://www.lenconnect.com/news?template=rss&mime=xml',
			'http://www.allegannews.com/rss.xml',
			'http://www.thealpenanews.com/page/syndRSS.front/headline.xml?ID=5009&subCatID=5004',
			'https://feeds.feedblitz.com/battlecreek/news&x=1',
			'http://blog.mlive.com/news_impact/atom.xml',
			'http://blog.mlive.com/annarbornews_impact/atom.xml',
			'http://blog.mlive.com/news/baycity_impact/atom.xml',
			'http://blog.mlive.com/news/detroit_impact/atom.xml',
			'http://blog.mlive.com/newsnow_impact/atom.xml',
			'http://blog.mlive.com/grpress/news_impact/atom.xml',
			'http://blog.mlive.com/citpat/news_impact/atom.xml',
			'http://blog.mlive.com/kzgazette_impact/atom.xml',
			'http://impact.mlive.com/lansing-news/atom.xml',
			'http://impact.mlive.com/lansing-news/atom.xml',
			'http://blog.mlive.com/saginawnews_impact/atom.xml',
			'http://www.antrimreview.net/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=local_news*&f=rss',
			'http://bellevilleareaindependent.com/category/news/feed/',
			'http://rssfeeds.hometownlife.com/livonia/news&x=1',
			'http://pilotonline.com/search/?q=&nsa=eedition&l=20&s=start_time&sd=desc&f=rss&c%5B%5D=inside-business',
			'http://www.tuscolatoday.com/index.php/feed/',
			'http://www.iosconews.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.sturgisjournal.com/news?template=rss&mime=xml',
			'http://www.thenewsherald.com/?rss=news',
			'http://www.heraldpalladium.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.stignacenews.com/news.xml',
			'http://www.petoskeynews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.argus-press.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news/national,news/national/*&f=rss',
			'http://milawyersweekly.com/feed/',
			'http://www.macombdaily.com/section?template=RSS&profile=4001918&mime=xml',
			'http://www.miningjournal.net/page/syndrss.front/headline.xml',
			'http://www.mackinacislandnews.com/news.xml',
			'http://www.sunad.com/feed/',
			'https://feeds.feedblitz.com/lansing/news&x=1',
			'http://www.yourdailyglobe.com/rss',
			'http://www.sentinel-standard.com/news?template=rss&mime=xml',
			'http://www.hollandsentinel.com/news?template=rss&mime=xml',
			'http://www.hillsdale.net/news?template=rss&mime=xml',
			'http://www.hillsdalecollegian.com/feed/',
			'http://www.grandhaventribune.com/rss/news',
			'http://www.petoskeynews.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.tctimes.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news*&f=rss',
			'http://www.dailypress.net/page/syndrss.front/headline.xml',
			'http://statenews.com/section/news.xml',
			'http://michronicleonline.com/category/local-news/feed/',
			'http://www.metrotimes.com/detroit/Rss.xml?section=2135207',
			'http://rssfeeds.detroitnews.com/detroit/home&x=1',
			'http://rssfeeds.freep.com/freep/news',
			'http://www.thedailyreporter.com/news?template=rss&mime=xml',
			'http://www.cheboygannews.com/news?template=rss&mime=xml'
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
			location = "MI"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			