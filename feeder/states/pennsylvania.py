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
			'http://www.wfmz.com/24835118?format=rss_2.0&view=feed',
			'http://wjactv.com/news/local.rss',
			'http://www.erietvnews.com/category/205182/news?clienttype=rss',
			'http://www.wgal.com/9361432?format=rss_2.0&view=feed',
			'http://local21news.com/news/local.rss',
			'http://abc27.com/feed/',
			'http://fox43.com/category/news/feed/',
			'http://philadelphia.cbslocal.com/category/news/local/feed/',
			'http://6abc.com/feed/',
			'http://www.nbcphiladelphia.com/news/local/?rss=y&embedThumb=y&summary=y',
			'http://phl17.com/category/phl17-morning-news/feed/',
			'http://www.telemundo62.com/noticias/local/?rss=y&embedThumb=y&summary=y',
			'http://pittsburgh.cbslocal.com/category/news/local/feed/',
			'http://www.wtae.com/9682036?format=rss_2.0&view=feed',
			'http://wnep.com/category/news/feed/',
			'http://fox56.com/news/local.rss',
			'http://www.wsba910.com/category/blog-910-wsba-news-center/feed/',
			'http://wnpv1440.com/category/news-archives/feed/',
			'http://wkok.com/feed/',
			'http://www.newsitem.com/news.xml',
			'http://www.morning-times.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.observer-reporter.com/rss',
			'http://www.delcotimes.com/section?template=RSS&profile=4003208&mime=xml',
			'http://www.exploreclarion.com/feed/',
			'http://blog.lehighvalleylive.com/lvnews_impact/rss.xml',
			'http://www.gettysburgtimes.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news&f=rss',
			'http://www.heraldstandard.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local_news*&f=rss',
			'http://www.theintell.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.kanerepublican.com/rss.xml',
			'http://www.metro.us/rss.xml?c=1414044023-2',
			'http://www.mcall.com/news/local/rss2.0.xml',
			'http://www.pottsmerc.com/section?template=RSS&profile=4002173&mime=xml',
			'http://www.dailyamerican.com/search/?q=&t=article&l=25&d=&d1=&d2=&s=start_time&sd=desc&c[]=news/local*&f=rss',
			'http://www.dailylocal.com/section?template=RSS&profile=4002110&mime=xml',
			'http://feeds.feedburner.com/tribliveBreakingNews?format=xml',
			'http://www.bradfordera.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.citizensvoice.com/cmlink/1.54220',
			'http://www.altoonamirror.com/page/syndRSS.front/headline.xml?subCatID=742',
			'http://www.timesonline.com/search/?c[]=news/local_news&f=rss',
			'http://www.timesherald.com/section?template=RSS&profile=4001772&mime=xml',
			'http://timesleader.com/category/news/feed',
			'http://www.tnonline.com/news/rss',
			'http://www.thetimes-tribune.com/cmlink/1.8269',
			'http://www.wayneindependent.com/news?template=rss&mime=xml',
			'http://www.tiogapublishing.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://sungazette.com/page/syndrss.front/headline.xml',
			'https://feeds.feedblitz.com/ydr/home&x=1',
			'http://feeds.feedblitz.com/yorkdispatch/news',
			'http://cumberlink.com/search/?f=rss&t=article&c=news/local&l=25&s=start_time&sd=desc',
			'http://www.smdailypress.com/rss.xml',
			'http://www.ridgwayrecord.com/rss.xml',
			'http://www.tiogapublishing.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=potter_leader_enterprise/news,potter_leader_enterprise/news/*&f=rss',
			'http://www.therecordherald.com/news?template=rss&mime=xml',
			'http://www.republicanherald.com/cmlink/1.87589',
			'http://www.phillytrib.com/search/?q=&t=article&l=10&d=&d1=&d2=&s=start_time&sd=desc&c[]=news,news/*&f=rss',
			'http://www.post-gazette.com/rss/local',
			'http://www.poconorecord.com/news?template=rss&mime=xml',
			'http://www.philly.com/philly_news.rss',
			'http://www.cpbj.com/section&template=rss&cat=CPBJ01,BLOGEXTRA,FACEFORWARD13,MAINDISH,REALESTATE&taxonomy=7130,7122,7126,7779,7693,7141,7646,7167,7150,7695,7154,7156,7785,7786,7787,7160,7164,7166',
			'http://www.echo-pilot.com/news?template=rss&mime=xml',
			'http://www.mainlinemedianews.com/?rss=main_line_times/news',
			'http://www.neagle.com/news?template=rss&mime=xml',
			'http://newpittsburghcourieronline.com/category/news/feed/',
			'http://www.shipnc.com/search/?q=&t=article&l=100&d=&d1=&d2=&s=start_time&sd=desc&nsa=eedition&c[]=news,news/*&f=rss',
			'http://www.pressandjournal.com/?format=feed&type=rss',
			'http://www.pghcitypaper.com/pittsburgh/Rss.xml',
			'http://temple-news.com/feed/'
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
			location = "PA"

			try:
				cur.execute("""INSERT INTO feeds_feeds(title, link, time, image, source, location) VALUES (%s, %s, %s, %s, %s, %s)""", (title, link, time, imageUrl, source, location))
				dbconnect.commit()
				
			except psycopg2.IntegrityError:
				dbconnect.rollback()

				
				

				

			