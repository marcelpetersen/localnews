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
			'http://woub.org/news/feed/',
			'http://www.wlwt.com/9838828?format=rss_2.0&view=feed',
			'http://scrippsobfeeds.endplay.com/content-syndication-portlet/feedServlet?obfType=RSS_FEED&siteId=10015&categoryId=20000',
			'http://local12.com/news/local.rss',
			'http://www.fox19.com/global/Category.asp?c=106132&clienttype=rss',
			'http://rssfeeds.wkyc.com/wkyc/news&x=1',
			'http://scrippsobfeeds2.endplay.com/content-syndication-portlet/feedServlet?obfType=RSS_FEED&siteId=10003&categoryId=20000',
			'http://fox8.com/category/news/feed/',
			'http://www.cleveland19.com/category/216452/kpho-newstream?clienttype=rss',
			'http://cle43.com/feed',
			'http://nbc4i.com/feed/',
			'http://abc6onyourside.com/news/local.rss',
			'http://www.10tv.com/content/syndication/news_central-ohio.xml',
			'http://myfox28columbus.com/news/local.rss',
			'http://wdtn.com/feed/',
			'http://wdtn.com/feed/',
			'http://www.whio.com/list/rss/news/local/whio-local-news/aMzc/',
			'http://abc22now.com/news/local.rss',
			'http://fox45now.com/news/local.rss',
			'http://www.thenewscenter.tv/content/news/index.rss2',
			'http://www.yourohiovalley.com/?clienttype=rss',
			'http://wtov9.com/news/local.rss',
			'http://www.wtol.com/Global/category.asp?C=160943&clienttype=rss',
			'http://www.13abc.com/home/headlines/index.rss2',
			'http://nbc24.com/news/local.rss',
			'http://www.wfmj.com/category/229774/mobile-news-category?clienttype=rss',
			'http://wkbn.com/category/news/local-news/feed/',
			'http://wytv.com/category/news/local-news/feed/',
			'http://www.wsaz.com/news/index.rss2',
			'http://newstalkcleveland.newsone.com/category/cle/feed/',
			'http://wfin.com/category/local-news/feed/',
			'http://www.whio.com/list/rss/news/local/whio-local-news/aMzc/',
			'http://www.ohio.com/cmlink/1.114425',
			'http://www.cantonrep.com/news?template=rss&mime=xml',
			'http://rssfeeds.cincinnati.com/cincinnati-news&x=1',
			'http://blog.cleveland.com/realtimenews/atom.xml',
			'http://blog.cleveland.com/sunmessenger/atom.xml',
			'http://blog.cleveland.com/sunpostherald/atom.xml',
			'http://blog.cleveland.com/sunpress/atom.xml',
			'http://blog.cleveland.com/thesun/atom.xml',
			'http://blog.cleveland.com/sunstarcourier/atom.xml',
			'http://blog.cleveland.com/westshoresun/atom.xml',
			'http://blog.cleveland.com/callandpost/atom.xml',
			'http://blog.cleveland.com/brunswicksuntimes/atom.xml',
			'http://blog.cleveland.com/chagrinsolonsun/atom.xml',
			'http://blog.cleveland.com/medinasun/atom.xml',
			'http://blog.cleveland.com/newssun/atom.xml',
			'http://www.dispatch.com/content/syndication/news_local-state.xml',
			'http://www.daytondailynews.com/list/rss/news/local/latest-local-news/aD6t/',
			'http://www.toledoblade.com/rss/local',
			'http://www.tribtoday.com/page/syndRSS.front/headline.xml?ID=5028&subCatID=5021',
			'http://www.vindy.com/mobile/rss/local/',
			'http://mydailytribune.com/category/news/feed',
			'http://www.heraldstaronline.com/page/syndRSS.front/headline.xml?ID=5015&subCatID=5010',
			'http://www.springfieldnewssun.com/list/rss/news/local/latest-headlines/aFBt/',
			'http://rssfeeds.lohud.com/westchester/news',
			'http://www.news-herald.com/section?template=RSS&profile=4002047&mime=xml',
			'http://www.crescent-news.com/feed',
			'http://sidneydailynews.com/feed',
			'http://www.sanduskyregister.com/rss/news',
			'http://www.reviewonline.com/page/syndrss.front/headline.xml',
			'http://mydailysentinel.com/category/news/feed',
			'http://portsmouth-dailytimes.com/feed',
			'http://www.daytoncitypaper.com/',
			'http://dailycall.com/feed',
			'http://thelantern.com/feed/',
			'http://rssfeeds.coshoctontribune.com/coshocton/news',
			'http://www.morningjournal.com/section?template=RSS&profile=4002041&mime=xml',
			'http://rssfeeds.mansfieldnewsjournal.com/mansfield/news&x=1',
			'http://www.indeonline.com/news?template=rss&mime=xml',
			'http://www.timesreporter.com/news?template=rss&mime=xml',
			'http://rssfeeds.newarkadvocate.com/newark/news&x=1',
			'http://norwalkreflector.com/rss/local',
			'http://buchtelite.com/category/news/feed/',
			'http://www.todayspulse.com/list/rss/news/local/butler-county-news/aGh7/',
			'http://www.todayspulse.com/list/rss/news/local/warren-county-news/aGh8/',
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
					imageUrl = 'http://polar-spire-13485.herokuapp.com/static/img/logo3.png'

			source = d.feed.title
			location = "OH"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			